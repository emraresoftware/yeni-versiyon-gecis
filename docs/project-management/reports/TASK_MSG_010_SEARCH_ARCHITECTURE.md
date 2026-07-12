PRE-FLIGHT CHECK
✓ AGENTS.md
✓ ANAYASA.md
✓ DOMAIN_MODEL.md

# TASK_MSG_010 Search Strategy: PostgreSQL FTS to OpenSearch Stratejisi

Stratejik araştırma ve mimari plan raporudur.

---

## 1. PostgreSQL FTS Yeterlilik & Sınırlar Değerlendirmesi

PostgreSQL Full Text Search (FTS) ve GIN indeksleri (`tsvector`), sistemin başlangıç ve orta ölçekli evrelerinde (kiracı başına <10M mesaj, toplam <50M mesaj) arama ihtiyaçları için son derece yeterlidir ve ekstra altyapı maliyeti gerektirmez.

Ancak, aşağıdaki durumlarda PostgreSQL yetersiz kalır ve OpenSearch geçişi tetiklenmelidir:
* **Yazım Hatası Toleransı (Typo Tolerance):** FTS, GIN indeksi etkilenmeden Levenshtein mesafesine dayalı hızlı fuzzy arama yapamaz. `pg_trgm` (trigram) indeksleri ise büyük metinlerde yavaştır.
* **BM25 Sıralama (Relevance Ranking):** `ts_rank` sadece kelime frekansı ve sıklığına bakar. OpenSearch'ün BM25 gibi gelişmiş istatistiksel modellerini, zaman aşımı azalımını (decay functions) veya özel alan ağırlıklandırma (field boosting) mekanizmalarını barındırmaz.
* **Yüksek Yük & Lock Darboğazları:** 100M+ satır içeren veritabanlarında, concurrent GIN indeks aramaları yüksek disk I/O'suna sebep olur ve birincil veritabanı işlemlerini yavaşlatır.

---

## 2. İndekslenecek Veri Şeması (Denormalized Inbox Document)

Arama motoruna yazılacak denormalize edilmiş belge yapısı (`InboxSearchDocument`) şu alanları içerecektir:

```json
{
  "messageId": "UUID",
  "tenantId": "UUID",
  "conversationId": "UUID",
  "channelType": "keyword",
  "status": "keyword",
  "sender": {
    "name": "text",
    "email": "keyword",
    "phone": "keyword"
  },
  "content": {
    "text": "text",
    "attachments": [
      {
        "filename": "text",
        "mimeType": "keyword"
      }
    ]
  },
  "ticket": {
    "subject": "text",
    "priority": "keyword"
  },
  "tags": ["keyword"],
  "createdAt": "date"
}
```

---

## 3. Tenant Isolation (Kiracı İzolasyonu)

* **Enterprise / Özel Kurulumlar:** Her tenant için ayrı bir indeks oluşturulur: `inbox-search-{tenantId}`. En yüksek güvenlik izolasyonunu sağlar ve gdpr/kvkk kapsamında veri silmeyi (purge) kolaylaştırır.
* **Standart SaaS Müşterileri:** Paylaşımlı tek bir indeks (`inbox-search-shared`) kullanılır. 
  - Belgelere zorunlu `tenantId` alanı eklenir.
  - Sorgularda `routing` anahtarı olarak `tenantId` belirlenerek verinin diskteki shard izolasyonu sağlanır.
  - Arama API'si en üst katmanda oturumdaki `tenantId` filtresini sorguya otomatik enjekte eder (Fail-Closed Isolation).

---

## 4. Sıralama (Ranking) & Alan Ağırlıkları (Boosting)

* **Base Algorithm:** BM25 (Best Matching 25) kullanılacaktır.
* **Query-Time Boosting:**
  - Konu başlığı (Subject): `boost: 3.0`
  - Gönderen adı/bilgisi: `boost: 2.0`
  - Mesaj içeriği (Body): `boost: 1.0`
* **Time Decay:** `createdAt` tarihi esas alınarak üstel azalım fonksiyonu (Exponential/Gauss Decay) uygulanır. Böylece aynı kelimeleri içeren eski bir mesaj yerine yeni gelen mesaj en üstte gösterilir.

---

## 5. Yazım Hatası Toleransı (Typo Tolerance)

* OpenSearch `fuzziness` parametresi ile entegre edilir:
  - 1-2 karakterlik kelimeler için: `fuzziness: 0` (Fuzzy kapalı).
  - 3-5 karakterlik kelimeler için: `fuzziness: 1` (1 edit mesafesi).
  - 5 karakterden uzun kelimeler için: `fuzziness: 2` (2 edit mesafesi).
* Edge N-Gram tokenizers ile "search-as-you-type" desteği kurulacaktır.

---

## 6. Dil Desteği (Language Support)

Metin alanları multi-field mapping şeklinde tasarlanır:
* `content.text.raw` (Arama yapılmayan, birebir eşleşme için).
* `content.text.turkish` (Türkçe morfolojik analiz/stemmer).
* `content.text.english` (İngilizce analiz/stemmer).
* Arama esnasında sorgu `multi_match` ile tüm dil alt alanlarında koşturulur.

---

## 7. Zero-Downtime Reindexing

* İndeks isimleri doğrudan kullanılmaz. Bunun yerine **Index Aliases** kullanılır:
  - Okuma Alias'ı: `inbox-search-read`
  - Yazma Alias'ı: `inbox-search-write`
* Şema veya mapping güncellenmesi gerektiğinde:
  1. `inbox-search-v2` yeni mapping ile oluşturulur.
  2. Yazma alias'ı v2'ye yönlendirilir.
  3. OpenSearch `Reindex` API ile veriler arka planda v1'den v2'ye aktarılır.
  4. Okuma alias'ı v2'ye yönlendirilir.
  5. Eski indeks `inbox-search-v1` silinir.

---

## 8. Eşitleme Stratejisi (Sync Strategy)

Çift yönlü (Dual-Sync) eşitleme modeli uygulanır:
1. **Real-time Sync (Write-Path):**
   - Gateway üzerinde mesaj kaydedildiğinde **Transactional Outbox** tablosuna `message_received` veya `status_changed` event'i yazılır.
   - Outbox dispatcher bu eventi alıp OpenSearch'e gönderir. Böylece HTTP request döngüsü OpenSearch gecikmesinden etkilenmez.
2. **Periodic Reconciliation (Batch Sync):**
   - Her gece çalışan bir background worker, PostgreSQL son güncellenme tarihleri ile OpenSearch üzerindeki döküman sayılarını karşılaştırır ve eksik/hatalı kayıtları senkronize eder.

---

## 9. Fallback Stratejisi (Resiliency)

* **OpenSearch Kesintisi (Write Fallback):**
  - Outbox dispatcher, OpenSearch'e yazarken hata alırsa transient hata retry politikası ile (exponential backoff + jitter) bekletir. OpenSearch ayağa kalktığında kuyruktaki tüm veriler sıralı şekilde işlenir.
* **OpenSearch Kesintisi (Read Fallback):**
  - Arama API'si OpenSearch'e ulaşamazsa, hata fırlatmak yerine şeffaf bir şekilde PostgreSQL FTS (`tsquery`) fallback metoduyla aramayı veritabanında çalıştırır. Kullanıcıya arama sonucunun toleranssız/yavaş gelebileceğine dair bir metadata bayrağı dönülür, ancak arama hizmeti kesintiye uğramaz.

---

## 10. Altyapı Maliyet Analizi & Tetikleyici (Trigger)

| Kriter | PostgreSQL FTS | OpenSearch Cluster |
| ------ | -------------- | ------------------ |
| **Ek Sunucu Maliyeti** | $0 | Min. 2x Node (Prod HA için min. 3) |
| **Bellek Tüketimi** | Düşük (Mevcut paylaşımlı) | Yüksek (JVM Heap RAM gereksinimi) |
| **Yazım Hatası Desteği**| Yok veya Yavaş | Çok Hızlı (Fuzzy Levenshtein) |
| **Arama Hızı (Büyük Veri)**| Yavaş (>50M satırda I/O kilitleri) | Milisaniyeler mertebesinde |

* **OpenSearch Geçiş Tetikleyicisi:**
  - Tek kiracıda mesaj sayısının **10 Milyon** barajını aşması, veya
  - Toplam veritabanında mesaj tablosunun **50 Milyon** satırı geçmesi, veya
  - Ürün arayüzünde "fuzzy search", "gelişmiş BM25 zaman azalımlı sıralama" isteklerinin zorunlu hale gelmesi.

---

## Final Report

**STATUS:** APPROVED

**DECISION:** ADOPT (PostgreSQL FTS as initial MVP; OpenSearch transition roadmap established)

**POSTGRES_FTS_SCOPE:** Complete FTS integration with GIN index on `ConversationMessages` for MVP stage.

**OPENSEARCH_TRIGGER:** Single tenant > 10M messages OR total messages > 50M.

**TENANT_MODEL:** Shared Index with Routing + Mandatory Filter context.

**INDEX_SCHEMA:** Denormalized Inbox Search Document mappings.

**SYNC_MODEL:** Transactional Outbox write-path + Daily Reconciliation worker.

**RISKS:**
1. OpenSearch split-brain or cluster state locks during high volume shards expansion.
2. Inconsistent document counts between Postgres and OpenSearch during outbox network drops (handled by Reconciliation job).

**BLOCKERS:** None

**READY_FOR_IMPLEMENTATION:** YES (PostgreSQL FTS MVP is ready for TASK_MSG_010 implementation phase)
