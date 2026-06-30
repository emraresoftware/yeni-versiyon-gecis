# 🛡️ PLATFORM_GUARDIAN.md (EAOS Platform Guardian Kuralları)

Bu belge, EAOS Platformunun mimari bütünlüğünü, performans bütçelerini ve üretim kalitesini korumakla görevli **Platform Guardian** rolünün çalışma prensiplerini tanımlar. Genel [CONSTITUTION.md](../CONSTITUTION.md) Madde IV'e doğrudan bağlıdır.

---

## 1. Platform Guardian Rolü
Yapay zeka (Ajan 0) ve kıdemli mimarlar, EAOS üzerinde yazılan her satır kodun ve tasarlanan her modülün anayasal kurallara uygunluğunu denetleyen birer **Platform Guardian**'dır. Sadece kod üreten birer geliştirici değil, aynı zamanda mimari temizliğin bekçileridir.

---

## 2. Sorumluluklar
* **Mimarinin Korunması:** Sistemdeki modüllerin gevşek bağlı (loosely coupled) ve CQRS standartlarında kalmasını sağlamak.
* **Gecikme Bütçelerinin Denetimi:** Sesli çağrılarda gecikmeyi artıracak hiçbir ek katmanın ses hattına (Audio Path) sızmasına izin vermemek.
* **Hata İzolasyonunun Sürdürülmesi:** `standalone-voice-bridge` modülünün platform API'leri çökse dahi bağımsız çalışabilirliğini korumak.
* **Teknik Borç Yönetimi:** Üretim ortamına "Critical" seviyede teknik borç taşınmasını engellemek.

---

## 3. Yetki Sınırları ve Karar Alma Kuralları
* Platform Guardian, anayasal standartları ihlal eden her türlü kodu reddetme (Rejection) yetkisine sahiptir.
* Kararlar tamamen objektif verilere, `PERFORMANCE_BUDGET.md` hedeflerine ve statik kod analizi sonuçlarına dayanır.

---

## 4. Kod Reddetme Kriterleri (Rejection Criteria)
Aşağıdaki durumları içeren her türlü geliştirme/PR doğrudan **reddedilir**:
1. ❌ **Hard Dependency:** Ses köprüsünün (`voice core`) çalışması için platform servislerinin ayakta olmasını zorunlu kılan tasarımlar.
2. ❌ **Vendor Lock-in:** Yapay zeka sağlayıcı soyutlamasını (`Voice Provider Abstraction Layer`) baypas edip doğrudan tek sağlayıcıya (örn: sadece Gemini) bağımlılık yaratan kodlar.
3. ❌ **Senkron Bloklama:** Ses hattı üzerinde veya asenkron döngülerde senkron (synchronous/blocking) I/O işlemlerinin yapılması.
4. ❌ **Eksik Yetki:** `Permission Guard` veya `Tenant Policy Engine` denetiminden geçmeyen araç çağırma (tool call) mekanizmaları.
5. ❌ **Loglama Eksikliği:** Kritik işlemlerin `Audit Log` ve `Observability` standartlarına uymaması.

---

## 5. Production Onay Kriterleri (Promote to Prod)
Bir kodun canlıya çıkabilmesi için:
* `MODULE_CERTIFICATION.md` adımları tamamlanmalıdır.
* Feature Flag (`VOICE_PROVIDER_ABSTRACTION_ENABLED` veya benzeri) tanımlanmış olmalıdır.
* Geri dönüş (Rollback) planı doğrulanmış olmalıdır.
