# 🔌 API_CONSTITUTION.md (EAOS API ve Haberleşme Anayasası)

Bu anayasa, EAOS servislerinin iç ve dış dünya ile kurduğu tüm uygulama programlama arayüzlerinin (API) standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde I.4 ve Madde IV.2'ye doğrudan bağlıdır.

---

## 1. API Protokol Standartları
* **REST (Public & Web client):** JSON tabanlı, HTTP fiillerine (GET, POST, PUT, DELETE) tam uyumlu ve RESTful kurallarına göre tasarlanmış dışa açık API'ler.
* **gRPC (Internal Microservices):** Mikroservisler arası yüksek hızlı veri transferlerinde Protobuf formatında zorunlu gRPC kullanımı.
* **WebSockets (Realtime streams):** Webchat widget sohbet akışları, mobil asistan ses alışverişi ve Unity bildirimleri için WSS standardı.

---

## 2. Versioning (Sürümleme) ve OpenAPI
* **Sürümleme:** REST API uç noktaları URL seviyesinde sürümlenmelidir (Örn: `/api/v1/customers`, `/api/v2/customers`).
* **Dokümantasyon:** Her API ucu için Swagger / OpenAPI şemaları otomatik olarak üretilmeli, parametre tipleri ve hata kodları şemada tam tanımlanmalıdır.

---

## 3. Rate Limit (İstek Sınırlandırma)
* Kötü niyetli kullanımı (DDoS) ve aşırı kaynak tüketimini önlemek için her uç noktaya IP ve Token bazlı Rate Limiting uygulanır.
* Standart kullanıcı sınırları: IP başına dakikada en fazla 60 istek, API anahtarları için kiracı paket limitlerine göre dinamik sınırlar.

---

## 4. Deprecation (Eski Sürümleri Devre Dışı Bırakma)
* Eski bir API ucu kapatılmadan önce:
  1. API yanıt başlığında `Warning: 299 - "Deprecated API"` dönülmelidir.
  2. Entegratörlere ve kiracılara en az 6 ay önceden e-posta / panel bildirimi gönderilmelidir.
  3. API tamamen kapatıldığında `410 Gone` hata kodu verilmelidir.
