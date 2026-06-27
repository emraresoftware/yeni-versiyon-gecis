# 🚀 Emare AI Dashboard — Yeni Versiyon Geçişi Ajan Kılavuzu

Bu klasör, **Emare AI Dashboard** projesinin Odoo bağımlılıklarından arındırılarak özelleştirilmiş ERP/CRM modüllerine geçiş sürecini (V3 Aşama C) yöneten 7 yapay zeka ajanı için ortak koordinasyon merkezidir.

---

## 👥 Ajan Rol Dağılımı ve Görev Alanları

Sistemde eşzamanlı veya ardışık çalışan 7 ajan bulunmaktadır:

| Ajan ID | Ajan Rolü / Departman | Görev Kartı Dosyası |
|---------|-----------------------|---------------------|
| **A1**  | CEO / Executive       | `GOREVLER/A1_CEO.md` |
| **A2**  | Sales Manager         | `GOREVLER/A2_SALES.md` |
| **A3**  | Finance Manager       | `GOREVLER/A3_FINANCE.md` |
| **A4**  | HR & Admin            | `GOREVLER/A4_HR.md` |
| **A5**  | Production / Imalat   | `GOREVLER/A5_PRODUCTION.md` |
| **A6**  | QC (Quality Control)  | `GOREVLER/A6_QC.md` |
| **A7**  | Logistics / Sevkiyat  | `GOREVLER/A7_LOGISTICS.md` |

---

## 🛠️ Çalışma Kuralları ve Protokoller

### 1. Aktif Branch ve Kod Güncelleme
- Tüm geliştirmeler **`gece-otonom`** branch'inde yapılmalıdır.
- Kod üzerinde değişiklik yapmadan önce daima yerel deponuzu güncelleyin (`git pull`).
- Geliştirme sonrasında kodların derlendiğini doğrulamak için hem backend testlerini çalıştırın hem de frontend build alın:
  ```bash
  # Backend
  dotnet build && dotnet test
  # Frontend
  cd web && npm run build
  ```

### 2. Canlıya Alım (Deployment) Adımları
Değişiklikleri Git deposuna gönderdikten sonra staging sunucularını tetikleyin:
```bash
git add .
git commit -m "feat/fix: aciklama"
git push emaredestek gece-otonom

# Staging (31.169.72.85) sunucusunda derlemeyi başlatmak için lokalden:
ssh -o StrictHostKeyChecking=no ticket@31.169.72.85 "/home/ticket/sync_deploy.sh 31.169.72.85 gece-otonom"
```

### 3. Görev Güncelleme ve Kapanış
- Her ajan çalışmaya başladığında `STATUS.md` dosyasındaki durumunu `IN_PROGRESS` yapar.
- Kendi rol dosyasındaki (`GOREVLER/A*_*.md`) görev maddelerini tamamlandıkça `[x]` ile işaretler.
- Tüm görevler tamamlandığında ve derleme testleri başarılı olduğunda durumunu `TAMAM` olarak günceller.

### 4. Yazılım Standartları (Anayasa)
- Her geliştirici ajan, kod yazmaya başlamadan önce **[ANAYASA.md](./ANAYASA.md)** dosyasını okumak ve kurallara istisnasız uymak zorundadır.
- PostgreSQL DateTime UTC zorunluluğuna ve dinamik kiracı (White-Labeling) standartlarına özellikle dikkat edilmelidir.

### 5. Mimari Standartlar ve Entegrasyon Dokümanları
Sürecin ERP bütünlüğü içinde yürütülmesi için aşağıdaki 10 mimari ve standart dokümanı mutlaka rehber alınmalıdır:
1. **[ORTAK_TEKNIK_PROTOKOL.md](./ORTAK_TEKNIK_PROTOKOL.md):** Git branching, dosya sınırları ve build kontrolleri.
2. **[BAGIMLILIK_HARITASI.md](./BAGIMLILIK_HARITASI.md):** Modüller arası veri akışı ve ajan ilişkileri.
3. **[ENTITY_STANDARDLARI.md](./ENTITY_STANDARDLARI.md):** BaseAuditableEntity, decimal para tipleri, enum dönüşümleri ve merkezi numara üretimi.
4. **[API_STANDARDLARI.md](./API_STANDARDLARI.md):** `Result<T>`, `ApiResponse<T>`, RFC-7807 validasyon hataları ve JWT tenant claims çözümleme.
5. **[FRONTEND_STANDARDLARI.md](./FRONTEND_STANDARDLARI.md):** API istemci metodları, Zod form doğrulamaları ve UI Loading/Empty durum tasarımları.
6. **[TEST_STRATEJISI.md](./TEST_STRATEJISI.md):** xUnit, FluentAssertions, `DateTimeKind.Utc` assert kuralları ve multi-tenant veri izolasyon testleri.
7. **[VERITABANI_MIGRATION_PLANI.md](./VERITABANI_MIGRATION_PLANI.md):** EF Core Migration sıralaması (CRM -> Finance -> Logistics -> QC -> HR -> CEO).
8. **[MODUL_ENTEGRASYON_PLANI.md](./MODUL_ENTEGRASYON_PLANI.md):** MediatR Domain Event'ler ile gevşek bağlı (loose-coupled) entegrasyon senaryoları.
9. **[SECURITY_AUTHORIZATION.md](./SECURITY_AUTHORIZATION.md):** Rol bazlı erişim denetimi (RBAC) matrisleri ve `[RequireTenant]` denetimleri.
10. **[AI_AGENT_RUNBOOK.md](./AI_AGENT_RUNBOOK.md):** Kodlamayı üstlenecek yapay zeka ajanları için adım adım çalışma ve teslimat kılavuzu.

### 6. Mevcut Projeler ve Referans Kodlar (Hazır Kaynaklar)
- Geliştiriciler, kodları sıfırdan yazarken yerel bilgisayardaki mevcut projelerden ve iş kurallarından yararlanmalıdır. Detaylı eşleşme tablosu için **[REFERANSLAR.md](./REFERANSLAR.md)** dosyasını inceleyin.

