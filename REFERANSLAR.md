# 📚 Yerel Kod Referansları ve Hazır Kaynaklar Haritası (REFERANSLAR.md)

Bu dosya, yeni ERP/CRM modüllerini geliştiren yapay zeka ajanlarının (A1-A7), yerel bilgisayardaki mevcut projelerden ve hazır kodlardan nasıl referans alacağını göstermektedir. Sıfırdan kod yazarken buradaki veri yapıları ve iş mantıkları (business logic) rehber alınmalıdır.

---

## 📂 Rol Bazlı Kaynak Eşleşmeleri

### 1. CEO & Stratejik Kararlar (A1)
* **`emare ai cevap`** (`/Users/emre/emare ai cevap`)
  * **İçerik:** AI destekli e-posta ve ticket cevap taslakları oluşturma motoru.
  * **Kullanım:** CEO'nun karar alma ve otonom cevap/özetleme akışlarında LLM komutları (prompts) ve servis entegrasyonu referans alınabilir.
* **`Emare Analiz`** (`/Users/emre/Emare Analiz`)
  * **İçerik:** Raporlama ve analitik veri yapısı.

### 2. Müşteriler, Fırsatlar & Satış (A2)
* **`emare-crm`** (`/Users/emre/Dergah/Emare projeler/emarerp/emare-crm`)
  * **İçerik:** Laravel tabanlı eksiksiz CRM veritabanı şeması ve arayüz yapısı.
  * **Kullanım:** Fırsatlar (`Opportunity`), Müşteri Segmentleri (`CustomerSegment`) ve Teklifler (`Quote`) modelleri ve ilişkileri bu projeden kopyalanarak .NET'e uyarlanacaktır.
* **`lead`** (`/Users/emre/lead`)
  * **İçerik:** Google Maps ve web tarama üzerinden otomatik müşteri datası toplayan lead scraper araçları.
* **`Kampanya`** (`/Users/emre/Kampanya`)
  * **İçerik:** Pazarlama kampanyaları ve müşteri toplu erişim senaryoları.

### 3. Genel Muhasebe, Kasa, Banka & Fatura (A3)
* **`Emare Finance`** (`/Users/emre/Dergah/Emare projeler/Emare Finance`)
  * **İçerik:** Tek düzen hesap planı (`AccountPlan`), yevmiye fişleri (`JournalEntry`), banka entegrasyonu (`BankReconciliation`) ve amortisman tabloları.
  * **Kullanım:** Borç/Alacak balance hesaplama algoritmaları ve hiyerarşik hesap ağacı SQL yapısı doğrudan buradan C# katmanına taşınmalıdır.
* **`Emare odeme`** (`/Users/emre/Emare odeme`)
  * **İçerik:** Kredi kartı/sanal POS tahsilat ve ödeme entegrasyon modülleri.

### 4. Personel, İzin & İK Yönetimi (A4)
* **`Emare Task` & `emare-is-havuzu`** (`/Users/emre/Emare Task` / `/Users/emre/emare-is-havuzu`)
  * **İçerik:** Şirket içi görev havuzu, çalışma saatleri ve performans takipleri.
  * **Kullanım:** İK organizasyon şemaları ve personel kartları ile entegre edilecektir.

### 5. Üretim, İmalat & Santral Entegrasyonu (A5)
* **`Emare Finance` (MRP & BOM Modülü)**
  * **İçerik:** Reçete (`Bom`), reçete detayları (`BomLine`) ve iş merkezleri (`Workstation`).
  * **Kullanım:** Reçete birim maliyeti hesaplama logic'i (`unitCost()`) referans alınmalıdır.
* **`Emare voice` & `emarecallcenter`** (`/Users/emre/Emare voice` / `/Users/emre/emarecallcenter`)
  * **İçerik:** Asterisk entegrasyonu, STT (Speech-to-Text) ve TTS (Text-to-Speech) ses köprüleri.

### 6. Kalite Kontrol (A6)
* **`Emare Finance` (QC & İade Modülleri)**
  * **İçerik:** Ürün kalite standart tanımları, hata kategorileri ve müşteri tazminat talepleri.

### 7. Lojistik & Sevkiyat (A7)
* **`Emare Finance` (Stok & Sevkiyat)**
  * **İçerik:** Stok hareketleri (`StockMovement`), depolar arası transferler (`StockTransfer`) ve teslimat formları (`GoodsReceipt`).
  * **Kullanım:** FIFO/LIFO stok maliyet yöntemleri ve depo transfer onay akışları rehber alınmalıdır.

---

## ⚠️ Ajanlar İçin Önemli Uyarı
Bu projelerdeki kodlar doğrudan **kopyala-yapıştır yapılamaz**. Sadece veritabanı tablolarının alanları (database schemas), veri türleri ve iş kurallarının (business logic) .NET 8 ve React tarafında sıfırdan temiz bir şekilde kodlanması için referans olarak kullanılacaktır.
