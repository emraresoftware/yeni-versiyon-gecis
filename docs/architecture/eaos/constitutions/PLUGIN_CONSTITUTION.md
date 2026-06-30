# 🔌 PLUGIN_CONSTITUTION.md (EAOS Eklenti ve Pazar Yeri Anayasası)

Bu anayasa, EAOS platformuna eklenecek üçüncü taraf yazılımların, eklentilerin (plugins) ve entegrasyon araçlarının geliştirilme, güvenlik ve dağıtım standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde III.1'e doğrudan bağlıdır.

---

## 1. Plugin SDK
* Tüm eklentiler, EAOS tarafından sağlanan resmi SDK arayüzlerini kullanmalıdır.
* SDK; eklentilerin platform veritabanına, ağa ve dosya sistemine doğrudan erişimini engeller, kontrollü API'ler sunar.

---

## 2. Sandbox (İzole Çalışma Ortamı)
* Eklenti kodları ana uygulama sunucusunda doğrudan çalıştırılamaz.
* Her eklenti, CPU, bellek ve ağ kısıtlamaları olan izole edilmiş Docker container'ları (sandbox) veya WASM (WebAssembly) runtime'ları içinde yürütülür.

---

## 3. Permission (Eklenti İzinleri)
* Her eklenti, kurulurken ihtiyaç duyduğu izinleri (örn: `ReadContacts`, `SendSms`, `NetworkOutbound`) açıkça beyan etmek zorundadır.
* Kiracı yöneticisi bu izinleri onaylamadan eklenti aktif edilemez. Ajanlar, eklentinin izin vermediği hiçbir aracı tetikleyemez.

---

## 4. Versioning (Sürüm Yönetimi)
* Eklentiler **Semantic Versioning (SemVer - MAJOR.MINOR.PATCH)** standardına uymak zorundadır.
* Geriye dönük uyumluluğu bozan (breaking changes) güncellemelerde eklentinin MAJOR sürümü artırılmalı ve kiracılara geçiş süresi tanınmalıdır.

---

## 5. Signing (Dijital İmzalama ve Güvenlik)
* Pazar yerine (Marketplace) yüklenecek her eklenti paketi, geliştiricinin özel anahtarı ve EAOS sertifikası ile dijital olarak imzalanmalıdır.
* İmzası doğrulanmayan veya üzerinde oynanmış eklenti paketleri sisteme kurulamaz.

---

## 6. Dağıtım ve Pazar Yeri (Marketplace)
* **Marketplace Mimarisi:** Eklentiler merkezi EAOS eklenti deposunda barındırılır.
* **Onay Süreci:** Pazar yerine yüklenecek her eklenti; statik kod analizi, güvenlik taraması ve fonksiyonel testlerden geçirilerek onaylanmalıdır.
