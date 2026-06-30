# 🚀 12_GOLIVE_BLUEPRINT.md (Canlıya Geçiş Protokolü)

Bir kiracının EAOS üzerinde canlıya geçiş gününde (Go-Live Day) uygulanacak adım adım eylem planı.

---

## 1. Geçiş Günü Adımları
1. **DNS ve SSL Yönlendirmeleri:** Kiracıya ait sub-domain (örn: `elyafgroup.emarecloud.tr`) doğrulamaları tamamlanır.
2. **SIP Trunk Switch:** Telefon hattı sağlayıcısından gelen arama rotaları Asterisk PBX'e yönlendirilir.
3. **Smoke Test:** Canlı numaradan ilk test araması yapılır. Asistanın karşılama, konuşma ve database ticket oluşturma özellikleri uçtan uca doğrulanır.
4. **Log Doğrulama:** `AIAuditLogs` ve faturalandırma (Billing) kayıtlarının veritabanına düştüğü doğrulanır.
