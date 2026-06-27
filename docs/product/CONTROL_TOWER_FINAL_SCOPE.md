# 🏰 Elyaf Group 2.0 — Control Tower Final Scope

**Versiyon:** 1.1.0  
**Durum:** Draft — Onay Bekliyor  
**Sahip:** Product Board  
**Son Güncelleme:** 2026-06-27  
**Bağımlı Dokümanlar:** DOMAIN_MODEL.md, BOUNDED_CONTEXTS.md, UBIQUITOUS_LANGUAGE.md, SECURITY_AUTHORIZATION.md, EVENT_BUS.md

---

## Amaç

Bu doküman, Elyaf Group 2.0 platformunun **final ürün kapsamını** tanımlar.  
Her Control Tower ekranının menü yapısını, KPI'larını, bileşenlerini, backend gereksinimlerini ve entity adaylarını içerir.  
Bu doküman tamamlanmadan CRM/Sales sprint çalışmaları başlatılmaz.

---

## Genel Control Tower Arayüz Mimarisi

Her Control Tower aşağıdaki standart bileşen alanlarından oluşur:

| Bölge | Açıklama |
|-------|----------|
| **Executive Snapshot** | Günlük/haftalık özet KPI kutuları — en üst satır |
| **KPI Kartları** | Sayısal ve trend göstergeli metrik kartlar |
| **Today's Priorities** | Bugün aksiyon gerektiren konular listesi |
| **Critical Alerts** | Sistem veya iş kritikliği olan uyarılar |
| **Notifications** | Rol tabanlı bildirimler |
| **Risk / Health Score** | Departman veya süreç sağlık skoru |
| **Customer / Supplier / Department Panel** | İlgili cari/tedarikçi/departman listesi ve durumları |
| **Message Drafts** | Gönderilmeyi bekleyen onaylı mesaj taslakları |
| **Calendar & Key Events** | Yaklaşan toplantılar, teslim tarihleri, kritik günler |
| **Next 7 Days Focus** | Önümüzdeki 7 günün öne çıkan iş maddeleri |
| **Reports & Analytics** | Hızlı rapor bağlantıları ve mini analiz alanı |

---

## Visual Acceptance Criteria

Müşterinin paylaştığı Control Tower görselleri final ürün için görsel kabul kriteridir. Her Control Tower için aşağıdakiler zorunlu kabul edilecek:

* **Sol dikey menü:** İlgili Control Tower'a özel modül alt menüleri ve genel geçiş bağlantıları.
* **Üst KPI kart satırı:** En az 4 adet, trend yönü (yeşil/kırmızı ok) ve periyot karşılaştırması içeren metrik kartı.
* **Executive Snapshot paneli:** Üst düzey özet metinler veya kritik durum grafikleri.
* **Today’s Priorities paneli:** Bugün yapılması gereken acil işlerin (onaylar, takipler vb.) listelendiği aksiyon paneli.
* **Critical Alerts paneli:** Eşik aşımı durumlarında (gecikme, limit aşımı vb.) tetiklenen kırmızı alarm göstergeleri.
* **Notifications paneli:** Kullanıcı rolüne özel anlık sistem bildirimleri.
* **Health / Risk Score kartı:** Sürecin veya departmanın genel sağlık durumunu (1-100 veya A-F) gösteren görsel widget.
* **Customer / Supplier / Department paneli:** İlgili dış ve iç paydaşların performans ve durum izleme tablosu.
* **Message Drafts alanı:** Hızlı iletişim için şablonlanmış ve onay bekleyen hazır mesaj taslakları.
* **Calendar & Key Events alanı:** Kritik teslim günleri, denetimler, toplantılar ve kilit tarihleri içeren takvim.
* **Next 7 Days Focus alanı:** Gelecek 7 günün hedefleri ve odak noktalarının listelendiği alan.
* **Reports & Analytics bağlantıları:** Modüle ait detaylı analitik raporlara hızlı geçiş menüsü.
* **Rol bazlı kullanıcı/profil alanı:** Aktif kullanıcının kimlik ve rol (Persona) bilgilerinin gösterildiği profil alanı.
* **Export / Filter / Date controls:** CSV/Excel export, dinamik filtreleme ve tarih aralığı seçicileri.
* **Legend / status açıklamaları:** Tablolarda ve grafiklerde kullanılan durum renklerinin ve sembollerinin açıklamaları.

---

## 1. CEO Control Tower

### Menü Başlıkları
- Executive Overview
- Strategic Decisions
- Company Health Score
- Department Scorecards
- Budget vs Actuals
- Key Risk Indicators
- Board Reports

### KPI Kartları
- Aylık Ciro (Gerçek vs Hedef)
- EBITDA Marjı (%)
- Aktif Müşteri Sayısı
- Toplam Alacak / Borç
- Sipariş Backlog Değeri
- Personel Sayısı
- Üretim Verimliliği (%)
- Kalite Red Oranı (%)
- Net Promoter Score (NPS)
- Nakit Pozisyonu

### Executive Snapshot
- Şirket geneli günlük özet
- En kritik 3 departman uyarısı
- Bugün alınması gereken kararlar
- Bu hafta tamamlanan satışlar
- Risk skoru (1–100)

### Today's Priorities
- Onay bekleyen kararlar (DecisionLog)
- Kritik geciken faturalar
- Cevap bekleyen müşteri eskalasyonları
- Günlük kur ve nakit pozisyon özeti

### Critical Alerts
- Nakit açığı eşik uyarısı
- Geciken üretim emirleri
- Müşteri şikayeti eskalasyonu
- Tedarikçi ödeme riski

### Notifications
- Departman yöneticisi bildirimleri
- Onay bekleyen belgeler
- Otomatik rapor hazır bildirimleri

### Risk / Health Score
- Finansal Sağlık Skoru
- Operasyonel Risk Skoru
- Müşteri Memnuniyet Skoru
- Tedarik Zinciri Risk Skoru

### Customer / Supplier / Department Panels
- Top 10 Müşteri (ciro bazlı)
- Top 5 Tedarikçi (risk bazlı)
- Departman Scorecard Özeti

### Message Drafts
- CEO imzasını bekleyen yazışmalar
- Yönetim kurulu duyuru taslakları

### Calendar & Key Events
- Yönetim kurulu toplantıları
- Audit/denetim tarihleri
- Fuar ve etkinlikler
- Kilit müşteri ziyaretleri

### Next 7 Days Focus
- Kritik toplantılar
- Bütçe kapanış tarihleri
- Departman raporlama son günleri

### Reports & Analytics
- P&L Özeti
- Cash Flow Raporu
- Departman Performans Özeti
- Yönetim Kurulu Sunusu

### Gerekli Backend Modülleri
- FinanceModule (P&L, Cash Flow)
- SalesModule (Ciro, Backlog)
- HRModule (Personel)
- ProductionModule (Verimlilik)
- QCModule (Red Oranı)
- CRMModule (Müşteri, NPS)
- ReportingModule (Tüm özet raporlar)

### Gerekli Entity Adayları
- `DecisionLog` (Karar defteri)
- `CompanyHealthScore` (Hesaplanmış skor — view/materialized)
- `ExecutiveDashboardSnapshot` (Günlük özet kaydı)
- `BudgetTarget` (Hedef değerler)

### Gerekli Workflow / Event / Permission Adayları
- `CeoDecisionLogCreated`, `CeoDecisionLogApproved`
- Permission: `CEO.ControlTower.View`, `CEO.DecisionLog.Approve`
- Workflow: KPI Özeti Hesaplama (scheduled), Eskalasyon Tetikleme

---

## 2. Sales Control Tower

### Menü Başlıkları
- Sales Overview
- Opportunities Pipeline
- Proposals & Quotes
- Sales Orders
- Customer Accounts
- Targets & Performance
- Sales Reports

### KPI Kartları
- Aylık Satış Cirosu (Gerçek vs Hedef)
- Aktif Fırsat Sayısı ve Toplam Değeri
- Win Rate (%)
- Ortalama Kapanış Süresi (gün)
- Teklife Dönüşüm Oranı
- Aktif Sipariş Sayısı
- Yeni Müşteri Sayısı (Ay)
- Kayıp Fırsat Değeri

### Executive Snapshot
- Bu ay kazanılan satışlar
- Kapanmak üzere olan fırsatlar (bu hafta)
- Yüksek değerli teklifler
- Son 7 gün yeni müşteri

### Today's Priorities
- Bugün takip edilmesi gereken fırsatlar
- Yanıt bekleyen teklifler
- Geciken sipariş onayları
- Teklif son tarihleri

### Critical Alerts
- Teklif geçerlilik tarihi yaklaşan teklifler
- Uzun süredir güncellenmemiş fırsatlar
- Müşteri hesabı limitini aşan siparişler

### Notifications
- Yeni fırsat atandı
- Teklif onaylandı / reddedildi
- Sipariş oluşturuldu

### Risk / Health Score
- Pipeline Sağlık Skoru
- Müşteri Çeşitlilik Skoru (HHI bazlı)

### Customer / Supplier / Department Panels
- Müşteri Listesi (segment, durum, son işlem tarihi)
- Satış Temsilcisi Performans Paneli

### Message Drafts
- Müşteriye gönderilecek teklif e-postaları
- Takip mesajı taslakları

### Calendar & Key Events
- Müşteri ziyaretleri
- Teklif son günleri
- Fuar / etkinlik tarihleri

### Next 7 Days Focus
- Kapanması beklenen fırsatlar
- Bekleyen teklif gönderimleri
- Yeni müşteri randevuları

### Reports & Analytics
- Pipeline Raporu (Funnel)
- Satışçı Performans Raporu
- Ürün Bazlı Satış Analizi
- Müşteri Segment Analizi

### Gerekli Backend Modülleri
- CRMModule (CrmAccount, CrmContact, CrmOpportunity)
- SalesModule (SalesOrder, CrmProposal)
- ReportingModule

### Gerekli Entity Adayları
- `CrmAccount`, `CrmContact`, `CrmOpportunity`
- `CrmProposal`, `CrmProposalItem`
- `SalesOrder`, `SalesOrderItem`
- `SalesTarget` (Aylık/Yıllık hedefler)
- `SalesActivityLog` (Aktivite takibi)

### Gerekli Workflow / Event / Permission Adayları
- `CrmOpportunityCreated`, `CrmProposalCreated`, `CrmProposalApproved`
- `SalesOrderCreated`, `SalesOrderConfirmed`
- Permission: `Sales.ControlTower.View`, `CRM.Proposal.Approve`, `Sales.Order.Write`
- Workflow: Teklif Onay Akışı, Fırsat Kapanış Hatırlatması

---

## 3. Finance & Cash Control Tower

### Menü Başlıkları
- Finance Overview
- Cash Position
- Receivables & Payables
- Journal Entries
- Invoices
- Bank & Vault
- Budget Management
- Tax & Compliance
- Finance Reports

### KPI Kartları
- Günlük Nakit Pozisyonu (₺, $, €)
- Toplam Alacak (vadesi gelmemiş / gecikmiş)
- Toplam Borç (vadesi gelmemiş / gecikmiş)
- DSO — Ortalama Tahsilat Süresi (gün)
- DPO — Ortalama Ödeme Süresi (gün)
- Aylık Gelir vs Gider Farkı
- Vergi Borcu
- Banka Bakiyeleri (tüm hesaplar özet)

### Executive Snapshot
- Günlük nakit giriş/çıkış
- Bugün vadesi gelen ödemeler
- Bu hafta gelecek tahsilatlar
- Güncel kur bilgisi

### Today's Priorities
- Bugün yapılacak ödemeler
- Bugün tahsilatı beklenen faturalar
- Geciken banka mutabakatları
- Onay bekleyen yevmiye fişleri

### Critical Alerts
- Negatif nakit pozisyonu uyarısı
- 30+ gün gecikmiş alacaklar
- Vergi beyanı son gün uyarısı
- Bütçe aşım uyarısı

### Notifications
- Fatura oluşturuldu
- Ödeme gerçekleşti
- Banka mutabakatı tamamlandı

### Risk / Health Score
- Likidite Skoru
- Alacak Tahsilat Skoru

### Customer / Supplier / Department Panels
- Alacak Yaşlandırma Listesi (müşteri bazlı)
- Borç Yaşlandırma Listesi (tedarikçi bazlı)
- Departman Bütçe Kullanım Paneli

### Message Drafts
- Gecikmiş alacak uyarı e-postası taslakları
- Ödeme bildirimi taslakları

### Calendar & Key Events
- Vergi beyan tarihleri
- Banka kredi taksit tarihleri
- Dönem kapanış tarihleri

### Next 7 Days Focus
- Haftalık nakit akış özeti
- Vadesi gelen ödemeler
- Banka mutabakat planı

### Reports & Analytics
- Nakit Akış Tablosu (Cash Flow Statement)
- Alacak Yaşlandırma Raporu
- Borç Yaşlandırma Raporu
- Gelir Tablosu (P&L)
- Bilanço Özeti

### Gerekli Backend Modülleri
- FinanceModule (JournalEntry, AccountPlan, Invoice, Payment)
- BankModule (BankAccount, BankTransaction)
- BudgetModule

### Gerekli Entity Adayları
- `FinanceAccountPlan`, `FinanceJournalEntry`, `FinanceJournalEntryLine`
- `FinanceInvoice`, `FinanceInvoiceLine`
- `FinancePayment`
- `BankAccount`, `BankTransaction`, `BankReconciliation`
- `CashVault`, `CashVaultTransaction`
- `BudgetTarget`, `BudgetLine`
- `TaxDeclaration`

### Gerekli Workflow / Event / Permission Adayları
- `FinanceJournalEntryCreated`, `FinanceJournalEntryPosted`
- `FinanceInvoiceCreated`, `FinancePaymentCompleted`
- Permission: `Finance.ControlTower.View`, `Finance.JournalEntry.Post`, `Finance.Invoice.Write`
- Workflow: Otomatik Gecikme Uyarısı, Dönem Kapanış Checklist

---

## 4. HR & Admin Control Tower

### Menü Başlıkları
- HR Overview
- Employees
- Leave Management
- Payroll
- Recruitment
- Performance Reviews
- Org Chart
- HR Reports

### KPI Kartları
- Toplam Personel Sayısı
- Bu Ay İzinde Olan Personel
- Açık Pozisyon Sayısı
- Ortalama İzin Bakiyesi
- İşe Alım Sürecindeki Aday Sayısı
- Aylık Personel Devir Hızı (%)
- Eğitim Tamamlama Oranı (%)

### Executive Snapshot
- Bugün izinli personel listesi
- Bu hafta işe başlayanlar
- Kritik açık pozisyonlar
- Performans dönemi durumu

### Today's Priorities
- Bugün onaylanması gereken izin talepleri
- İşe giriş/çıkış işlemleri
- Görev süresi dolan sözleşmeler

### Critical Alerts
- Kıdem tazminatı hak eden personel
- İzin limitini aşan çalışanlar
- Sözleşme bitiş tarihi yaklaşanlar

### Notifications
- İzin talebi oluşturuldu
- İzin onaylandı / reddedildi
- Personel kaydı güncellendi

### Risk / Health Score
- İşgücü Risk Skoru
- Personel Memnuniyet Endeksi

### Customer / Supplier / Department Panels
- Departman Bazlı Personel Dağılımı
- Departman İzin Kullanım Paneli

### Message Drafts
- Personel duyuru taslakları
- Sözleşme yenileme bildirimleri

### Calendar & Key Events
- Doğum günleri ve iş yıl dönümleri
- Performans değerlendirme tarihleri
- Eğitim ve seminer tarihleri

### Next 7 Days Focus
- İşe başlayacak personel
- Süresi dolacak izinler
- Maaş bordro hazırlık tarihi

### Reports & Analytics
- Personel Devir Analizi
- İzin Kullanım Raporu
- Departman Maliyet Raporu
- Demografik Analiz

### Gerekli Backend Modülleri
- HRModule (Employee, Leave, LeaveType)
- PayrollModule
- RecruitmentModule
- PerformanceModule

### Gerekli Entity Adayları
- `HrEmployee`, `HrLeave`, `HrLeaveType`
- `HrDepartment`, `HrPosition`
- `HrPayroll`, `HrPayrollLine`
- `HrRecruitmentJob`, `HrCandidate`
- `HrPerformanceReview`
- `HrContract`

### Gerekli Workflow / Event / Permission Adayları
- `HrLeaveRequested`, `HrLeaveApproved`, `HrLeaveRejected`
- `HrEmployeeOnboarded`, `HrEmployeeOffboarded`
- Permission: `HR.ControlTower.View`, `HR.Leave.Approve`, `HR.Payroll.Read`
- Workflow: İzin Onay Akışı, Onboarding Checklist

---

## 5. Production & Manufacturing Control Tower

### Menü Başlıkları
- Production Overview
- Work Orders
- Production Lines
- Machine Efficiency
- Material Consumption
- Production Schedule
- Waste & Loss
- Production Reports

### KPI Kartları
- Günlük Üretim Adedi (Gerçek vs Plan)
- OEE — Toplam Ekipman Verimliliği (%)
- Fire / Atık Oranı (%)
- Makine Duruş Süresi (saat)
- Ortalama Çevrim Süresi
- WIP — Süreçteki Yarı Mamul Değeri
- Kapasite Kullanım Oranı (%)

### Executive Snapshot
- Bugünkü üretim planı özeti
- Kritik geciken iş emirleri
- Makine arıza durumu
- Günlük fire özeti

### Today's Priorities
- Başlaması gereken iş emirleri
- Malzeme eksikliği uyarıları
- Planlanan bakım işleri
- Bekleyen kalite onayları

### Critical Alerts
- Makine arızası
- Üretim planı gerisinde kalma
- Kritik hammadde stok alarmı
- Red / fire oranı eşik aşımı

### Notifications
- İş emri tamamlandı
- Kalite onayı gerekiyor
- Hammadde talebi oluşturuldu

### Risk / Health Score
- Üretim Sağlık Skoru (OEE bazlı)
- Kapasite Risk Göstergesi

### Customer / Supplier / Department Panels
- Aktif Üretim Hattı Durumu
- Malzeme Tedarikçi Durumu

### Message Drafts
- Bakım talebi bildirimleri
- Müşteri gecikme bildirimleri

### Calendar & Key Events
- Planlı bakım tarihleri
- Müşteri teslimat tarihleri
- Üretim vardiya değişiklikleri

### Next 7 Days Focus
- Haftalık üretim planı
- Tamamlanması gereken iş emirleri
- Planlanan makine bakımları

### Reports & Analytics
- Günlük Üretim Raporu
- OEE Analizi
- Fire / Atık Analizi
- Kapasite Planlama Raporu
- Makine Duruş Raporu

### Gerekli Backend Modülleri
- ProductionModule (WorkOrder, ProductionLine, BOM)
- MachineModule
- InventoryModule (hammadde)
- MaintenanceModule

### Gerekli Entity Adayları
- `ProductionWorkOrder`, `ProductionWorkOrderLine`
- `ProductionLine`, `ProductionShift`
- `Machine`, `MachineDowntime`
- `BillOfMaterials`, `BOMLine`
- `ProductionMaterialConsumption`
- `ProductionWasteLog`
- `MaintenanceSchedule`

### Gerekli Workflow / Event / Permission Adayları
- `ProductionWorkOrderCreated`, `ProductionWorkOrderStarted`, `ProductionWorkOrderCompleted`
- `ProductionMachineBreakdownReported`
- Permission: `Production.ControlTower.View`, `Production.WorkOrder.Write`
- Workflow: İş Emri Akışı, Bakım Alarm Tetikleme

---

## 6. Quality Control Tower

### Menü Başlıkları
- QC Overview
- Inspection Results
- Claims & CAPA
- Standards Management
- Supplier Quality
- Customer Returns
- QC Reports

### KPI Kartları
- Günlük Kalite Muayene Adedi
- İlk Geçiş Oranı — FPY (%)
- Müşteri Red / İade Oranı (%)
- Açık CAPA Sayısı
- Tedarikçi Kaynaklı Red Oranı (%)
- Ortalama CAPA Kapatma Süresi (gün)

### Executive Snapshot
- Bugün tamamlanan muayeneler
- Açık kritik CAPA'lar
- Son 7 gün müşteri şikayeti sayısı
- Günlük red oranı

### Today's Priorities
- Tamamlanması gereken muayeneler
- Yanıt bekleyen müşteri şikayetleri
- Süresi yaklaşan CAPA'lar

### Critical Alerts
- FPY eşik altı düşüş
- Müşteri iadesi yüksek hacim
- Kritik CAPA süre aşımı

### Notifications
- Muayene tamamlandı
- CAPA oluşturuldu
- Şikayet çözüldü

### Risk / Health Score
- Kalite Skoru (100 üzerinden)
- Tedarikçi Kalite Skoru

### Customer / Supplier / Department Panels
- Müşteri Şikayet Geçmişi Paneli
- Tedarikçi Kalite Performans Paneli

### Message Drafts
- Müşteri şikayet yanıt taslakları
- Tedarikçi düzeltme talebi taslakları

### Calendar & Key Events
- Planlı kalite denetimleri
- Sertifika yenileme tarihleri
- Müşteri kalite ziyaretleri

### Next 7 Days Focus
- Planlanan muayeneler
- CAPA son tarihleri
- Tedarikçi denetim ziyaretleri

### Reports & Analytics
- FPY Trend Raporu
- CAPA Durumu Raporu
- Müşteri İade Analizi
- Tedarikçi Kalite Karnesi

### Gerekli Backend Modülleri
- QCModule (QcTestResult, QcStandard, QcClaim)
- SupplierModule (kalite verileri)

### Gerekli Entity Adayları
- `QcStandard`, `QcTestResult`
- `QcClaim`, `QcCapa`
- `QcInspectionPlan`
- `SupplierQualityScore`

### Gerekli Workflow / Event / Permission Adayları
- `QcTestResultCompleted`, `QcClaimCreated`, `QcClaimResolved`
- `QcCapaCreated`, `QcCapaClosed`
- Permission: `QC.ControlTower.View`, `QC.Claim.Write`, `QC.Claim.Resolve`
- Workflow: CAPA Hatırlatma Akışı, Müşteri Şikayet Eskalasyon Akışı

---

## 7. Logistics Control Tower

### Menü Başlıkları
- Logistics Overview
- Shipments
- Warehouses & Stock
- Stock Transfers
- Carrier Management
- Customs & Documentation
- Logistics Reports

### KPI Kartları
- Bekleyen Sevkiyat Sayısı
- Bugün Teslim Edilecek Sipariş
- Ortalama Teslim Süresi (gün)
- Zamanında Teslimat Oranı (%)
- Depo Doluluk Oranı (%)
- Transit Stok Değeri

### Executive Snapshot
- Bugün çıkacak sevkiyatlar
- Gecikmiş teslimatlar
- Depo doluluk özeti
- Aktif transfer emirleri

### Today's Priorities
- Bugün hazırlanacak sevkiyatlar
- Bekleyen evrak onayları
- Geciken transferler

### Critical Alerts
- Geciken kritik teslimat
- Depo kapasite aşımı
- Gümrük bekleyen sevkiyat süresi

### Notifications
- Sevkiyat oluşturuldu
- Transfer tamamlandı
- Teslimat onaylandı

### Risk / Health Score
- Lojistik Risk Skoru
- Depo Sağlık Skoru

### Customer / Supplier / Department Panels
- Nakliye Firması Performans Paneli
- Depo Bazlı Stok Paneli

### Message Drafts
- Müşteri teslimat bildirimi taslakları
- Taşıyıcı koordinasyon mesajları

### Calendar & Key Events
- Planlı sevkiyat tarihleri
- Gümrük giriş/çıkış randevuları
- Periyodik stok sayım tarihleri

### Next 7 Days Focus
- Haftalık sevkiyat planı
- Süresi yaklaşan gümrük evrakları
- Stok sayım planı

### Reports & Analytics
- Sevkiyat Performans Raporu
- Depo Hareket Raporu
- Taşıyıcı Kıyaslama Raporu
- Stok Yaşlandırma Raporu

### Gerekli Backend Modülleri
- LogisticsModule (Shipment, StockTransfer, Warehouse, StockMovement)
- CustomsModule

### Gerekli Entity Adayları
- `LogisticsWarehouse`, `LogisticsShipment`
- `LogisticsStockMovement`, `LogisticsStockTransfer`, `LogisticsStockTransferLine`
- `LogisticsCarrier`
- `CustomsDeclaration`

### Gerekli Workflow / Event / Permission Adayları
- `LogisticsShipmentCreated`, `LogisticsShipmentDelivered`
- `LogisticsStockTransferRequested`, `LogisticsStockTransferCompleted`
- Permission: `Logistics.ControlTower.View`, `Logistics.Shipment.Write`, `Logistics.StockTransfer.Write`
- Workflow: Sevkiyat Onay Akışı, Gümrük Evrak Hatırlatma

---

## 8. Fabric Procurement Control Tower

### Menü Başlıkları
- Fabric Procurement Overview
- Purchase Orders
- Supplier Catalog
- Open Tenders / RFQ
- Delivery Tracking
- Price & Cost Analysis
- Procurement Reports

### KPI Kartları
- Aktif Kumaş Satın Alma Siparişi Sayısı
- Bu Ay Kumaş Alım Tutarı
- Ortalama Tedarik Süresi (gün)
- Zamanında Teslim Oranı (%)
- Fiyat Sapma Oranı (bütçe vs gerçek)
- Açık RFQ Sayısı
- Onay Bekleyen Sipariş Tutarı

### Executive Snapshot
- Bu hafta teslim edilecek kumaşlar
- Fiyat bütçe sapma özeti
- Aktif tedarikçi listesi ve risk skoru
- Acil temin gerektiren malzemeler

### Today's Priorities
- Bugün teslim beklenen siparişler
- Onay bekleyen satın alma emirleri
- Yanıt bekleyen RFQ'lar

### Critical Alerts
- Teslim tarihi geçmiş siparişler
- Kalite reddi yüksek tedarikçi uyarısı
- Stok altı düşen kumaş türleri

### Notifications
- Satın alma emri onaylandı
- Teslim tamamlandı
- RFQ yanıtı geldi

### Risk / Health Score
- Tedarikçi Güvenilirlik Skoru
- Tedarik Risk Skoru

### Customer / Supplier / Department Panels
- Kumaş Tedarikçi Listesi (performans, teslim, fiyat)
- Kumaş Kategori Bazlı Alım Paneli

### Message Drafts
- Tedarikçiye sipariş onay bildirimi
- Gecikme uyarı mesajları

### Calendar & Key Events
- Tedarikçi görüşme tarihleri
- Fuar ve tekstil fuarı tarihleri
- Sipariş teslim takvimi

### Next 7 Days Focus
- Bu hafta teslim edilecek kumaşlar
- Son teklif tarihleri
- Tedarikçi değerlendirme ziyaretleri

### Reports & Analytics
- Tedarikçi Performans Karnesi
- Kumaş Alım Maliyet Analizi
- Fiyat Karşılaştırma Raporu
- Tedarik Süresi Trend Raporu

### Gerekli Backend Modülleri
- ProcurementModule (PurchaseOrder, RFQ)
- SupplierModule
- InventoryModule (kumaş stok)

### Gerekli Entity Adayları
- `FabricPurchaseOrder`, `FabricPurchaseOrderLine`
- `FabricSupplier`, `FabricSupplierEvaluation`
- `FabricRFQ`, `FabricRFQResponse`
- `FabricMaterial` (Kumaş tanım kartı)
- `FabricPriceHistory`

### Gerekli Workflow / Event / Permission Adayları
- `FabricPurchaseOrderCreated`, `FabricPurchaseOrderApproved`
- `FabricPurchaseOrderDelivered`
- Permission: `FabricProcurement.ControlTower.View`, `FabricProcurement.PurchaseOrder.Approve`
- Workflow: Satın Alma Onay Akışı, Tedarikçi Değerlendirme Akışı

---

## 9. Accessories Procurement Control Tower

### Menü Başlıkları
- Accessories Procurement Overview
- Purchase Orders
- Supplier Catalog
- RFQ Management
- Stock & Inventory
- Cost Analysis
- Procurement Reports

### KPI Kartları
- Aktif Aksesuar Satın Alma Siparişi Sayısı
- Bu Ay Aksesuar Alım Tutarı
- Stok Altı Aksesuar Sayısı
- Ortalama Tedarik Süresi (gün)
- Onay Bekleyen Sipariş Değeri
- Açık RFQ Sayısı

### Executive Snapshot
- Kritik stok altı aksesuarlar
- Bu hafta teslim beklenenler
- Bütçe kullanım özeti

### Today's Priorities
- Bugün teslim beklenen aksesuarlar
- Onay bekleyen siparişler
- Acil stok ikmali gerektiren kalemler

### Critical Alerts
- Kritik aksesuar stoğu bitti
- Geciken teslimatlar
- Fiyat bütçe sapması

### Notifications
- Sipariş onaylandı
- Teslim gerçekleşti
- Yeni RFQ yanıtı

### Risk / Health Score
- Aksesuar Tedarik Risk Skoru

### Customer / Supplier / Department Panels
- Aksesuar Tedarikçi Listesi
- Aksesuar Kategori Paneli (düğme, fermuar, etiket vb.)

### Message Drafts
- Tedarikçi sipariş bildirimleri
- Gecikme uyarıları

### Calendar & Key Events
- Teslim takvimleri
- Tedarikçi görüşmeleri

### Next 7 Days Focus
- Bu haftaki teslimler
- Son teklif tarihleri

### Reports & Analytics
- Aksesuar Alım Maliyet Raporu
- Tedarikçi Performans Raporu
- Stok Kullanım Analizi

### Gerekli Backend Modülleri
- ProcurementModule
- SupplierModule
- InventoryModule

### Gerekli Entity Adayları
- `AccessoryPurchaseOrder`, `AccessoryPurchaseOrderLine`
- `AccessoryMaterial` (Aksesuar tanım kartı)
- `AccessorySupplier`
- `AccessoryRFQ`, `AccessoryRFQResponse`
- `AccessoryStockLevel`

### Gerekli Workflow / Event / Permission Adayları
- `AccessoryPurchaseOrderCreated`, `AccessoryPurchaseOrderApproved`
- Permission: `AccessoryProcurement.ControlTower.View`, `AccessoryProcurement.PurchaseOrder.Approve`
- Workflow: Satın Alma Onay Akışı

---

## 10. Merchandising Control Tower

### Menü Başlıkları
- Merchandising Overview
- Collections & Seasons
- Product Development
- Order Tracking
- Buyer Communication
- Margin Analysis
- Merchandising Reports

### KPI Kartları
- Aktif Koleksiyon Sayısı
- Bu Sezon Hedeflenen vs Gerçek Sipariş Adedi
- Ortalama Geliştirme Süresi (gün)
- Aktif Alıcı (Buyer) Sayısı
- Sipariş Onay Oranı (%)
- Marj (Hedef vs Gerçek)

### Executive Snapshot
- Bu sezon aktif koleksiyonlar
- Kritik alıcı geri bildirimleri
- Geciken onaylar

### Today's Priorities
- Yanıt bekleyen alıcı talepleri
- Onay bekleyen ürün geliştirme aşamaları
- Bu hafta teslim edilecek numuneler

### Critical Alerts
- Sezon kapanış tarihi yaklaşan koleksiyonlar
- Marj eşik altında olan ürünler
- Alıcı onayı geciken siparişler

### Notifications
- Yeni alıcı talebi geldi
- Ürün onaylandı
- Sipariş güncellendi

### Risk / Health Score
- Koleksiyon Sağlık Skoru
- Alıcı İlişki Skoru

### Customer / Supplier / Department Panels
- Alıcı (Buyer) Listesi
- Koleksiyon Bazlı Ürün Paneli

### Message Drafts
- Alıcı güncellemesi e-postaları
- Ürün sunum taslakları

### Calendar & Key Events
- Koleksiyon sunum tarihleri
- Sipariş finalizasyon tarihleri
- Sezon teslim takvimleri

### Next 7 Days Focus
- Bu hafta teslim edilecek numuneler
- Alıcı toplantıları
- Koleksiyon sunum hazırlıkları

### Reports & Analytics
- Koleksiyon Performans Raporu
- Alıcı Sipariş Analizi
- Marj Analizi
- Ürün Geliştirme Zaman Analizi

### Gerekli Backend Modülleri
- MerchandisingModule
- SamplingModule
- CRMModule (Buyer ilişkisi)

### Gerekli Entity Adayları
- `Collection`, `CollectionProduct`
- `SeasonPlan`
- `Buyer`, `BuyerOrder`
- `ProductDevelopmentCard`
- `MerchandisingMarginTarget`

### Gerekli Workflow / Event / Permission Adayları
- `MerchandisingCollectionCreated`, `MerchandisingProductApproved`
- `MerchandisingBuyerOrderReceived`
- Permission: `Merchandising.ControlTower.View`, `Merchandising.Collection.Write`
- Workflow: Ürün Onay Akışı, Koleksiyon Sunum Akışı

---

## 11. Design Control Tower

### Menü Başlıkları
- Design Overview
- Design Briefs
- Design Revisions
- Mood Boards & Inspiration
- Sample Requests from Design
- Design Approvals
- Design Reports

### KPI Kartları
- Aktif Tasarım Brief Sayısı
- Ortalama Brief-to-Approval Süresi (gün)
- Onay Oranı (İlk revizyon) (%)
- Bu Sezon Tasarım Sayısı
- Revizyon Talep Sayısı

### Executive Snapshot
- Bu hafta tamamlanan tasarımlar
- Onay bekleyen tasarımlar
- Kritik tasarım son tarihleri

### Today's Priorities
- Bugün teslim edilmesi gereken tasarımlar
- Yanıt bekleyen revizyon talepleri
- Acil brief'ler

### Critical Alerts
- Son tarihi geçmiş tasarımlar
- Çok revizyonlu (3+) takılmış tasarımlar
- Alıcı onayı geciken tasarımlar

### Notifications
- Yeni brief atandı
- Tasarım onaylandı
- Revizyon talebi geldi

### Risk / Health Score
- Tasarım Süreç Sağlık Skoru

### Customer / Supplier / Department Panels
- Tasarımcı Bazlı İş Yükü Paneli
- Koleksiyon Bazlı Tasarım Paneli

### Message Drafts
- Alıcı / merchandising tasarım sunum taslakları
- Revizyon onay mesajları

### Calendar & Key Events
- Koleksiyon sunum tarihleri
- Tasarım kilit teslim günleri

### Next 7 Days Focus
- Bu hafta teslim edilecek tasarımlar
- Bekleyen revizyon süreçleri

### Reports & Analytics
- Tasarım Verimlilik Raporu
- Revizyon Analizi
- Tasarımcı Performans Raporu

### Gerekli Backend Modülleri
- DesignModule

### Gerekli Entity Adayları
- `DesignBrief`, `DesignRevision`
- `DesignAsset` (Dosya referansı)
- `MoodBoard`
- `DesignApproval`

### Gerekli Workflow / Event / Permission Adayları
- `DesignBriefCreated`, `DesignBriefApproved`, `DesignRevisionRequested`
- Permission: `Design.ControlTower.View`, `Design.Brief.Write`, `Design.Brief.Approve`
- Workflow: Tasarım Onay Akışı, Revizyon Takip Akışı

---

## 12. Sample / Model Room Control Tower

### Menü Başlıkları
- Sample Overview
- Sample Requests
- Sample Production Status
- Customer Sample Approvals
- Sample Costs
- Sample Inventory
- Sample Reports

### KPI Kartları
- Bekleyen Numune Talebi Sayısı
- Ortalama Numune Üretim Süresi (gün)
- Müşteri Numune Onay Oranı (%)
- Bu Ay Numune Maliyeti
- Red / Revizyon Oranı (%)

### Executive Snapshot
- Bugün teslim edilecek numuneler
- Onay bekleyen numuneler
- Geciken numune üretimleri

### Today's Priorities
- Bugün başlanacak numune üretimleri
- Onay sonuçlarına göre güncellenecek numuneler
- Teslim tarihi bugün olan numuneler

### Critical Alerts
- Geciken kritik numuneler
- Çok kez revize edilen numuneler
- Alıcı son tarihi yaklaşan numuneler

### Notifications
- Numune talebi oluşturuldu
- Numune onaylandı / reddedildi
- Üretim tamamlandı

### Risk / Health Score
- Numune Süreç Sağlık Skoru

### Customer / Supplier / Department Panels
- Müşteri/Alıcı Numune Durumu Paneli
- Koleksiyon Bazlı Numune Takip Paneli

### Message Drafts
- Müşteri numune gönderim bildirimleri
- Revizyon talep yanıtları

### Calendar & Key Events
- Numune teslim takvimleri
- Müşteri numune inceleme günleri

### Next 7 Days Focus
- Bu hafta teslim edilecek numuneler
- Bekleyen alıcı onayları

### Reports & Analytics
- Numune Performans Raporu
- Maliyet Analizi
- Revizyon Analizi

### Gerekli Backend Modülleri
- SamplingModule
- DesignModule (bağlantı)

### Gerekli Entity Adayları
- `SampleRequest`, `SampleCard`
- `SampleRevision`
- `SampleApproval`
- `SampleCostRecord`

### Gerekli Workflow / Event / Permission Adayları
- `SampleRequestCreated`, `SampleCompleted`, `SampleApproved`, `SampleRejected`
- Permission: `Sample.ControlTower.View`, `Sample.Request.Write`, `Sample.Request.Approve`
- Workflow: Numune Üretim Akışı, Müşteri Onay Takip Akışı

---

## 13. Licensing Control Tower

### Menü Başlıkları
- Licensing Overview
- License Agreements
- Royalty Tracking
- License Compliance
- Renewal Management
- Licensing Reports

### KPI Kartları
- Aktif Lisans Sayısı
- Bu Dönem Royalty Tahakkuku
- Süresi Dolacak Lisans Sayısı (90 gün içinde)
- Uyumsuzluk Bildirimi Sayısı
- Lisans Yenileme Oranı (%)

### Executive Snapshot
- Bu dönem kritik lisans durumu
- Royalty özeti
- Süresi yaklaşan lisanslar

### Today's Priorities
- Onay bekleyen lisans belgeleri
- Royalty ödeme tarihleri
- Uyumsuzluk aksiyon maddeleri

### Critical Alerts
- Süresi dolmuş lisanslar
- Royalty ödeme gecikmeleri
- Uyumsuzluk bildirimleri

### Notifications
- Lisans süresi doldu
- Royalty raporu hazır
- Yeni uyumsuzluk bildirimi

### Risk / Health Score
- Lisans Uyumluluk Skoru

### Customer / Supplier / Department Panels
- Lisans Sahibi / Marka Listesi
- Kategori Bazlı Lisans Paneli

### Message Drafts
- Yenileme hatırlatma taslakları
- Royalty bildirim taslakları

### Calendar & Key Events
- Lisans yenileme tarihleri
- Royalty ödeme günleri
- Denetim tarihleri

### Next 7 Days Focus
- Bu hafta sona erecek lisanslar
- Royalty raporlama son günleri

### Reports & Analytics
- Lisans Portföy Raporu
- Royalty Analizi
- Uyumluluk Durum Raporu

### Gerekli Backend Modülleri
- LicensingModule

### Gerekli Entity Adayları
- `LicenseAgreement`
- `RoyaltyRecord`
- `LicenseComplianceReport`
- `LicenseBrand`

### Gerekli Workflow / Event / Permission Adayları
- `LicensingAgreementExpiringSoon`, `LicensingAgreementRenewed`
- `LicensingRoyaltyDue`
- Permission: `Licensing.ControlTower.View`, `Licensing.Agreement.Write`
- Workflow: Lisans Yenileme Hatırlatma Akışı

---

## 14. Compliance & Sustainability Control Tower

### Menü Başlıkları
- Compliance Overview
- Regulatory Requirements
- Sustainability Metrics
- Certifications
- Audit Trail
- ESG Reporting
- Compliance Reports

### KPI Kartları
- Aktif Sertifika Sayısı
- Süresi Dolacak Sertifika Sayısı (90 gün)
- Açık Uyumsuzluk Bulgusu Sayısı
- CO₂ Emisyon Değeri (Ay)
- Su Tüketimi (Ay)
- Geri Dönüştürülmüş Malzeme Oranı (%)
- ESG Skoru

### Executive Snapshot
- Kritik uyumsuzluk bildirimleri
- Sertifika yenileme özeti
- ESG performans özeti

### Today's Priorities
- Denetim hazırlıkları
- Onay bekleyen uyumluluk belgeleri
- Acil düzeltme gerektiren bulgular

### Critical Alerts
- Süresi dolan sertifikalar
- Regülasyon değişiklik uyarıları
- Kritik ESG eşik aşımları

### Notifications
- Denetim raporu hazır
- Sertifika süresi yaklaşıyor
- Yeni regülasyon güncellendi

### Risk / Health Score
- Uyumluluk Risk Skoru
- ESG Sağlık Skoru

### Customer / Supplier / Department Panels
- Sertifika Portföy Paneli
- Tedarikçi Sürdürülebilirlik Skoru Paneli

### Message Drafts
- Denetim davet yanıtları
- Müşteri ESG raporlama taslakları

### Calendar & Key Events
- Denetim tarihleri
- Sertifika yenileme tarihleri
- ESG raporlama son günleri

### Next 7 Days Focus
- Bu hafta gerçekleşecek denetimler
- Süresi dolacak sertifikalar

### Reports & Analytics
- ESG Durum Raporu
- Sertifika Portföy Raporu
- Uyumsuzluk Bulgu Analizi
- Karbon Ayak İzi Raporu

### Gerekli Backend Modülleri
- ComplianceModule
- SustainabilityModule
- CertificationModule

### Gerekli Entity Adayları
- `Certification`, `CertificationAudit`
- `ComplianceFinding`, `ComplianceAction`
- `SustainabilityMetric`
- `ESGReport`
- `RegulationRecord`

### Gerekli Workflow / Event / Permission Adayları
- `ComplianceCertificationExpiringSoon`, `ComplianceCertificationRenewed`
- `ComplianceFindingOpened`, `ComplianceFindingClosed`
- Permission: `Compliance.ControlTower.View`, `Compliance.Certification.Write`
- Workflow: Sertifika Yenileme Akışı, Bulgu Kapatma Akışı

---

## 15. IT & AI Digital Control Tower

### Menü Başlıkları
- IT Overview
- System Health
- Infrastructure Monitoring
- AI Engine Status
- Security Alerts
- Support Tickets
- Integration Status
- IT Reports

### KPI Kartları
- Sistem Uptime Oranı (%)
- Açık IT Destek Talebi Sayısı
- Aktif AI Model Sayısı
- API Hata Oranı (%)
- Ortalama Destek Yanıt Süresi (dakika)
- Güvenlik Olayı Sayısı (Son 7 gün)
- Veritabanı Performans Skoru

### Executive Snapshot
- Sistem sağlık özeti
- Aktif güvenlik uyarıları
- Açık kritik destek talepleri
- AI servis durumu

### Today's Priorities
- Kritik destek talepleri
- Planlı bakım işlemleri
- Güvenlik olayı takibi

### Critical Alerts
- Sistem downtime
- Güvenlik ihlali
- Kritik API hatası
- Veritabanı bağlantı sorunu

### Notifications
- Sunucu uyarısı
- Destek talebi güncellendi
- Otomatik yedekleme tamamlandı

### Risk / Health Score
- Sistem Sağlık Skoru
- Güvenlik Risk Skoru

### Customer / Supplier / Department Panels
- Departman Destek Talebi Paneli
- Entegrasyon Durumu Paneli

### Message Drafts
- Sistem bakım duyuruları
- Kullanıcı bilgilendirme taslakları

### Calendar & Key Events
- Planlı bakım pencereleri
- Güvenlik denetim tarihleri
- Sistem güncelleme takvimi

### Next 7 Days Focus
- Planlı bakım işleri
- Açık kritik ticket'lar
- Güvenlik yama takvimleri

### Reports & Analytics
- Sistem Uptime Raporu
- Destek Talebi Analizi
- AI Model Performans Raporu
- Güvenlik Olay Raporu

### Gerekli Backend Modülleri
- ITSupportModule
- MonitoringModule
- AIEngineModule
- SecurityModule

### Gerekli Entity Adayları
- `ITSupportTicket`
- `SystemHealthSnapshot`
- `AIModelRegistry`, `AIModelRun`
- `SecurityIncident`
- `IntegrationLog`

### Gerekli Workflow / Event / Permission Adayları
- `ITSupportTicketCreated`, `ITSupportTicketResolved`
- `ITSecurityIncidentReported`
- Permission: `IT.ControlTower.View`, `IT.SupportTicket.Write`, `IT.SecurityIncident.Write`
- Workflow: Destek Talebi Akışı, Güvenlik Olay Eskalasyon Akışı

---

## 16. Performance Intelligence Control Tower

### Menü Başlıkları
- Performance Overview
- KPI Dashboard Builder
- Goal Management (OKR/KPI)
- Departman Scorecards
- Trend Analysis
- Benchmarking
- Performance Reports

### KPI Kartları
- Şirket OKR Tamamlanma Oranı (%)
- Departman Scorecard Ortalama Skoru
- Bu Çeyrekte Gerçekleşen Hedef Sayısı
- Geciken Hedef Sayısı
- Yüksek Performanslı Departman Sayısı
- Düşük Performanslı KPI Sayısı

### Executive Snapshot
- Şirket geneli hedef takip özeti
- En yüksek / en düşük performanslı departmanlar
- Bu çeyrekte kritik hedef durumu

### Today's Priorities
- Güncelleme gerektiren KPI değerleri
- Onay bekleyen hedef değişiklik talepleri
- Raporlama son günleri

### Critical Alerts
- Kritik hedef geriye düşüş
- OKR tamamlanma oranı kritik eşik altı
- Veri eksik KPI uyarısı

### Notifications
- Hedef güncellendi
- OKR dönemi kapandı
- Yeni benchmark verisi eklendi

### Risk / Health Score
- Şirket Performans Skoru
- Departman Bazlı Hedef Sağlık Skoru

### Customer / Supplier / Department Panels
- Departman Scorecard Paneli
- Kişi Bazlı Hedef Takip Paneli

### Message Drafts
- Departman hedef güncelleme hatırlatmaları
- Dönem kapanış raporlama talepleri

### Calendar & Key Events
- OKR dönem başlangıç / bitiş tarihleri
- Performans değerlendirme toplantıları
- Yönetim kurulu sunum tarihleri

### Next 7 Days Focus
- Bu hafta güncellenmesi gereken KPI'lar
- OKR check-in toplantıları
- Dönem kapanış hazırlıkları

### Reports & Analytics
- OKR İlerleme Raporu
- Departman Scorecard Raporu
- Trend Analizi
- Benchmark Karşılaştırma Raporu

### Gerekli Backend Modülleri
- PerformanceModule
- ReportingModule
- AnalyticsModule

### Gerekli Entity Adayları
- `OKRGoal`, `OKRKeyResult`
- `KPIDefinition`, `KPIValue`
- `DepartmentScorecard`
- `BenchmarkData`
- `PerformancePeriod`

### Gerekli Workflow / Event / Permission Adayları
- `PerformanceOKRGoalCreated`, `PerformanceOKRPeriodClosed`
- `PerformanceKPIValueUpdated`
- Permission: `Performance.ControlTower.View`, `Performance.OKRGoal.Write`, `Performance.KPIValue.Write`
- Workflow: OKR Check-in Hatırlatma, Dönem Kapanış Akışı

---

## Özet ve Görsel Kabul Matrisi

| Control Tower | Screenshot Reference | Required UI Blocks | Backend Modules | Missing Domain | MVP Priority |
| ------------- | -------------------- | ------------------ | --------------- | -------------- | ------------ |
| CEO Control Tower | `screenshots/ceo-ct.png` | Tüm 15 UI Bloğu Zorunlu | Finance, Sales, HR, Production, QC, CRM, Reporting | ExecutiveDashboard, BudgetTarget, DecisionLog | 🔴 Kritik |
| Sales Control Tower | `screenshots/sales-ct.png` | Tüm 15 UI Bloğu Zorunlu | CRM, Sales, Reporting | CrmOpportunity, SalesOrder, SalesTarget | 🔴 Kritik |
| Finance & Cash Control Tower | `screenshots/finance-ct.png` | Tüm 15 UI Bloğu Zorunlu | Finance, Bank, Budget | FinanceJournal, BankAccount, BudgetLine | 🔴 Kritik |
| HR & Admin Control Tower | `screenshots/hr-ct.png` | Tüm 15 UI Bloğu Zorunlu | HR, Payroll, Recruitment | HrEmployee, HrLeave, HrPayroll | 🔴 Kritik |
| Production & Manufacturing Control Tower | `screenshots/production-ct.png` | Tüm 15 UI Bloğu Zorunlu | Production, Machine, Inventory | WorkOrder, BOM, MachineDowntime | 🔴 Kritik |
| Quality Control Tower | `screenshots/qc-ct.png` | Tüm 15 UI Bloğu Zorunlu | QC | QcTestResult, QcClaim, QcCapa | 🟠 Yüksek |
| Logistics Control Tower | `screenshots/logistics-ct.png` | Tüm 15 UI Bloğu Zorunlu | Logistics, Customs | LogisticsShipment, StockTransfer | 🟠 Yüksek |
| Fabric Procurement Control Tower | `screenshots/fabric-proc-ct.png` | Tüm 15 UI Bloğu Zorunlu | Procurement, Supplier, Inventory | FabricPurchaseOrder, FabricSupplier, FabricMaterial | 🟠 Yüksek |
| Accessories Procurement Control Tower | `screenshots/accessories-proc-ct.png` | Tüm 15 UI Bloğu Zorunlu | Procurement, Supplier, Inventory | AccessoryPurchaseOrder, AccessoryMaterial | 🟠 Yüksek |
| Merchandising Control Tower | `screenshots/merch-ct.png` | Tüm 15 UI Bloğu Zorunlu | Merchandising, Sampling, CRM | Collection, Buyer, BuyerOrder | 🟡 Orta |
| Design Control Tower | `screenshots/design-ct.png` | Tüm 15 UI Bloğu Zorunlu | Design | DesignBrief, DesignAsset, DesignApproval | 🟡 Orta |
| Sample / Model Room Control Tower | `screenshots/sample-ct.png` | Tüm 15 UI Bloğu Zorunlu | Sampling, Design | SampleRequest, SampleCard, SampleApproval | 🟡 Orta |
| Licensing Control Tower | `screenshots/licensing-ct.png` | Tüm 15 UI Bloğu Zorunlu | Licensing | LicenseAgreement, RoyaltyRecord | 🟡 Orta |
| Compliance & Sustainability Control Tower | `screenshots/compliance-ct.png` | Tüm 15 UI Bloğu Zorunlu | Compliance, Sustainability | Certification, ESGReport, ComplianceFinding | 🟡 Orta |
| IT & AI Digital Control Tower | `screenshots/it-ai-ct.png` | Tüm 15 UI Bloğu Zorunlu | IT Support, Monitoring, AI, Security | ITSupportTicket, SecurityIncident, AIModelRegistry | 🟡 Orta |
| Performance Intelligence Control Tower | `screenshots/performance-ct.png` | Tüm 15 UI Bloğu Zorunlu | Performance, Reporting, Analytics | OKRGoal, KPIDefinition, DepartmentScorecard | 🟡 Orta |

---

## Sprint Hazırlık Notu

Bu doküman onaylanmadan sprint planlaması başlatılamaz.

**Backend hazırlığı için öncelikli domainler:**

1. **Sprint 2A:** CRM + Sales (Control Tower 1 & 2)
2. **Sprint 2B:** Finance + Cash (Control Tower 3)
3. **Sprint 2C:** HR + Admin (Control Tower 4)
4. **Sprint 3A:** Production + QC (Control Tower 5 & 6)
5. **Sprint 3B:** Logistics + Procurement (Control Tower 7, 8, 9)
6. **Sprint 4:** Merchandising + Design + Sample (Control Tower 10, 11, 12)
7. **Sprint 5:** Licensing + Compliance + IT + Performance (Control Tower 13–16)

---

---

*Bu doküman ürün kapsamı çıkarma amacıyla hazırlanmıştır. Kod içermez.*  
*Güncellemeler Architecture Board onayı ile yapılır.*

---

## Standardization Notes

**Versiyon:** 1.1.0 — Standardizasyon güncellemesi (2026-06-27)

### Permission Adlandırma Standardı

Kaynak: `SECURITY_AUTHORIZATION.md` § 3 Permission Matrix

**Format:** `Module.Resource.Action`

| Eski (v1.0.0 — Hatalı) | Yeni (v1.1.0 — Standart) |
|---|---|
| `ceo.control-tower.view` | `CEO.ControlTower.View` |
| `decision-log.approve` | `CEO.DecisionLog.Approve` |
| `sales.control-tower.view` | `Sales.ControlTower.View` |
| `proposal.approve` | `CRM.Proposal.Approve` |
| `order.create` | `Sales.Order.Write` |
| `finance.control-tower.view` | `Finance.ControlTower.View` |
| `journal.post` | `Finance.JournalEntry.Post` |
| `invoice.approve` | `Finance.Invoice.Write` |
| `hr.control-tower.view` | `HR.ControlTower.View` |
| `leave.approve` | `HR.Leave.Approve` |
| `payroll.view` | `HR.Payroll.Read` |
| `production.control-tower.view` | `Production.ControlTower.View` |
| `work-order.manage` | `Production.WorkOrder.Write` |
| `qc.control-tower.view` | `QC.ControlTower.View` |
| `claim.manage` | `QC.Claim.Write` |
| `capa.close` | `QC.Claim.Resolve` |
| `logistics.control-tower.view` | `Logistics.ControlTower.View` |
| `shipment.manage` | `Logistics.Shipment.Write` |
| `stock.transfer` | `Logistics.StockTransfer.Write` |
| `fabric-procurement.control-tower.view` | `FabricProcurement.ControlTower.View` |
| `purchase-order.approve` (Fabric) | `FabricProcurement.PurchaseOrder.Approve` |
| `accessories-procurement.control-tower.view` | `AccessoryProcurement.ControlTower.View` |
| `purchase-order.approve` (Accessory) | `AccessoryProcurement.PurchaseOrder.Approve` |
| `merchandising.control-tower.view` | `Merchandising.ControlTower.View` |
| `collection.manage` | `Merchandising.Collection.Write` |
| `design.control-tower.view` | `Design.ControlTower.View` |
| `brief.assign` | `Design.Brief.Write` |
| `design.approve` | `Design.Brief.Approve` |
| `sample.control-tower.view` | `Sample.ControlTower.View` |
| `sample.manage` | `Sample.Request.Write` |
| `sample.approve` | `Sample.Request.Approve` |
| `licensing.control-tower.view` | `Licensing.ControlTower.View` |
| `license.manage` | `Licensing.Agreement.Write` |
| `compliance.control-tower.view` | `Compliance.ControlTower.View` |
| `certification.manage` | `Compliance.Certification.Write` |
| `it.control-tower.view` | `IT.ControlTower.View` |
| `support.manage` | `IT.SupportTicket.Write` |
| `security.manage` | `IT.SecurityIncident.Write` |
| `performance.control-tower.view` | `Performance.ControlTower.View` |
| `okr.manage` | `Performance.OKRGoal.Write` |
| `kpi.update` | `Performance.KPIValue.Write` |

> [!NOTE]
> `ControlTower.View` action'ı her modülde standart olarak tanımlanmalıdır. Bu permission, Control Tower ekranına genel erişimi kontrol eder. Granüler kaynak izinleri ayrıca tanımlanır.

---

### Domain Event Adlandırma Standardı

Kaynak: `EVENT_BUS.md` § Event İsimlendirme Standardı

**Format:** `EntityAction` — Entity adı modül prefix'i ile başlar (örn. `Crm`, `Finance`, `HR`, `Logistics`)

| Eski (v1.0.0 — Hatalı) | Yeni (v1.1.0 — Standart) | Modül |
|---|---|---|
| `DecisionLogCreated` | `CeoDecisionLogCreated` | CEO |
| `DecisionLogApproved` | `CeoDecisionLogApproved` | CEO |
| `OpportunityCreated` | `CrmOpportunityCreated` | CRM |
| `ProposalCreated` | `CrmProposalCreated` | CRM |
| `ProposalApproved` | `CrmProposalApproved` | CRM |
| `JournalEntryCreated` | `FinanceJournalEntryCreated` | Finance |
| `JournalEntryPosted` | `FinanceJournalEntryPosted` | Finance |
| `InvoiceCreated` | `FinanceInvoiceCreated` | Finance |
| `PaymentCompleted` | `FinancePaymentCompleted` | Finance |
| `WorkOrderCreated` | `ProductionWorkOrderCreated` | Production |
| `WorkOrderStarted` | `ProductionWorkOrderStarted` | Production |
| `WorkOrderCompleted` | `ProductionWorkOrderCompleted` | Production |
| `MachineBreakdownReported` | `ProductionMachineBreakdownReported` | Production |
| `CapaCreated` | `QcCapaCreated` | QC |
| `CapaClosed` | `QcCapaClosed` | QC |
| `ShipmentCreated` | `LogisticsShipmentCreated` | Logistics |
| `ShipmentDelivered` | `LogisticsShipmentDelivered` | Logistics |
| `StockTransferRequested` | `LogisticsStockTransferRequested` | Logistics |
| `StockTransferCompleted` | `LogisticsStockTransferCompleted` | Logistics |
| `FabricDeliveryReceived` | `FabricPurchaseOrderDelivered` | FabricProcurement |
| `CollectionCreated` | `MerchandisingCollectionCreated` | Merchandising |
| `ProductApproved` | `MerchandisingProductApproved` | Merchandising |
| `BuyerOrderReceived` | `MerchandisingBuyerOrderReceived` | Merchandising |
| `DesignApproved` | `DesignBriefApproved` | Design |
| `SampleRequested` | `SampleRequestCreated` | Sample |
| `LicenseExpiringSoon` | `LicensingAgreementExpiringSoon` | Licensing |
| `LicenseRenewed` | `LicensingAgreementRenewed` | Licensing |
| `RoyaltyDue` | `LicensingRoyaltyDue` | Licensing |
| `CertificationExpiringSoon` | `ComplianceCertificationExpiringSoon` | Compliance |
| `CertificationRenewed` | `ComplianceCertificationRenewed` | Compliance |
| `SupportTicketCreated` | `ITSupportTicketCreated` | IT |
| `SupportTicketResolved` | `ITSupportTicketResolved` | IT |
| `SecurityIncidentReported` | `ITSecurityIncidentReported` | IT |
| `OKRGoalCreated` | `PerformanceOKRGoalCreated` | Performance |
| `OKRPeriodClosed` | `PerformanceOKRPeriodClosed` | Performance |
| `KPIValueUpdated` | `PerformanceKPIValueUpdated` | Performance |

> [!NOTE]
> `HrLeaveRequested`, `HrLeaveApproved`, `HrLeaveRejected`, `HrEmployeeOnboarded`, `HrEmployeeOffboarded`, `QcTestResultCompleted`, `QcClaimCreated`, `QcClaimResolved`, `FabricPurchaseOrderCreated`, `FabricPurchaseOrderApproved`, `AccessoryPurchaseOrderCreated`, `AccessoryPurchaseOrderApproved`, `DesignBriefCreated`, `DesignRevisionRequested`, `SalesOrderCreated`, `SalesOrderConfirmed` event adları zaten standarda uygundu — değiştirilmedi.

---

### Entity Adlandırma Standardı

Kaynak: `DOMAIN_MODEL.md` Entity Matrix + `UBIQUITOUS_LANGUAGE.md`

Entity adları `ModuleEntityName` formatında korunmuştur:

| Doğrulanan Prefix | Modül | Örnek Entity |
|---|---|---|
| `Crm` | CRM | `CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal` |
| `Sales` | Sales | `SalesOrder`, `SalesOrderItem`, `SalesTarget` |
| `Finance` | Finance | `FinanceAccountPlan`, `FinanceJournalEntry`, `FinanceInvoice`, `FinancePayment` |
| `Hr` | HR | `HrEmployee`, `HrLeave`, `HrLeaveType`, `HrPayroll` |
| `Logistics` | Logistics | `LogisticsWarehouse`, `LogisticsShipment`, `LogisticsStockMovement` |
| `Qc` | QC | `QcStandard`, `QcTestResult`, `QcClaim`, `QcCapa` |
| `Production` | Production | `ProductionWorkOrder`, `ProductionLine`, `ProductionWasteLog` |
| `Fabric` | Fabric Procurement | `FabricPurchaseOrder`, `FabricMaterial`, `FabricSupplier` |
| `Accessory` | Accessory Procurement | `AccessoryPurchaseOrder`, `AccessoryMaterial` |
| `Merchandising` | Merchandising | `MerchandisingMarginTarget`, `Collection`, `Buyer` |
| `Design` | Design | `DesignBrief`, `DesignRevision`, `DesignApproval` |
| `Sample` | Sample | `SampleRequest`, `SampleCard`, `SampleApproval` |
| `Licensing` | Licensing | `LicenseAgreement`, `RoyaltyRecord` |
| `Compliance` | Compliance | `Certification`, `ComplianceFinding`, `ESGReport` |
| `IT` | IT | `ITSupportTicket`, `SystemHealthSnapshot` |
| `Performance` | Performance | `PerformanceOKRGoal`, `PerformanceKPIDefinition` |

> [!IMPORTANT]
> Yeni domain event veya permission tanımlarken bu tabloya ve ilgili standart dokümanlara başvurun.
> Standartsız isimlendirme sprint planlama aşamasında reddedilir.
