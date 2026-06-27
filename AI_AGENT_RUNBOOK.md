# Yapay Zeka Ajanı Çalışma Kitabı (AI_AGENT_RUNBOOK.md)

Bu döküman, ERP platformundaki modülleri ve kodları geliştirecek olan yapay zeka ajanlarının (A1-A7) izlemesi gereken adım adım çalışma kılavuzudur. Ajanların bu adımları birebir uygulaması zorunludur.

---

## 🛠️ Ajanlar İçin Adım Adım Çalışma Planı

### Adım 1: Kuralları ve Standartları Okuyun
- Geliştirmeye başlamadan önce mutlaka aşağıdaki dosyaları okuyun ve kurallara uyun:
  1. **[ANAYASA.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/ANAYASA.md):** Kod kalitesi kuralları (DateTime UTC, Result Pattern, Async/Await vb.).
  2. **[ORTAK_TEKNIK_PROTOKOL.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/ORTAK_TEKNIK_PROTOKOL.md):** Git branching, dosya sınırları ve build kontrolleri.
  3. **[ENTITY_STANDARDLARI.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/ENTITY_STANDARDLARI.md):** BaseAuditableEntity, decimal hassasiyetleri ve sequence kod üretimi.
  4. **[API_STANDARDLARI.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/API_STANDARDLARI.md):** ApiResponse, Result sarmalama ve validation error formatları.

### Adım 2: Durumunuzu Güncelleyin (Stating Progress)
- Geliştirmeye başladığınızda, **[STATUS.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/STATUS.md)** dosyasında kendi Ajan ID'nize karşılık gelen satırdaki durumu **`IN_PROGRESS`** (Çalışıyor) olarak güncelleyin.
- Örnek: `| **A2** | Sales Manager | Ajan 2 | IN_PROGRESS |`

### Adım 3: Sadece Kendi Dizinlerinizde Çalışın (Isolate Edits)
- Conflict yaşamamak adına sadece size atanan Next.js dizinlerinde ve C# sınıflarında çalışın.
- Ortak dosyalarda (`DbContext` vb.) sadece kendi model kayıtlarınızı tek satır olarak ekleyin, mevcut kodları silmeyin veya değiştirmeyin.

### Adım 4: Veritabanı Migration'ını Koşturun
- Entity şemalarınızı oluşturduktan sonra veritabanı migration planındaki sıraya göre migration ekleme ve güncelleme komutlarını koşturun.

### Adım 5: xUnit Testlerini Yazın ve Koşturun
- Yazdığınız tüm business logic kurallarını denetleyen en az 5-8 adet birim testi yazın.
- `dotnet test` komutunun sıfır hata ile tamamlandığını doğrulayın.

### Adım 6: Projeyi Build Edin
- Kod teslimi öncesinde:
  - Backend tarafında: `dotnet build`
  - Frontend tarafında: `npm run build` ve `npm run lint`
  komutlarının hatasız geçtiğini kontrol edin.

### Adım 7: Rapor Hazırlayın ve Durumu Kapatın
- Geliştirme bittiğinde:
  - Kendi görev kartınızın (`GOREVLER/A*.md`) sonundaki kontrol listelerini tikleyin.
  - **[STATUS.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/STATUS.md)** dosyasındaki durumunuzu **`TAMAM`** olarak güncelleyin.
  - Yaptığınız değişiklikleri özetleyen kısa bir commit mesajı ile kodları yerel depoya commit edin.
