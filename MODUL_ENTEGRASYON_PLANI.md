# Modül Entegrasyon Planı (MODUL_ENTEGRASYON_PLANI.md)

Bu döküman, bağımsız gibi duran CRM, Finans, Lojistik, Kalite ve İK modüllerinin ERP bütünlüğünü oluşturabilmesi için kod seviyesinde nasıl entegre edileceğini açıklar.

---

## ⚡ 1. Entegrasyon Senaryoları ve Tetikleyiciler (Triggers)

### Senaryo A: Teklif Onaylandığında Muhasebe ve Fatura Entegrasyonu (CRM ➔ Finance)
- **Tetikleyici Event:** A2 CRM modülünde bir Teklifin (`CrmProposal`) durumu `Approved` (Onaylandı) yapıldığında bir domain event (`CrmProposalApprovedEvent`) fırlatılır.
- **Entegrasyon Handler'ı:** A3 Finans modülündeki handler bu eventi yakalar:
  1. Müşterinin cari hesabına (`FinanceAccountPlan` 120 alıcılar hesabı) borç kaydeder.
  2. Gelir hesabına (`FinanceAccountPlan` 600 yurt içi satışlar hesabı) alacak kaydeder.
  3. KDV hesabına (`FinanceAccountPlan` 391 hesaplanan KDV) alacak kaydeder.
  4. Toplam Borç = Toplam Alacak olacak şekilde otomatik bir `FinanceJournalEntry` fişi oluşturur ve kaydeder.

### Senaryo B: Sipariş Alındığında ve Sevkiyat Yapıldığında Stok Entegrasyonu (CRM ➔ Logistics)
- **Tetikleyici Event:** A2 CRM tarafında faturalandırılan bir sipariş sevk edilmeye hazır olduğunda:
  1. A7 Lojistik modülündeki `LogisticsStockMovement` tablosuna ilgili `ProductCode` için `MovementType = "Out"` (Çıkış) yönünde stok hareket kaydı atılır.
  2. İlgili deponun güncel stok miktarı güncellenir.

### Senaryo C: Üretim Tamamlandığında Stok ve Kalite Kontrol Entegrasyonu (Production ➔ Logistics ➔ QC)
- **Tetikleyici Event:** A5 Üretim modülünde bir üretim emri (Batch) tamamlandığında:
  1. A7 Lojistik tarafına `MovementType = "In"` (Giriş) yönünde üretilen lot/batch numarası ile stok hareket kaydı atılır.
  2. A6 Kalite Kontrol modülü için otomatik bir kalite test formu (`QcTestResult`) oluşturulur ve durumu `Pending` olarak kalite departmanına iletilir.
  3. Ürün kalite testi onaylanmadan (`Result == "Pass"`), lojistik departmanı bu lot/batch ürünün sevk edilmesine izin vermez.

### Senaryo D: Maaş Tahakkuku ve Muhasebe Entegrasyonu (HR ➔ Finance)
- **Tetikleyici Event:** A4 İK modülünde aylık puantajlar kapatılıp maaş tahakkuk ettirildiğinde:
  1. Personel borç/alacak hesapları üzerinden A3 Muhasebe modülünde yevmiye fişi (`YV-`) otomatik olarak oluşturulur (Örn: 770 Genel Yönetim Giderleri borçlu, 335 Personele Borçlar alacaklı).

---

## 🛠️ 2. Kod Seviyesinde İletişim Standartları (Service DI vs MediatR)

Ajanlar modüller arası entegrasyonu sağlarken şu iki yöntemden birini kullanmalıdır:
1. **MediatR Domain Events (Tercih Edilen - Loose Coupling):**
   - Modüllerin birbirine sıkı sıkıya bağlanmasını önlemek için bir event fırlatılır (`_mediator.Publish(new ProposalApprovedEvent(proposalId))`). Diğer modül bu eventi `INotificationHandler` ile yakalayıp kendi işlemlerini yürütür.
2. **Interface Servis Enjeksiyonu (Direct Calls):**
   - Senkron ve anlık kontrol gerektiren yerlerde (Örn: Stok bakiye kontrolü), ilgili modülün servis interface'i enjekte edilerek çağrılır (Örn: `ILogisticsStockService.GetAvailableStock(productCode, warehouseId)`).
