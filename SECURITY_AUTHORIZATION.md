# Güvenlik ve Yetkilendirme Standartları (SECURITY_AUTHORIZATION.md)

**Title:** Güvenlik ve Yetkilendirme Standartları
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** README.md
**Related Documents:** SECURITY_ARCHITECTURE.md, UBIQUITOUS_LANGUAGE.md, MASTER_ARCHITECTURE_INDEX.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Standardized permissions, roles, and AI boundaries. |

---

## 🔒 1. Kiracı İzolasyonu (Tenant Isolation Enforcement)

Sistemdeki tüm kalıcı veriler kiracı bazında izole edilmelidir.
* **DbContext Seviyesi Filtreleme:**
  ```csharp
  builder.Entity<CrmAccount>().HasQueryFilter(x => x.TenantId == _tenantProvider.TenantId);
  ```
* **Kural:** HTTP Context içindeki JWT claims üzerinden tenant_id çözümlenmeli, client'tan gelen tenant parametrelerine güvenilmemelidir.

---

## 👥 2. Kilitlenen Rol Listesi

Sistemde tanımlı ve yetki sınırları belirlenmiş roller şunlardır:
1. `SystemAdmin`: Global sistem yöneticisi.
2. `TenantAdmin`: Kiracı/şirket yöneticisi.
3. `CEO`: Şirket tepe yöneticisi.
4. `SalesManager`: Satış yöneticisi.
5. `FinanceManager`: Finans ve muhasebe yöneticisi.
6. `HRManager`: İnsan kaynakları yöneticisi.
7. `ProductionManager`: Üretim yöneticisi.
8. `QCManager`: Kalite kontrol yöneticisi.
9. `LogisticsManager`: Lojistik ve depo yöneticisi.
10. `Employee`: Standart şirket çalışanı.
11. `Auditor`: Denetçi.
12. `AIOrchestrator`: Otonom AI ajan yöneticisi.

---

## 🔑 3. Permission Matrix (İzin Matrisi)

Permission isimlendirme standardı: `Module.Resource.Action`

| Permission | Module | Resource | Action | Default Roles | Scope | Notes |
| ---------- | ------ | -------- | ------ | ------------- | ----- | ----- |
| `CRM.Account.Read` | CRM | Account | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, FinanceManager, HRManager, QCManager, LogisticsManager, Employee | Tenant | Cari hesap listesini okuma. |
| `CRM.Account.Write` | CRM | Account | Write | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Cari oluşturma/düzenleme. |
| `CRM.Contact.Read` | CRM | Contact | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | İletişim kişisi okuma. |
| `CRM.Contact.Write` | CRM | Contact | Write | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | İletişim kişisi yazma. |
| `CRM.Opportunity.Read` | CRM | Opportunity | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Satış fırsatlarını okuma. |
| `CRM.Opportunity.Write` | CRM | Opportunity | Write | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Satış fırsatı yazma. |
| `CRM.Proposal.Read` | CRM | Proposal | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, FinanceManager | Tenant | Teklifleri okuma. |
| `CRM.Proposal.Write` | CRM | Proposal | Write | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Teklif oluşturma. |
| `CRM.Proposal.Approve` | CRM | Proposal | Approve | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Teklif onaylama. |
| `CRM.Activity.Read` | CRM | Activity | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Cari aktivite günlüklerini okuma. |
| `CRM.Activity.Write` | CRM | Activity | Write | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Cari aktivite günlüğü yazma. |
| `Sales.Order.Read` | Sales | Order | Read | SystemAdmin, TenantAdmin, CEO, SalesManager, FinanceManager, LogisticsManager | Tenant | Satış siparişlerini okuma. |
| `Sales.Order.Write` | Sales | Order | Write | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Satış siparişi yazma. |
| `Sales.Order.Approve` | Sales | Order | Approve | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Satış siparişi onaylama. |
| `Finance.AccountPlan.Read` | Finance | AccountPlan | Read | SystemAdmin, TenantAdmin, CEO, FinanceManager, HRManager | Tenant | Hesap planını okuma. |
| `Finance.AccountPlan.Write` | Finance | AccountPlan | Write | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Hesap planı yazma. |
| `Finance.JournalEntry.Read` | Finance | JournalEntry | Read | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Yevmiye fişlerini okuma. |
| `Finance.JournalEntry.Write` | Finance | JournalEntry | Write | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Yevmiye fişi yazma. |
| `Finance.JournalEntry.Post` | Finance | JournalEntry | Post | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Fişi deftere işleme. |
| `Finance.Invoice.Read` | Finance | Invoice | Read | SystemAdmin, TenantAdmin, CEO, FinanceManager, SalesManager | Tenant | Faturaları okuma. |
| `Finance.Invoice.Write` | Finance | Invoice | Write | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Fatura kesme. |
| `Finance.Payment.Read` | Finance | Payment | Read | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Ödemeleri okuma. |
| `Finance.Payment.Write` | Finance | Payment | Write | SystemAdmin, TenantAdmin, CEO, FinanceManager | Tenant | Ödeme/tahsilat girişi. |
| `HR.Employee.Read` | HR | Employee | Read | SystemAdmin, TenantAdmin, CEO, HRManager | Tenant | Personel kartlarını okuma. |
| `HR.Employee.Write` | HR | Employee | Write | SystemAdmin, TenantAdmin, CEO, HRManager | Tenant | Personel kartı yazma. |
| `HR.Leave.Read` | HR | Leave | Read | SystemAdmin, TenantAdmin, CEO, HRManager, Employee | User/Tenant | İzin okuma (Employee: kendi izni). |
| `HR.Leave.Write` | HR | Leave | Write | SystemAdmin, TenantAdmin, CEO, HRManager, Employee | User/Tenant | İzin talebi açma. |
| `HR.Leave.Approve` | HR | Leave | Approve | SystemAdmin, TenantAdmin, CEO, HRManager | Tenant | İzin onaylama. |
| `Logistics.Warehouse.Read` | Logistics | Warehouse | Read | SystemAdmin, TenantAdmin, CEO, LogisticsManager, ProductionManager | Tenant | Depoları listeleme. |
| `Logistics.Warehouse.Write` | Logistics | Warehouse | Write | SystemAdmin, TenantAdmin, CEO, LogisticsManager | Tenant | Depo tanımlama. |
| `Logistics.Stock.Read` | Logistics | Stock | Read | SystemAdmin, TenantAdmin, CEO, LogisticsManager, ProductionManager, SalesManager | Tenant | Stok durumunu okuma. |
| `Logistics.StockTransfer.Write` | Logistics | StockTransfer | Write | SystemAdmin, TenantAdmin, CEO, LogisticsManager | Tenant | Depo transfer talebi. |
| `Logistics.StockTransfer.Approve` | Logistics | StockTransfer | Approve | SystemAdmin, TenantAdmin, CEO, LogisticsManager | Tenant | Transfer onaylama. |
| `Logistics.StockTransfer.Complete` | Logistics | StockTransfer | Complete | SystemAdmin, TenantAdmin, CEO, LogisticsManager | Tenant | Depo transferini tamamlama. |
| `QC.Standard.Read` | QC | Standard | Read | SystemAdmin, TenantAdmin, CEO, QCManager, ProductionManager | Tenant | Standartları okuma. |
| `QC.Standard.Write` | QC | Standard | Write | SystemAdmin, TenantAdmin, CEO, QCManager | Tenant | Kalite standardı yazma. |
| `QC.TestResult.Read` | QC | TestResult | Read | SystemAdmin, TenantAdmin, CEO, QCManager, ProductionManager | Tenant | Test sonuçlarını okuma. |
| `QC.TestResult.Write` | QC | TestResult | Write | SystemAdmin, TenantAdmin, CEO, QCManager | Tenant | Test sonucu yazma. |
| `QC.Claim.Read` | QC | Claim | Read | SystemAdmin, TenantAdmin, CEO, QCManager, SalesManager | Tenant | Müşteri şikâyetlerini okuma. |
| `QC.Claim.Write` | QC | Claim | Write | SystemAdmin, TenantAdmin, CEO, QCManager | Tenant | Şikâyet kaydı açma. |
| `QC.Claim.Resolve` | QC | Claim | Resolve | SystemAdmin, TenantAdmin, CEO, QCManager | Tenant | Şikâyet kapatma/çözme. |
| `Production.WorkOrder.Read` | Production | WorkOrder | Read | SystemAdmin, TenantAdmin, CEO, ProductionManager, LogisticsManager | Tenant | İş emirlerini listeleme. |
| `Production.WorkOrder.Write` | Production | WorkOrder | Write | SystemAdmin, TenantAdmin, CEO, ProductionManager | Tenant | İş emri oluşturma/yönetme. |
| `CEO.DecisionLog.Read` | CEO | DecisionLog | Read | SystemAdmin, TenantAdmin, CEO, Auditor | Tenant | Karar defterini okuma. |
| `CEO.DecisionLog.Write` | CEO | DecisionLog | Write | SystemAdmin, TenantAdmin, CEO | Tenant | Karar oluşturma. |
| `CEO.DecisionLog.Approve` | CEO | DecisionLog | Approve | SystemAdmin, TenantAdmin, CEO | Tenant | Kararları onaylama. |
| `System.User.Manage` | System | User | Manage | SystemAdmin, TenantAdmin | Tenant | Kullanıcıları yönetme. |
| `System.Role.Manage` | System | Role | Manage | SystemAdmin | Tenant | Rolleri yönetme. |
| `AI.Copilot.Use` | AI | Copilot | Use | All Roles | User | AI Copilot kullanımı. |
| `AI.Agent.Execute` | AI | Agent | Execute | SystemAdmin, TenantAdmin, CEO, AIOrchestrator | Tenant | Ajan çalıştırma/yönetme. |
| `AI.Agent.Configure` | AI | Agent | Configure | SystemAdmin, TenantAdmin, CEO | Tenant | AI Ajan parametrelerini yapılandırma. |
| `AI.Prompt.Manage` | AI | Prompt | Manage | SystemAdmin, TenantAdmin, CEO | Tenant | AI prompt şablonlarını yönetme. |
| `AI.Memory.Read` | AI | Memory | Read | SystemAdmin, TenantAdmin, CEO, AIOrchestrator | Tenant | AI bellek kayıtlarını okuma. |
| `AI.Memory.Write` | AI | Memory | Write | SystemAdmin, TenantAdmin, CEO, AIOrchestrator | Tenant | AI bellek kayıtlarını yazma/güncelleme. |
| `AI.Audit.Read` | AI | Audit | Read | SystemAdmin, TenantAdmin, CEO, Auditor | Tenant | AI işlem denetim günlüklerini izleme. |

---

## 🛠️ 4. RBAC ve ABAC Ayrımı

Sistemde yetkilendirme iki katmanlı olarak çözümlenir:
1. **RBAC (Role-Based Access Control):** Kullanıcının rolüne göre statik yetki denetimi. (Örn: `FinanceManager` rolüne sahip biri yevmiye fişi girebilir).
2. **ABAC (Attribute-Based Access Control):** Dinamik veri niteliklerine göre denetim.
   - **Kiracı (Tenant) Koşulu:** Verinin `TenantId` bilgisi ile HTTP Context tenant'ı eşleşmelidir.
   - **Veri Sahibi (Owner) Koşulu:** Standart kullanıcılar (Employee) sadece kendi açtıkları talepleri (örn. kendi izin taleplerini) görebilir.
   - **Tutar Limiti Koşulu:** Belirli bir limitin üzerindeki teklif/satın alma onayları CEO veya yetkili rol onayına tabidir.

---

## 🤖 5. AI Agent Yetki Sınırları

AI Ajanları ve Copilot mekanizmaları sisteme erişirken şu sınırlara kesinlikle uymak zorundadır:
1. **Doğrudan Veritabanı Erişimi Yasaktır:** AI Ajanı veritabanına (`DbContext` veya ham SQL) doğrudan bağlanamaz, okuma ve yazma yapamaz.
2. **Uygulama Katmanı Zorunluluğu:** AI Ajanı sadece ve sadece API/Application katmanında yetkilendirilmiş somut servisleri (`IApplicationService` veya MediatR Command/Query) çağırarak işlem yürütebilir.
3. **Rol Sınırları:** AI tetiklendiği kullanıcının veya ona özel olarak atanan `AIOrchestrator` rolünün izin sınırlarını aşamaz.
4. **Öneri Gücü:** AI sadece öneri üretebilir ve onay yetkisi kendisinde olamaz. Kararlar her zaman bir insan (CEO, Manager) tarafından onaylanmalıdır.

---

## 🛡️ 6. Permission Kontrol Katmanları

* **API Controller Katmanı:** Endpoint bazında `[Authorize(Permissions.CRM.Account.Read)]` gibi deklaratif izin attribute'ları kullanılacaktır.
* **Application Katmanı:** Pipeline Behavior (`RequestValidationBehavior`) veya Handler içinde ABAC limit/departman kontrolleri yapılır.
* **Frontend Katmanı:** `canAccessElyafTower` ve `elyafAccess.ts` yardımcıları ile menü linkleri ve sayfalar gizlenir; ancak asıl denetim her zaman Server Components tarafında API çağrısında yapılır.
* **Workflow / Plugin Katmanı:** Dynamic workflow engine veya harici sandbox eklentiler çalışmadan önce token üzerinden permission doğrulamasından geçmek zorundadır.

Bu doküman platformdaki tüm yetkilendirme şemasının teknik temelidir.
