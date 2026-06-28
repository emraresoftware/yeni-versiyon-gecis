# Legacy Entity Catalog — TASK 021

**Tarih:** 2026-06-28 (TASK 021-B genişletme)  
**Amaç:** Eski projelerden çıkarılan entity envanteri; yeni BOS `DOMAIN_MODEL.md` ile eşleştirme referansı

---

## Eşleştirme Anahtarı

| Yeni BOS (DOMAIN_MODEL) | Legacy karşılık(lar) |
|-------------------------|----------------------|
| `CrmAccount` | Customer (Ticket), Hesap (emare-crm), Customer (Finance) |
| `CrmContact` | CustomerContact, Kisi |
| `CrmOpportunity` | Firsat, SalesLead, Opportunity |
| `CrmProposal` | Proposal, Teklif, Quote |
| `SalesOrder` | Order (Ticket), Satış siparişi (Finance Sale) |
| `FinanceAccountPlan` | HesapPlani, AccountPlan |
| `FinanceJournalEntry` | YevmiyeFisi, JournalEntry |
| `FinanceInvoice` | Fatura, PurchaseInvoice, EInvoice |
| `FinancePayment` | Payment, CariHesap hareketleri |
| `HrEmployee` | Calisan, Employee |
| `HrLeave` | IzinTalebi, Leave |
| `LogisticsWarehouse` | Depo, Warehouse |
| `LogisticsStockMovement` | StokHareketi, StockMovement |
| `QcStandard` / `QcTestResult` / `QcClaim` | VeriKaliteKurali (emare-crm); QC stub (Elyafgroup) |
| `ProductionWorkOrder` | MrpSuggestion → PO (Finance); IsEmri (saha servis, farklı) |
| `DecisionLog` | — (yalnızca BOS hedef) |

---

## 1. Elyafgroup — EmareTicket.Domain

### Elyaf / Control Tower (`Domain/Elyaf/`)

| Entity | Alanlar / Not |
|--------|---------------|
| `CrmAccount` | Cari hesap (yeni BOS uyumlu) |
| `CrmContact` | İletişim kişisi |
| `CrmOpportunity` | Satış fırsatı, stage: New→Won/Lost |
| `CrmProposal` | Teklif; status Draft/Sent/Approved/Declined |
| `CrmProposalItem` | Teklif satırları |
| `NumberSequence` | CR-/PR- otomatik numara |
| `ElyafKpiSnapshot` | KPI zaman serisi |
| `ElyafAlert` | Operasyon uyarıları |
| `ElyafPriority` | Öncelik kayıtları |
| `ElyafHealthScore` | Sağlık skoru |
| `ElyafMessageDraft` | AI mesaj taslakları |
| `ElyafDataSource` | Sheets/ERP sync metadata |
| `ElyafCollection` | Koleksiyon (merchandising) |
| `ElyafStyle` | Stil kartı, OTD/risk |
| `ElyafSample` | Numune (SampleType, LeadTimeDays) |

### Core Platform (`Domain/Entities/`)

**Kimlik & Tenant**

- `User`, `Role`, `Permission`, `UserRole`, `RolePermission`, `RefreshToken`
- `Tenant`, `TenantFeature`, `UserFeatureAccess`, `TenantApiKey`
- `SubscriptionPlan`, `ProvisioningToken`

**CRM & Satış**

- `Customer`, `CustomerNote`, `CustomerActivity`, `CustomerFile`, `CustomerContact`
- `Proposal`, `ProposalView`, `Project`, `Task`, `Appointment`
- `SalesLead`, `SalesLeadActivity`, `SalesLeadItem`
- `Product`, `Order`, `OrderItem`, `Payment`

**Service Desk**

- `SupportTicket`, `TicketProcess`, `TicketProcessStage`
- `TicketFieldDefinition`, `TicketFieldRule`, `WorkflowRule`

**İletişim**

- `MailAccount`, `MailTemplate`, `MailSignature`, `InboundEmail`
- `WhatsAppAccount`, `WhatsAppConversation`, `WhatsAppMessage`
- `ChatVisitor`, `ChatConversation`, `ChatMessage`, `ChatOperator`
- `CallLog`, `CallDetailRecord`, `CallCampaign`, `SipTrunk`, `AfterHoursConfig`

**AI & Konfig**

- `AIProviderConfig`, `AIScenarioConfig`, `AIAutoReplyConfig`
- `AgentDocument`, `AiUsageRecord`, `AIAuditLog`
- `VoiceScenario`, `Sector`, `SectorKnowledgeEntry`, `ExternalIntegration`

**Audit**

- `AuditLog`, `PlatformFeedback`, `MailAiNotificationLog`

### Platform BOS (`src/Platform/Domain/`)

- `ApplicationUser`, `Tenant`, `Role`, `Permission`, `AuditLog`, `OutboxMessage`
- CRM: `CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmProposalItem`, `CrmActivity`, `CrmTag`

---

## 2. emare-crm (Laravel) — 186 Model

### CRM Çekirdek

| Entity (TR) | İngilizce karşılık |
|-------------|-------------------|
| `Hesap` | Account |
| `Kisi` | Contact |
| `Firsat` | Opportunity |
| `AdayMusteri` | Lead |
| `Aktivite` | Activity |
| `DestekTalebi` | Support Ticket |
| `Teklif` | Proposal |
| `Sozlesme` | Contract |
| `Fatura` | Invoice |
| `Urun`, `UrunVaryant` | Product, Variant |
| `Kampanya`, `FiyatListesi` | Campaign, Price List |

### Finans

- `HesapPlani`, `YevmiyeFisi`, `YevmiyeSatiri`, `CariHesap`
- `DovizKuru`, `Butce`, `SabitKiymet`

### Operasyon

- `SatinalmaTalebi`, `Tedarikci`, `Depo`, `DepoStok`, `StokHareketi`, `MalKabul`
- `IsEmri`, `SahaMalzeme`, `SahaTeknisyen` (saha servis — üretim değil)

### İş Akışı & Kurallar

- `Blueprint`, `BlueprintState`, `BlueprintTransition`
- `OtomasyonKurali`, `OnayAkisi`, `OnayTalebi`, `CustomRule`
- `VeriKaliteKurali`, `VeriKaliteSkoru`

### AI & Sektör

- `AiAjan`, `AiAjanLog`, `MusteriDijitalIkiz`, `RakipIntelligence`
- `InsaProje`, `OtoArac`, `SaglikHasta`, `TlkmAbonelik` (sektör dikey)

### RBAC

- `Rol`, `Izin`, `Tenant`, `User`

---

## 3. Emare Finance Standalone — 194 Model

### Ticari

| Entity | Not |
|--------|-----|
| `Customer` | Cari |
| `Product`, `ProductBatch`, `ProductSerial` | Ürün, lot, seri |
| `ProductAttribute`, `ProductAttributeValue` | Varyant |
| `Sale`, `SaleItem` | Satış |
| `Quote` | Teklif |
| `Campaign` | Kampanya |

### Finans / Muhasebe

- `AccountPlan`, `JournalEntry`, `JournalEntryLine`
- `CashAccount`, `CheckNote`, `Reconciliation`
- `FixedAsset`, `Loan`, `CurrencyRate`
- `EInvoice`, `ESmmDocument`

### Tedarik & Lojistik

- `PurchaseOrder`, `GoodsReceipt`, `PurchaseInvoice`
- `Shipment`, `SupplierProposal`
- `StockMovement`

### Üretim (kritik — BOS'ta yok)

| Entity | Not |
|--------|-----|
| `Bom` | Ürün reçetesi; `unitCost()` fire oranı |
| `BomLine` | Reçete satırı |
| `BomOperation` | Operasyon / routing |
| `Workstation` | İş istasyonu |
| `MrpRule` | min/max stock, lead time, reorder |
| `MrpSuggestion` | MRP önerisi → PO draft |

### Tenant & Yetki

- `Tenant`, `Branch`, `Role`, `Permission`, `UserRole`
- `Module`, `TenantModule`, `BranchModule`

### POS / Perakende

- `PosTable`, `PosTableOrder`, restoran masa/mutfak entity'leri

### HR

- `Employee`, `Leave`, `Timesheet`, `Recruitment*`

### Diğer

- `Ticket`, `Project`, `Webhook*`, `Marketplace*` (Trendyol, HB, N11)

---

## 4. emarecc — PostgreSQL Şema

| Tablo / Entity | Not |
|----------------|-----|
| `users` | admin / supervisor / agent |
| `customers` | Borç, dosya no, kurum, ödeme sözü |
| `customer_phone_numbers` | Çoklu telefon |
| `calls`, `cdr_records` | Çağrı kayıtları |
| `campaigns`, `campaign_leads` | Tahsilat kampanyası |
| `scripts` | Script placeholder (`{{debt_amount}}`) |
| `queues`, `trunks` | Kuyruk, hat |
| `chat_sessions`, `interactions` | Omnichannel |
| `sms_*` | SMS modülü |
| `customer_transfer_log` | Agent transfer |

---

## 5. Floragenix CRM — Prisma Schema

| Entity | Not |
|--------|-----|
| `User` | Rol: ADMIN, LEADER, EMPLOYEE, DEALER, WAREHOUSE |
| `Lead` | Pipeline; `parentId` bayi hiyerarşisi |
| `Product`, `Stock` | minLevel, literPrice |
| `Proposal`, `ProposalItem` | Draft/Sent/Accepted/Rejected |
| `Task`, `Document`, `CalendarEvent` | |
| `AutomationRule` | LeadStatusChange, ProposalCreated, TaskOverdue |
| `Team`, `Tag`, `Notification` | |
| `customFields` | JSON — esnek sektör alanları |

---

## 6. emarepos — Laravel Models

| Entity | Not |
|--------|-----|
| `Sale`, `SaleItem` | Satış, karma ödeme |
| `Product`, `Customer`, `Firm` | Ürün, müşteri, tedarikçi |
| `Order`, `RestaurantTable` | Restoran sipariş/masa |
| `Branch`, `CashRegister` | Şube, kasa |
| `StockMovement`, `PurchaseInvoice` | Stok, alış faturası |
| `Campaign`, `LoyaltyProgram` | |
| `Tenant`, `Plan`, `Module` | SaaS paketleme |
| `Role`, `Permission` | Granüler izinler |

---

## Textile-Specific Entity Durumu

| Entity | Var mı? | Proje |
|--------|---------|-------|
| Fabric / Kumaş | Hayır | — |
| Yarn / İplik | Hayır | — |
| Dyeing / Boyama | Hayır | — |
| Knitting / Örme | Hayır (yol haritası WorkCenter örneği) | Elyafgroup docs |
| Weaving / Dokuma | Hayır | — |
| Sample / Numune | Evet | `ElyafSample` |
| Style / Collection | Evet | `ElyafStyle`, `ElyafCollection` |
| BOM | Evet | Emare Finance |
| MRP | Evet | Emare Finance |
| WorkOrder (üretim) | Kısmi | Finance migration; saha IsEmri farklı |
| Machine | Hayır | Workstation var |
| Merchandising | UI only | Elyafgroup dashboard |

---

## Entity Sayı Özeti

| Proje | Entity / Model Sayısı |
|-------|----------------------|
| Elyafgroup EmareTicket.Domain | ~80+ entity sınıfı |
| Elyafgroup Platform.Domain | ~15 CRM + kernel |
| emare-crm | 186 model |
| Emare Finance standalone | 194 model |
| emarecc | ~20 tablo |
| Floragenix | ~15 Prisma model |
| emarepos | ~25 model |

---

# TASK 021-B — Yeni Entity'ler

## 7. Emare Saloon — ~96 model (`app/Models/`)

**Tenant/SaaS:** `Tenant`, `Branch`, `Module`, `TenantModule`

**CRM:** `Customer*`, randevu/agenda entity'leri

**Satış/Kasa:** `Sale`, `SalePayment`, `CashRegister`, `Cash*`, `Bank*`

**Stok:** `Stock*`, transfer, sayım entity'leri

**Finans:** `Income`, `Expense`, gelir/gider

**Personel:** `Staff*`, SMS/kampanya

## 8. Emare Pazar — (`app/models/`)

| Entity | Not |
|--------|-----|
| `Marketplace`, `MarketplaceCredential` | Platform bağlantı |
| `Product`, `ProductVariant`, `ProductMarketplace` | Katalog sync |
| `Order`, `OrderItem` | Normalize sipariş |
| `Category`, `CategoryMapping` | Kategori eşleme |

## 9. raporlama-app — (`app/Models/`)

| Entity | Not |
|--------|-----|
| `Tenant` | Multi-tenant |
| `Sale`, `Product`, `Category`, `Customer`, `Staff` | Rapor domain |
| `StaffMotion` | Personel hareket |
| `StockMovement`, `StockLot` | Stok analizi |
| `DataImportBatch` | CSV/batch import yaşam döngüsü |

## 10. emareciftlik — 50 model (`app/Models/`)

| Entity | Not |
|--------|-----|
| `Animal`, `SmallAnimal` | Büyükbaş/küçükbaş |
| `MilkRecord` | Süt kaydı |
| `InventoryItem` | Yem/stok |
| `Contact`, `ContactTransaction` | CRM/tedarikçi |
| `Staff`, `Field`, `Equipment` | Operasyon |
| `Financial*` | Finans kartları |

## 11. emareaplincedesk — 13 model

`Customer`, `ServiceRequest`, `Technician`, `Invoice`, `InvoiceItem`, `SparePart`, `SparePartUsage`, `Payment`, `Device`, `Branch`

## 12. emareasistan — (`models/`)

| Entity | Not |
|--------|-----|
| `Tenant`, `User`, `Partner` | Multi-tenant SaaS |
| `Conversation`, `ChatMessage` | Omnichannel |
| `Product`, `Order`, `Contact`, `Appointment` | Hafif ERP |
| `Invoice`, `PurchaseOrder`, `LeaveRequest` | Operasyon |
| `TenantWorkflow`, `ResponseRule`, `Embedding` | AI/workflow |

## 13. translation-manager

`Project`, `TranslationNamespace`, `TranslationKey`, `Translation`, `Language`

## 14. flovla (Closy)

`Room`, `RoomSection`, `RoomContent`, `ActionItem`, `RoomMember`, `SignatureRequest`, `FormField`, `FormSubmission`, `Integration`

## 15. ecomaiq

V1: `Store`, `Question`, `User` (JSON settings)  
V2 (planlı): tenant/user/store/question

---

## Güncellenmiş Entity Sayı Özeti

| Proje | Entity / Model Sayısı |
|-------|----------------------|
| Elyafgroup EmareTicket.Domain | ~80+ |
| Elyafgroup Platform.Domain | ~15 |
| emare-crm | 186 |
| Emare Finance standalone | 194 |
| **Emare Saloon** | **~96** |
| **emareciftlik** | **50** |
| emarepos | ~53 (arşiv) / ~25 (aktif path) |
| **Emare Pazar** | **~8 core** |
| **raporlama-app** | **~10** |
| **emareasistan** | **~20+** |
| emareaplincedesk | 13 |
| emarecc | ~20 tablo |
| Floragenix | ~15 |
| translation-manager | 5 |
| flovla | ~10 |
