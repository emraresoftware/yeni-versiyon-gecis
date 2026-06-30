# 📦 06_ERP_BLUEPRINT.md (ERP Entegrasyon Planı)

Bu kılavuz, kiracının SAP, Logo, Netsis gibi ERP sistemlerinin EAOS veri akışına nasıl bağlanacağını açıklar.

---

## 1. Ortak Veri Şemaları (Data Schema)
* **Ürün Sorgulama:** `ProductId`, `ProductName`, `StockQuantity`, `Price`, `Currency`.
* **Sipariş Gönderme:** `OrderId`, `CustomerId`, `Items` (List), `ShippingAddress`, `TotalAmount`.

---

## 2. Entegrasyon Kuralları
* ERP entegrasyonu doğrudan veritabanı yazma şeklinde olamaz. ERP'nin REST/SOAP API'leri veya güvenli ara tablolar (staging tables) kullanılmalıdır.
* ERP'den veri çeken ajan fonksiyonları **1500ms** timeout sınırı ile çalıştırılmalıdır.
