# 🛠️ Ortak Teknik Protokol

Bu dosya, `yeni-versiyon-gecis` projesinde çalışan tüm yapay zeka ajanlarının ortak teknik çalışma kurallarını tanımlar.

Amaç; her ajanın aynı mimari, aynı kalite standardı ve aynı teslim protokolüyle çalışmasını sağlamaktır.

---

## 1. Aktif Branch

Tüm geliştirmeler yalnızca aşağıdaki branch üzerinde yapılacaktır:

```bash
gece-otonom
```

Kodlamaya başlamadan önce:

```bash
git checkout gece-otonom
git pull
```

---

## 2. Zorunlu Okuma Sırası

Her ajan kod yazmadan önce aşağıdaki dosyaları okumalıdır:

1. `ANAYASA.md`
2. `README.md`
3. `STATUS.md`
4. `REFERANSLAR.md`
5. Kendi görev dosyası:

   * `A1_CEO.md`
   * `A2_SALES.md`
   * `A3_FINANCE.md`
   * `A4_HR.md`
   * `A5_PRODUCTION.md`
   * `A6_QC.md`
   * `A7_LOGISTICS.md`

---

## 3. Çalışmaya Başlama Protokolü

Ajan çalışmaya başlamadan önce:

1. `STATUS.md` içinde kendi durumunu `IN_PROGRESS` yapar.
2. Kendi görev dosyasında çalışacağı maddeleri kontrol eder.
3. Bağımlı olduğu modüller varsa `BAGIMLILIK_HARITASI.md` dosyasını kontrol eder.
4. Kod yazmadan önce mevcut mimariyi bozmadan gerekli dosya yollarını tespit eder.

---

## 4. Dosya Değiştirme Sınırları

Her ajan öncelikle kendi modül alanında çalışmalıdır.

Örnek:

* A2 yalnızca CRM / Sales dosyalarında çalışır.
* A3 yalnızca Finance / Accounting dosyalarında çalışır.
* A6 yalnızca QC dosyalarında çalışır.
* A7 yalnızca Logistics dosyalarında çalışır.

Ortak dosyalar değiştirilecekse dikkat edilmelidir:

* DbContext
* Dependency Injection
* Shared DTO
* Result Pattern
* ApiResponse
* Layout / Navigation
* Route config
* Migration dosyaları

Ortak dosya değişikliği gerekiyorsa ilgili değişiklik açıklanmalıdır.

---

## 5. Clean Architecture Kuralı

Bağımlılık yönü daima içe doğrudur:

```text
Domain
  ↓
Application
  ↓
Infrastructure / Persistence
  ↓
API
```

Kurallar:

* `Domain` katmanı dış katmanlara bağımlı olamaz.
* Entity sınıfları business identity ve temel ilişki bilgisini taşır.
* İş kuralları mümkün olduğunca Application servislerinde veya domain servislerinde tutulur.
* API Controller doğrudan iş kuralı yazmaz.
* Controller yalnızca request alır, servis çağırır ve response döner.

---

## 6. Backend Kodlama Standardı

Backend tarafında zorunlu standartlar:

* `.NET 8`
* `async/await`
* Her async metoda `CancellationToken ct`
* EF Core sorgularında `ct` kullanımı
* `DateTime.UtcNow`
* `DateTimeKind.Utc`
* `Result<T>` / `Result`
* `ApiResponse<T>`
* FluentValidation
* xUnit testleri

Yasaklar:

```csharp
throw new Exception()
DateTime.Now
Task.Result
.Wait()
hardcoded tenant
hardcoded brand
```

---

## 7. Frontend Kodlama Standardı

Frontend tarafında zorunlu standartlar:

* Next.js 16
* TypeScript
* Responsive tasarım
* Dark mode uyumu
* Ortak API client kullanımı
* Form validation için tek standart
* Loading / empty / error state
* Toast veya kullanıcıya görünür hata mesajı

Rota standardı:

```text
/control-tower/...
```

Yasak rota:

```text
/elyaf/...
```

---

## 8. White-Labeling Kuralı

Kod içinde marka ismi sabit yazılmayacaktır.

Backend:

```csharp
Environment.GetEnvironmentVariable("CONTROL_TOWER_TENANT_SLUG") ?? "elyaf-group"
```

Frontend:

```ts
process.env.NEXT_PUBLIC_CONTROL_TOWER_TENANT_SLUG || "elyaf-group"
process.env.NEXT_PUBLIC_BRAND_NAME
```

Not: Varsayılan değer yalnızca fallback olarak kullanılabilir. UI ve iş mantığı marka bağımsız olmalıdır.

---

## 9. Migration Protokolü

Her yeni entity için:

1. Entity oluşturulur.
2. DbContext içine `DbSet` eklenir.
3. Entity configuration varsa eklenir.
4. Migration oluşturulur.
5. Migration adı anlamlı verilir.

Örnek:

```bash
dotnet ef migrations add AddCrmModule
dotnet ef database update
```

Migration dosyaları kontrol edilmeden commit atılmaz.

---

## 10. Test Protokolü

Her ajan kendi modülü için test yazmak zorundadır.

Minimum test sayıları görev dosyalarında belirtilmiştir.

Genel test alanları:

* Validation testleri
* Business rule testleri
* Tenant isolation testleri
* DateTime UTC testleri
* Create / Update / List senaryoları
* Hatalı veri senaryoları

Backend doğrulama:

```bash
dotnet build
dotnet test
```

Frontend doğrulama:

```bash
cd web
npm run build
npm run lint
```

---

## 11. Commit Protokolü

Commit mesajları açık ve modül bazlı olmalıdır.

Örnekler:

```bash
feat(crm): add account and proposal entities
feat(finance): add journal entry balancing validation
fix(logistics): prevent transfer completion with insufficient stock
docs(agent): update A2 sales checklist
```

---

## 12. Kapanış Protokolü

Ajan işi bitirdiğinde:

1. Kendi görev dosyasındaki maddeleri `[x]` yapar.
2. `STATUS.md` içinde durumunu `TAMAM` yapar.
3. Yapılan işleri kısa özetler.
4. Test/build sonucunu yazar.
5. Eksik kalan veya sonraki ajana devreden konu varsa açıkça belirtir.

---

## 13. Sıfır Hata İlkesi

Bir ajan teslim yapmadan önce aşağıdakileri doğrulamalıdır:

* Backend build başarılı
* Backend test başarılı
* Frontend build başarılı
* Frontend lint başarılı
* Migration çalışıyor
* DateTime UTC kuralı ihlal edilmemiş
* Hardcoded tenant/brand yok
* Result Pattern kullanılmış
* Controller içinde business logic yok
* API response standardı korunmuş

---

## 14. Temel İlke

Bu proje yalnızca modül ekleme çalışması değildir.

Amaç, klasik ERP ekranları yerine olay tabanlı, AI destekli ve modüler bir Business Operating System altyapısı oluşturmaktır.

Bu yüzden her ajan yalnızca kendi görevini değil, bütün sistemin sürdürülebilirliğini de korumakla yükümlüdür.
