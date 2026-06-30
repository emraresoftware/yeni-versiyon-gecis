# 🏛️ EAOS Governance (Yönetişim ve Geliştirme Kuralları)

Bu belge, EAOS platformunda kararların nasıl alınacağını, kodun nasıl yazılacağını ve değişikliklerin üretim (production) ortamına nasıl güvenle taşınacağını tanımlar.

---

## 1. Mimari Karar Alma Süreci (RFC & ADR)
* **ADR (Architectural Decision Records):** Mimariyi etkileyecek her türlü radikal değişiklik (yeni veri tabanı, yeni servis eklenmesi, kütüphane değişimi) bir ADR dosyası olarak `docs/adr/` altında belgelenmelidir.
* **Format:** Her ADR; bağlam (context), karar (decision) ve sonuçlar (consequences) bölümlerini içermelidir.
* **Onay Mekanizması:** Değişiklik kodlanmadan önce ADR belgesi hazırlanmalı ve `Chief Architect` tarafından onaylanmalıdır.

---

## 2. Geliştirme ve Entegrasyon Döngüsü
Geliştiriciler ve AI ajanları için zorunlu entegrasyon protokolü:

```
[KOD DEĞİŞİKLİĞİ] ──► [LOKAL TEST] ──► [PRE-FLIGHT CHECK] ──► [STAGING DEPLOY] ──► [QA ONAYI] ──► [PROD DEPLOY]
```

1. **Pre-flight Check:** Kod tabanına dokunmadan önce `AGENTS.md` ve `ANAYASA.md` dosyalarını okumak ve doğrulamak zorunludur.
2. **Commit Konvansiyonu:** Commit mesajlarında hangi task'ın yapıldığı ve neyin değiştiği açıkça yazılmalıdır (Örn: `feat: add circuit breaker for openai realtime adapter`).
3. **Mühürlü Ayarların Korunması:** `SEALED_SETTINGS.md` altındaki parametreler kesinlikle onay alınmadan değiştirilemez.

---

## 3. Yetkilendirme ve Güvenlik Seviyeleri (Authorization)
* **Seviye 1 (Core Engine):** Ses köprüsü, gateway ve yönlendiriciler. Sadece tam yetkili kıdemli geliştiriciler veya onaylanmış otonom süreçler tarafından değiştirilebilir.
* **Seviye 2 (Business Modules):** CRM, ERP, Task ve Bilet süreçleri. Standart geliştirici kurallarıyla güncellenebilir.
* **Seviye 3 (Adapters & Tools):** API Marketplace üzerindeki yeni entegrasyonlar. Hızlı eklenebilir ancak asenkron ve timeout sınırlarına tabi olmalıdır.

---

## 4. Kalite Güvence (QA) ve Raporlama
Her görev (task) sonunda:
* **Geliştirici Ajan (Agent 1):** `TASK_XXX_REPORT.md` dosyasını oluşturmalıdır.
* **QA Ajanı (Agent 2):** Bağımsız testleri çalıştırıp `QA_TASK_XXX.md` raporunu yazmalıdır.
* **Chief Architect:** İnceleme raporunu (`ARCHITECT_REVIEW_TASK_XXX.md`) onaylayıp yayına alma izni vermelidir.
