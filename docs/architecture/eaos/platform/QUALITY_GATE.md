# 🏁 QUALITY_GATE.md (EAOS CI/CD Kalite Kapısı)

Bu doküman, kod tabanına yapılacak her bir push ve pull request (PR) işleminin geçmek zorunda olduğu otomatik entegrasyon kalite kapılarını (Quality Gates) belirler. [GOVERNANCE.md](../GOVERNANCE.md) Madde 2'ye doğrudan bağlıdır.

---

## 1. Kalite Kapısı Aşamaları (Quality Gate Pipeline)

Her bir geliştirme adımında aşağıdaki kontroller sırasıyla başarılı olmak zorundadır:

### Adım 1: Kod Formatı ve Düzeni (Lint)
* C# kodları için `dotnet format` ve `Roslyn Analyzer` uyarıları sıfır olmalıdır.
* Python kodları için `flake8` veya `black` standartlarına uyulmalıdır.

### Adım 2: Birim Testler (Unit Tests)
* Backend için xUnit test projelerindeki tüm birim testler başarıyla tamamlanmalıdır.
* **Minimum Test Coverage (Kapsama Oranı):** Yeni yazılan iş mantığı (business logic) kodları için test kapsama oranı en az **%80** olmalıdır.

### Adım 3: Güvenlik Taramaları (Security Scan)
* NuGet ve npm paket bağımlılıklarında bilinen bir zafiyet (Vulnerability) taraması (`dotnet list package --vulnerable` / `npm audit`) yapılmalı ve kritik zafiyet içermemelidir.
* Hassas verilerin (şifre, api key) kod içine sızıp sızmadığı (secrets detection) taranmalıdır.

### Adım 4: Uyumluluk ve Sertifikasyon (Compliance Engine Check)
* `COMPLIANCE_ENGINE.md` ve `ARCHITECTURE_REVIEW_STANDARD.md` kurallarına uygunluk onaylanmalıdır.
* Yeni modüle ait `.md` dokümantasyonu tamamlanmış olmalıdır.

---

## 2. Kalite Kapısı Geçiş Kuralı (Block on Failure)
Otomatik CI/CD hattındaki (GitHub Actions) herhangi bir aşamada kalite kapısı başarısız olursa:
* PR'ın `main` veya `gece-otonom` branch'ine merge edilmesi sistem tarafından otomatik olarak engellenir.
* Platform Guardian onay vermedikçe manuel geçişe (override) izin verilmez.
