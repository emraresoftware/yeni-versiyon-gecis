# 🧭 Master Architecture Index

**Title:** Master Architecture Index
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** Yok
**Related Documents:** Tüm Mimari Dökümanlar

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Initial creation and added Document Dependency Matrix. |

---

## Amaç

Master Architecture Index, Emare Business Operating System (BOS) mimari dokümantasyonunun merkezi fihristi, okuma sırası, bağımlılıkları ve genel kılavuzudur. Projeye katılan tüm geliştiriciler ve AI ajanları platformun genel tasarım ilkelerini anlamak için bu indeksi referans almalıdır.

---

## Kapsam

Bu indeks platform genelindeki tüm mimari, veri, güvenlik, entegrasyon, geliştirme ve altyapı dökümanlarını listeler ve birbirleriyle olan ilişkilerini tanımlar.

---

## Hedef Kitle

* Geliştiriciler
* AI Ajanları
* Mimari Kurul (Architecture Board)

---

## Katman Bağımlılık Kuralları

Platformda Clean Architecture prensipleri uygulanmaktadır. Bağımlılık yönü daima içe doğrudur:

`Web / UI (En dış)` ➡️ `API` ➡️ `Infrastructure / Persistence` ➡️ `Application` ➡️ `Domain (En iç - bağımsız)`

### 5 Kritik Katman Yasağı:
1. **Controller ➡️ DbContext Yasaktır:** Veritabanı işlemleri doğrudan API Controller'larda yapılamaz.
2. **UI ➡️ Entity Yasaktır:** UI katmanı Domain Entity sınıflarını doğrudan kullanamaz, sadece DTO'ları kullanır.
3. **Domain ➡️ Infrastructure Yasaktır:** Domain katmanı altyapı sınıflarına bağımlı olamaz.
4. **Application ➡️ Infrastructure Implementation Yasaktır:** Application katmanı somut altyapı sınıflarına bağımlı olamaz, interface kullanır.
5. **Domain ➡️ Hiçbir Katmana Bağımlı Olamaz:** Domain en iç katmandır, bağımsız olmak zorundadır.

Daha fazla detay için bkz. [ADR-0002 — Clean Architecture](file:///Users/emre/yeni-versiyon-gecis/docs/adr/0002-clean-architecture.md).

---

## Doküman Bağımlılık Matrisi

| Doküman | Birincil Bağımlılıklar | İkincil Bağımlılıklar | Durum | Not |
| ------- | ---------------------- | --------------------- | ----- | --- |
| [MASTER_ARCHITECTURE_INDEX.md](file:///Users/emre/yeni-versiyon-gecis/MASTER_ARCHITECTURE_INDEX.md) | Yok | Tüm Diğer Dokümanlar | ✅ Approved | Giriş kapısı ve fihrist |
| [README.md](file:///Users/emre/yeni-versiyon-gecis/README.md) | MASTER_ARCHITECTURE_INDEX.md | DOMAIN_MODEL.md, BOUNDED_CONTEXTS.md | ✅ Approved | Hızlı başlangıç ve mimari özet |
| [ANAYASA.md](file:///Users/emre/yeni-versiyon-gecis/ANAYASA.md) | Yok | ORTAK_TEKNIK_PROTOKOL.md, ERD_MODEL.md, DOMAIN_MODEL.md | ✅ Approved | Kod kalitesi ve kuralları |
| [ORTAK_TEKNIK_PROTOKOL.md](file:///Users/emre/yeni-versiyon-gecis/ORTAK_TEKNIK_PROTOKOL.md) | ANAYASA.md, README.md | STATUS.md, REFERANSLAR.md | ✅ Approved | AI ajan çalışma kuralları |
| [DOMAIN_MODEL.md](file:///Users/emre/yeni-versiyon-gecis/DOMAIN_MODEL.md) | BOUNDED_CONTEXTS.md | ERD_MODEL.md, UBIQUITOUS_LANGUAGE.md | ✅ Approved | Temel domain nesneleri ve aggregate'ler |
| [ERD_MODEL.md](file:///Users/emre/yeni-versiyon-gecis/ERD_MODEL.md) | DOMAIN_MODEL.md | UBIQUITOUS_LANGUAGE.md | ✅ Approved | Veritabanı tabloları ve ilişkiler |
| [BOUNDED_CONTEXTS.md](file:///Users/emre/yeni-versiyon-gecis/BOUNDED_CONTEXTS.md) | DOMAIN_MODEL.md | UBIQUITOUS_LANGUAGE.md, EVENT_BUS.md | ✅ Approved | Sorumluluk sınırları ve ACL |
| [UBIQUITOUS_LANGUAGE.md](file:///Users/emre/yeni-versiyon-gecis/UBIQUITOUS_LANGUAGE.md) | DOMAIN_MODEL.md | BOUNDED_CONTEXTS.md | ✅ Approved | Ortak dil ve terim sözlüğü |
| [EVENT_BUS.md](file:///Users/emre/yeni-versiyon-gecis/EVENT_BUS.md) | README.md | WORKFLOW_ENGINE.md, RULE_ENGINE.md | ✅ Approved | Olay tabanlı haberleşme |
| [WORKFLOW_ENGINE.md](file:///Users/emre/yeni-versiyon-gecis/WORKFLOW_ENGINE.md) | EVENT_BUS.md | RULE_ENGINE.md, NOTIFICATION_ENGINE.md | ✅ Approved | Otomasyon ve onay süreçleri |
| [RULE_ENGINE.md](file:///Users/emre/yeni-versiyon-gecis/RULE_ENGINE.md) | WORKFLOW_ENGINE.md | METADATA_ENGINE.md, SECURITY_ARCHITECTURE.md | ✅ Approved | Koddan bağımsız iş kuralları |
| [AI_ENGINE.md](file:///Users/emre/yeni-versiyon-gecis/AI_ENGINE.md) | EVENT_BUS.md | WORKFLOW_ENGINE.md, INTEGRATION_ENGINE.md | ✅ Approved | Merkezi yapay zeka servisleri |
| [METADATA_ENGINE.md](file:///Users/emre/yeni-versiyon-gecis/METADATA_ENGINE.md) | RULE_ENGINE.md | EVENT_BUS.md, WORKFLOW_ENGINE.md | ✅ Approved | Kod yazmadan ekran/alan yönetimi |
| [DATA_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/DATA_ARCHITECTURE.md) | README.md, EVENT_BUS.md | ANALYTICS_ENGINE.md, METADATA_ENGINE.md, SECURITY_ARCHITECTURE.md, OBSERVABILITY.md, INTEGRATION_ENGINE.md | ✅ Approved | Veri saklama ve yaşam döngüsü |
| [SECURITY_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_ARCHITECTURE.md) | README.md | OBSERVABILITY.md, DATA_ARCHITECTURE.md | ✅ Approved | Zero Trust ve veri güvenliği |
| [OBSERVABILITY.md](file:///Users/emre/yeni-versiyon-gecis/OBSERVABILITY.md) | README.md | EVENT_BUS.md, WORKFLOW_ENGINE.md, SECURITY_ARCHITECTURE.md | ✅ Approved | Metrik, log ve dağıtık izleme |
| [DEPLOYMENT_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/DEPLOYMENT_ARCHITECTURE.md) | README.md | OBSERVABILITY.md, SECURITY_ARCHITECTURE.md, DATA_ARCHITECTURE.md, INTEGRATION_ENGINE.md, AI_ENGINE.md | ✅ Approved | K8s, CI/CD ve ortam stratejisi |
