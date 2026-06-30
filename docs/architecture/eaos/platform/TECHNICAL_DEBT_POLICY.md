# ⏳ TECHNICAL_DEBT_POLICY.md (EAOS Teknik Borç Yönetim Politikası)

Bu politika belgesi, geliştirme süreçlerinde ortaya çıkan veya bilinçli olarak ertelenen teknik borçların (technical debt) nasıl sınıflandırılacağını, takip edileceğini ve ne zaman kapatılacağını belirler. [GOVERNANCE.md](../GOVERNANCE.md) Madde 2'ye doğrudan bağlıdır.

---

## 1. Teknik Borç Sınıflandırma Matrisi

| Seviye | Tanım | Production Geçiş Kuralı | Çözüm Süresi |
|---|---|---|---|
| 🔴 **Critical** | Güvenlik açığı yaratan, tenant izolasyonunu ihlal eden, ses gecikmesini artıran veya veri kaybı riski taşıyan borçlar. | **KESİNLİKLE YASAK.** Canlıya çıkamaz. | Anında çözülmeli. |
| 🟠 **High** | Kod okunabilirliğini ciddi şekilde düşüren, test kapsamını eksik bırakan, geçici geçici çözümler (workarounds). | Sınırlı ve feature flag arkasında izin verilebilir. | Sonraki sprint içinde. |
| 🟡 **Medium** | Performansa doğrudan etkisi olmayan ancak standardı tam karşılamayan kod yapıları (refactoring ihtiyaçları). | İzin verilir. | 2 Sprint içinde. |
| 🟢 **Low** | Dokümantasyon iyileştirmeleri, minor kod temizlikleri. | İzin verilir. | Planlanan dönem içinde. |

---

## 2. Teknik Borç Takibi
* Tüm teknik borçlar `docs/project-management/debt/TECHNICAL_DEBT.md` (veya Jira/Git issues) üzerinde kayıt altına alınmalıdır.
* Her kayıt; borcun neden ertelendiğini, olası etkilerini ve hangi sprint içinde kapatılacağını açıkça içermelidir.

---

## 3. Kod Kalitesi Taahhüdü
Yeni bir modül yazılırken "hızlı teslimat" amacıyla geçici olarak eklenen `TODO` veya `FIXME` etiketli kodlar, sertifikasyon aşamasında temizlenmek zorundadır. Critical seviyede bir borcun gözden kaçarak canlıya çıkması durumunda, Platform Guardian yayını anında durdurma (rollback) yetkisine sahiptir.
