# 📋 02_CLIENT_ONBOARDING_BLUEPRINT.md (Kiracı Entegrasyon Planı)

Bu kılavuz, yeni bir müşterinin (kiracının) EAOS platformuna sıfır hata ve sıfır kesintiyle nasıl dahil edileceğini (onboarding) adım adım tanımlar.

---

## 1. Onboarding Aşamaları (5 Temel Faz)

### Faz 1: Analiz ve Kurulum (1. - 3. Gün)
* Kiracı veritabanı izolasyon tipinin (Logical / Physical DB) belirlenmesi.
* SIP trunk ve DID (telefon numaraları) bilgilerinin veritabanına (`SipTrunks`) tanımlanması.

### Faz 2: AI ve Ses Eğitimi (4. - 7. Gün)
* Kiracı prompt şablonlarının (`AgentSystemPromptOverride`) ve karşılama metinlerinin (`AgentCustomSettings`) sisteme tanımlanması.
* ElevenLabs veya yerel ses sentezleyici profilinin dondurulması.

### Faz 3: Entegrasyon (8. - 12. Gün)
* Kiracının kullandığı ERP/CRM sistemlerinin `API Marketplace` veya `Connector` aracılığıyla sisteme bağlanması.
* Ajanların kullanabileceği araçların (tool declarations) doğrulanması.

### Faz 4: Test ve Doğrulama (13. - 14. Gün)
* Kapalı devre sesli çağrı testleri, barge-in hassasiyet kontrolleri.
* Yük ve regresyon testleri (`MODULE_CERTIFICATION.md` kurallarına göre).

### Faz 5: Canlıya Geçiş (Go-Live)
* `12_GOLIVE_BLUEPRINT.md` protokolüne göre kontrollü geçiş.
