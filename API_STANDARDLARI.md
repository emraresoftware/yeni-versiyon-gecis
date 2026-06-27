# API Standartları (API_STANDARDLARI.md)

Bu döküman, C# backend API katmanında yazılacak olan Controller ve endpoint yanıtlarının standardını tanımlar. Ajanlar tüm API yanıtlarında bu formata uymak zorundadır.

---

## 📦 1. API Cevap Sarmalama (Response Wrapper)

Sistemde iki seviyeli bir cevap sarmalama yapısı mevcuttur:
1. **İş Katmanı Yanıtı (`Result<T>`):** Application katmanındaki Handler/Servis sınıfları hata fırlatmak (throw exception) yerine başarı/hata durumunu `Result<T>` (veya `Result`) nesnesi ile döner.
2. **API Katmanı Yanıtı (`ApiResponse<T>`):** Controller katmanı, `Result` nesnesini client'ın (React/Next.js) beklediği standart `ApiResponse` yapısına sarmalar.

### ApiResponse.cs (Global JSON Formatı)
Client'a dönen tüm başarılı ve başarısız yanıtlar aşağıdaki formatta olmalıdır:
```json
{
  "success": true,
  "data": { ... },
  "message": "İşlem başarıyla tamamlandı."
}
```

Hata durumunda:
```json
{
  "success": false,
  "data": null,
  "message": "Cari limit yetersiz."
}
```

---

## 🔀 2. HTTP Status Mapping Standardı

Controller sınıflarında `Result<T>` durumuna göre HTTP status kodları şu şekilde map edilmelidir:
- `Result.IsSuccess == true` ➔ **`200 OK`** veya **`201 Created`** (Yeni kayıt eklendiğinde)
- `Result.Error` tiplerine göre:
  - Kayıt bulunamadı (NotFound) ➔ **`404 Not Found`**
  - Yetkisiz işlem (Unauthorized/Forbidden) ➔ **`403 Forbidden`**
  - İş kuralı ihlali / Doğrulama hatası (Validation) ➔ **`400 Bad Request`**

---

## ❌ 3. Validasyon Hataları (Validation Error RFC-7807)

FluentValidation tarafından fırlatılan giriş parametresi doğrulama hataları, RFC-7807 (Problem Details) formatında sarmalanarak Bad Request olarak dönmelidir:

```json
{
  "success": false,
  "message": "Girdi doğrulama hatası oluştu.",
  "errors": {
    "Email": [
      "Geçersiz e-posta formatı.",
      "E-posta adresi boş geçilemez."
    ],
    "CreditLimit": [
      "Kredi limiti sıfırdan küçük olamaz."
    ]
  }
}
```

---

## 🔑 4. Kiracı Çözümleme (Tenant Resolution)
- **Claim Tabanlı Çözümleme:** API katmanında, istek yapan kullanıcının JWT token'ı içerisindeki `tenant_id` claim'i okunarak aktif tenant GUID değeri çözümlenir.
- **Güvenlik Filtresi:** Tenant ID bilgisi asla query parametresi veya body içerisinde client'tan alınmamalıdır. Her zaman HTTP Context user claims (`_tenantProvider.TenantId`) üzerinden güvenli bir şekilde alınmalıdır.
- **İzin Kontrolü:** Kiracı filtresini zorunlu kılmak için ilgili controller veya action metotlarının başına **`[RequireTenant]`** attribute'u konulmalıdır.
