# Frontend Standartları (FRONTEND_STANDARDLARI.md)

Bu döküman, Next.js 16 (App Router) frontend katmanında geliştirilecek sayfaların, formların ve arayüz bileşenlerinin uyması gereken kodlama standartlarını tanımlar.

---

## 🔌 1. API İstemci Standardı (apiClient)

Tüm backend istekleri, `@/lib/api/client` altında tanımlanmış olan **`apiClient`** (axios wrapper) nesnesi kullanılarak yapılmalıdır.
- **Kural:** URL rotaları ve istek parametreleri hardcoded yazılmamalıdır. Her modül kendi API istek fonksiyonlarını `@/lib/api/` altındaki ilgili dosyada (Örn: `@/lib/api/crm.ts`) tanımlamalı ve dışa aktarmalıdır (export).
- **Hata Yönetimi:** İsteklerin hata durumları Axios interceptor'ları tarafından merkezi olarak yakalanır; ancak sayfa bazlı özel hatalar `catch` bloklarında ele alınmalıdır.

---

## 📝 2. Form Doğrulama (Zod & React Hook Form)

Frontend formlarında form durumu yönetimi için **React Hook Form**, şema doğrulama (validation) için ise **Zod** kütüphanesi kullanılacaktır.
- **Zod Şema Tanımı Örneği:**
  ```typescript
  import { z } from "zod"

  export const customerFormSchema = z.object({
    name: z.string().min(2, "Müşteri adı en az 2 karakter olmalıdır."),
    email: z.string().email("Geçersiz e-posta adresi."),
    creditLimit: z.preprocess((val) => Number(val), z.number().min(0, "Kredi limiti negatif olamaz.")),
  })
  ```

---

## 🔔 3. Bildirimler ve Toast Kullanımı (sweetAlert)
- İşlem sonuçlarında kullanıcıyı bilgilendirmek için proje standart kütüphanesi olan **`sweetAlert`** (`@/lib/sweetalert`) kullanılacaktır.
- **Kullanım:**
  - Başarılı işlemler: `sweetAlert.success("Kayıt başarıyla oluşturuldu.")`
  - Hatalı işlemler: `sweetAlert.error("Sunucu bağlantı hatası oluştu.")`

---

## 🔄 4. Arayüz Durum Tasarımları (States UI)

Her veri listeleme sayfasında şu 3 durum (state) tasarımı mutlaka kodlanmalıdır:
1. **Loading State:** Veri yüklenirken iskelet ekran (Skeleton loader) gösterilmelidir (Shadcn UI Skeleton component).
2. **Empty State:** Veri bulunmadığında kullanıcıyı yönlendirecek açıklayıcı bir grafik/ikon ve "Yeni Kayıt Ekle" butonu içeren boş ekran gösterilmelidir.
3. **Error State:** Yükleme başarısız olduğunda "Yeniden Dene" butonu içeren hata ekranı sunulmalıdır.

---

## 🎨 5. Tasarım Jetleri (UI Components & Tokens)
- **Renkler:** Sert düz renkler yerine CSS HSL renk değişkenleri (border-primary/10, text-muted-foreground vb.) kullanılmalıdır.
- **Modal Dialogs:** Sayfa yönlendirmesi gerektirmeyen küçük formlar için Shadcn UI `Dialog` bileşenleri tercih edilmelidir.
- **Kanban Görünümü:** Kart sürükle-bırak işlemleri için `@hello-pangea/dnd` veya hafif dnd paketleri kullanılmalıdır.
