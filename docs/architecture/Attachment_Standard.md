# 📎 Attachment Standard

**Title:** Attachment Standard  
**Version:** 1.0.0  
**Status:** Approved / Freeze  
**Owner:** Architecture Board  
**Last Updated:** 2026-07-10  
**Dependencies:** DOMAIN_MODEL.md  

---

Bu doküman, Omnichannel Messaging Core (OMC) üzerinden gönderilen veya alınan tüm eklentilerin (attachments: resim, video, pdf, ses vb.) saklama, güvenlik, tarama ve yaşam döngüsü kurallarını tanımlar.

## Eklenti Güvenliği ve Doğrulama (Ingress Rules)

### 1. MIME ve Uzantı Doğrulaması (Mime Validation)
* Dosya tipi kontrolü sadece dosya uzantısına (.png, .pdf vb.) göre yapılmaz.
* Sunucu tarafında dosyanın ilk byte'ları okuma (Magic Number Signature Validation) tekniği ile doğrulanır.
* Desteklenen güvenli dosya tipleri:
  * **Resim:** `image/png`, `image/jpeg`, `image/gif`, `image/webp`
  * **Döküman:** `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document` (docx), `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` (xlsx), `text/plain`
  * **Ses:** `audio/mpeg` (mp3), `audio/ogg`, `audio/wav`, `audio/webm`, `audio/aac`
  * **Video:** `video/mp4`, `video/mpeg`, `video/webm`
* Çalıştırılabilir (.exe, .bat, .sh) veya sıkıştırılmış arşiv (.zip, .rar - şifreli ise taranamadığı için) dosyaları varsayılan olarak **engellenir**.

### 2. Boyut Sınırları (Max Size Limits)
* **Kanal Limitleri (Örn. WhatsApp API):** WhatsApp resim/ses için 16 MB, dökümanlar için 100 MB limit uygular.
* **Genel Sistem Limiti:** Güvenlik ve bant genişliği koruması amacıyla, sistem üzerinden gönderilebilecek veya alınabilecek tekil maksimum dosya boyutu **50 MB** ile sınırlandırılmıştır.

### 3. Virüs Tarama Protokolü (Virus Scan)
* Müşteriden gelen veya sisteme yüklenen her eklenti nesne deposuna (Object Storage) yüklenirken geçici bir alana (`/tmp/scanning/...`) alınır.
* Arka planda ClamAV veya bulut sağlayıcının tarama API'si (Örn. Google Cloud Web Security Scanner / Event-driven scanning) tetiklenir.
* Tarama bitene kadar eklenti veri tabanındaki durum `Scanning` olarak kalır. UI tarafında dosya yerine "Virüs Taraması Yapılıyor..." ibaresi gösterilir.
* Dosya temiz ise durum `Clean` yapılır ve erişime açılır. Enfekte ise durum `Infected` yapılarak dosya kalıcı olarak silinir ve sistem güvenlik olayı (`SecurityAuditLog`) kaydedilir.

---

## Depolama ve Erişim Stratejisi (Storage Standard)

### 1. Nesne Depolama (Object Storage)
* Eklentiler uygulama sunucularının yerel diskinde saklanmaz. S3 uyumlu veya Google Cloud Storage (GCS) gibi yatay ölçeklenebilir nesne depoları kullanılır.
* **Nesne Path Formatı:**
  `tenants/{tenantId}/attachments/{year}/{month}/{day}/{attachmentId}_{originalFilename}`
* Dosya isimleri doğrudan kullanılmaz; URL injection ve path traversal saldırılarını önlemek için dosya ismi URL encoding'den geçirilir ve önüne `attachmentId` (Guid) eklenir.

### 2. Thumbnail & Preview Üretimi
* Yüklenen her büyük resim dosyası için arka plan işleyicisi (Background Job) tarafından otomatik olarak küçük önizleme resmi (thumbnail - maks 200px genişlik) ve orta boy resim (preview - maks 800px genişlik) üretilir.
* Thumbnail dosyası `{original_filename}_thumb.webp` ismiyle kaydedilir. UI ekranlarında liste yüklenirken sadece thumbnail çekilir, bu da performansı optimize eder.
* PDF dökümanlarının ilk sayfası otomatik olarak resme dönüştürülerek önizleme dosyası üretilir.

---

## Saklama ve Silme Politikası (Retention Policy)

| Eklenti Kategorisi | Saklama Süresi (Retention) | Süre Sonu Aksiyonu |
|---|---|---|
| **Genel Sohbet Eklentileri** | 1 Yıl (365 Gün) | Arşiv/Cold Storage'a taşıma veya kalıcı silme. |
| **CRM Fırsat/Cari Kartına Bağlı Dosyalar** | Sınırsız (Cari aktif olduğu sürece) | Silinmez. |
| **Soft Deleted Mesaj Eklentileri** | 14 Gün | Nesne deposundan ve veri tabanından fiziksel silme (Hard Delete). |
| **Enfekte (Infected) Eklentiler** | 0 Gün | Derhal silme ve karantinaya alma. |

---

## Veritabanı Modeli (Attachment Metadata)

```csharp
public class MessageAttachment : BaseEntity, ITenantEntity
{
    public Guid Id { get; set; }
    public Guid? TenantId { get; set; }
    public Guid MessageId { get; set; }
    public string Filename { get; set; } = string.Empty;
    public string MimeType { get; set; } = string.Empty;
    public long FileSize { get; set; } // Bytes
    public string StorageKey { get; set; } = string.Empty; // Object storage path
    public string AttachmentUrl { get; set; } = string.Empty; // Public secure CDN/Proxy URL
    public string? Checksum { get; set; } // SHA-256 hash of file
    public AttachmentScanStatus ScanStatus { get; set; } = AttachmentScanStatus.Scanning;

    public ConversationMessage Message { get; set; } = null!;
}
```
Dosya erişimi doğrudan dosya linkiyle verilmez; yetkilendirme kontrolü sağlayan bir proxy endpoint'i (`GET /api/v1/attachments/{id}`) veya süreli güvenli linkler (Signed URLs - 15 dk geçerli) aracılığıyla sunulur.
