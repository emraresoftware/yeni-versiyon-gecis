# 🔒 CRM Güvenlik ve Yetkilendirme Denetimi (CRM_SECURITY_REVIEW_TASK_013A.md)

**Title:** CRM Güvenlik ve Yetkilendirme Denetimi — Task 013A  
**Version:** 1.1.0  
**Status:** Approved  
**Owner:** Agent 4 — CRM Security & Permission Review  
**Last Updated:** 2026-06-28  
**Dependencies:** SECURITY_AUTHORIZATION.md, TASK_013_CRM_FOUNDATION_PLAN.md  
**Related Documents:** DOMAIN_MODEL.md, SECURITY_REVIEW.md, ANAYASA.md

---

## 📌 Amaç

Bu denetim raporu, **Emare Ai Dashboard** platformunda Sprint 2A kapsamında geliştirilen CRM Modülü çekirdek yapısının (CRM Foundation) yetkilendirme şemasını incelemek ve planlanan izinlerin (permissions) kurumsal güvenlik standartlarına ([SECURITY_AUTHORIZATION.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_AUTHORIZATION.md)) uyumluluğunu değerlendirmek amacıyla **Agent 4** tarafından güncellenmiştir. 

Task 013A kapsamında yapılan sıkılaştırma (hardening) düzeltmeleri ve izin matrisi güncellemeleri sonrasında güvenlik durumu yeniden değerlendirilmiştir.

---

## 📊 1. İzin Karşılaştırma Matrisi (Permission Set vs. SECURITY_AUTHORIZATION.md)

CRM yetki seti ile `SECURITY_AUTHORIZATION.md` üzerinde güncellenmiş izin matrisi karşılaştırılmıştır:

| İzin Adı (Permission Constant) | SECURITY_AUTHORIZATION.md Durumu | Varsayılan Rol Sınırları (Default Roles) | Kapsam (Scope) | Durum Analizi ve Bulgular |
| :--- | :---: | :--- | :---: | :--- |
| **`CRM.Account.Read`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, FinanceManager, HRManager, QCManager, LogisticsManager, Employee | Tenant | Cari hesap listesini okuma. |
| **`CRM.Account.Write`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Cari oluşturma/düzenleme. |
| **`CRM.Contact.Read`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | İletişim kişisi okuma. |
| **`CRM.Contact.Write`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | İletişim kişisi yazma. |
| **`CRM.Opportunity.Read`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Satış fırsatlarını okuma. (Matrise başarıyla eklendi). |
| **`CRM.Opportunity.Write`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Satış fırsatı yazma. (Matrise başarıyla eklendi). |
| **`CRM.Proposal.Read`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, FinanceManager | Tenant | Teklifleri okuma. |
| **`CRM.Proposal.Write`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Teklif oluşturma. |
| **`CRM.Proposal.Approve`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager | Tenant | Teklif onaylama. |
| **`CRM.Activity.Read`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Cari aktivite günlüklerini okuma. (Matrise başarıyla eklendi). |
| **`CRM.Activity.Write`** | 🟢 Tanımlı (Ok) | SystemAdmin, TenantAdmin, CEO, SalesManager, Employee | Tenant | Cari aktivite günlüğü yazma. (Matrise başarıyla eklendi). |

### 🛠️ Giderilen Açıklar (Gap Resolution):
*   Önceki raporda eksik olduğu tespit edilen **4 izin** (`CRM.Opportunity.Read/Write` ve `CRM.Activity.Read/Write`), `SECURITY_AUTHORIZATION.md` dosyasına başarıyla eklenmiş ve rolleri kilitlenmiştir. 
*   `Permissions.cs` dosyasında bu yetkilere karşılık gelen tüm C# sabitleri tanımlanmış ve Persistence test katmanında doğrulanmıştır.

---

## 🔒 2. Güvenlik Risk Değerlendirmeleri ve Kontroller

### 2.1. Tenant Isolation (Kiracı İzolasyonu)

*   **Değerlendirme:**
    *   `EmareDbContext.cs` üzerinde yansıma (reflection) kullanılarak tasarlanan `ApplyGlobalQueryFilters` metodu, `IHasTenant` arayüzünü (interface) uygulayan tüm sınıfları otomatik olarak filtrelemektedir.
    *   Tüm CRM sınıfları (`CrmAccount`, `CrmContact`, `CrmOpportunity`, `CrmProposal`, `CrmProposalItem`, `CrmActivity`) `IHasTenant` arayüzünü uyguladığından, EF Core seviyesinde otomatik izolasyon altına alınmıştır.
    *   `CrmPersistenceTests.cs` altındaki `CrmEntities_MultiTenancy_IsolationWorks` integration testi ile kiracılar arası izolasyonun (Tenant A verisine Tenant B'nin erişememesi durumu) hatasız çalıştığı doğrulanmıştır.
*   **Kalan Risk ve Tavsiye:**
    *   Ham SQL veya Dapper üzerinden yazılapbilecek Control Tower sorgularında query filter devreye girmediğinden, bu sorgularda `TenantId` filtresinin elle yazılması zorunlu tutulmalıdır.

---

### 2.2. Proposal Approval Permission (Teklif Onay Yetkisi)

*   **Değerlendirme:**
    *   `CRM.Proposal.Approve` yetkisi C# tarafında ve izin matrisinde kilitlenmiştir.
    *   Sadece `SystemAdmin`, `TenantAdmin`, `CEO` ve `SalesManager` rolleri teklif onaylama hakkına sahiptir. Düşük yetkili `Employee` veya harici `Auditor` rollerinin bu yetkiye erişimi engellenmiştir.
*   **Güvenlik Tavsiyesi:**
    *   Büyük tutarlı tekliflerin onayında (örn: 100.000 USD üzeri), `ApproveCrmProposalCommand` içerisinde ABAC kuralı tetiklenmeli ve `SalesManager` yetkisi olsa dahi sadece `CEO` veya `TenantAdmin` onayı aranmalıdır.

---

### 2.3. Customer Health / Risk Score Erişimi

*   **Değerlendirme:**
    *   `CrmAccount.cs` üzerinde `Segment` (Segmentasyon), `NpsScore` (Memnuniyet), `RiskScore` (Risk) ve `HealthScore` (Sağlık) alanları implemente edilmiş ve validasyon kuralları (Risk/Health için 0-100, NPS için 0-10 aralıkları) eklenmiştir.
*   **Riskler:**
    *   `CRM.Account.Read` iznine sahip olan ve aralarında standart çalışanların da bulunduğu geniş bir rol grubu, varsayılan olarak tüm müşterilerin hassas ticari risk skorlarını (`RiskScore`) ve finansal segment bilgilerini okuyabilir.
*   **Önerilen Önlem:**
    *   API katmanında dönen DTO mapping işlemlerinde (`CrmAccountDto`), `RiskScore` ve `HealthScore` alanları sadece `CEO`, `SalesManager` veya `FinanceManager` rollerine sahip kullanıcılara doldurulmalı; diğer roller için `null` veya maskelenmiş olarak gönderilmelidir (DTO-level property authorization).

---

### 2.4. AI Permission Bypass Riski (Yapay Zekâ Yetki Aşımı)

*   **Değerlendirme:**
    *   AI Ajanları doğrudan veritabanına erişemez. MediatR pipeline'ı üzerinden yetki kontrolüne tabidir.
    *   AI otonom karar veremez; sadece onay önerisi üretebilir (Proposal approved action can only be completed by authorized human supervisor).
*   **Tavsiye:**
    *   AI servislerinin (Copilot vb.) veri getirdiği sorgularda, arka planda çalışan MediatR handler'ları kullanıcının token context'ini birebir taşımalıdır (claims principal propagation). AI tetikleyicisi kim ise, yetki denetimi o kullanıcının sınırlarında yapılmalıdır.

---

## 🏁 3. Sonuç (Final Verdict)

### **PASS (GEÇTİ)**

*CRM modülünün tüm yetkilendirme şeması, kiracı izolasyonu ve veri modelleri kurumsal güvenlik mimarisine uygun hale getirilmiştir. Geliştirme sürecinin bu standartlar dahilinde başlatılması güvenlik açısından onaylanmıştır.*
