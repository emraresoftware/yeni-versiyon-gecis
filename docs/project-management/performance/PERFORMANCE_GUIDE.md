# 🚀 Emare BOS Performans ve Ölçeklenebilirlik Kılavuzu (PERFORMANCE_GUIDE.md)

**Title:** Performans ve Ölçeklenebilirlik Kılavuzu  
**Version:** 1.0.0  
**Status:** Draft  
**Owner:** Agent 4 — Performance Review  
**Last Updated:** 2026-06-27  
**Dependencies:** DOMAIN_MODEL.md, EVENT_BUS.md, WORKFLOW_ENGINE.md, ANAYASA.md

---

## 📌 Amaç ve Kapsam

Bu kılavuz, **Emare Business Operating System (BOS)** platformunda yüksek performans, düşük gecikme süresi (latency) ve yüksek ölçeklenebilirlik sağlamak amacıyla geliştiricilere ve AI ajanlarına yönelik teknik standartları ve stratejileri tanımlar. 

Kılavuz hazırlanırken [DOMAIN_MODEL.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/DOMAIN_MODEL.md), [EVENT_BUS.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/EVENT_BUS.md) ve [WORKFLOW_ENGINE.md](file:///Users/emre/Elyafgroup/Yeni%20versiyon%20ge%C3%A7i%C5%9F/WORKFLOW_ENGINE.md) dokümanları referans alınmış; PostgreSQL, Redis, EF Core ve CQRS bileşenlerinin proje gereksinimlerine göre en verimli şekilde entegre edilmesi hedeflenmiştir.

---

## 🗂️ Performans Stratejileri

### 1. Database Index Strategy (Veritabanı İndeks Stratejisi)

* **Recommendation (Öneri):**
  * **Composite Tenant-Specific Indexes (Çoklu Kiracı İndeksleri):** Emare BOS multi-tenant bir mimari olduğundan ve tüm sorgularda `TenantId` zorunlu olduğundan, veritabanı indeksleri mutlaka `TenantId` ile başlamalıdır.
    * *Örnek:* `CrmProposal` tablosunda `CrmAccountId` üzerinden filtreleme yaparken composite indeks oluşturun: `IX_CrmProposals_TenantId_CrmAccountId` (sadece `CrmAccountId` üzerinde tekil indeks kullanmayın).
  * **Partial/Filtered Indexes (Filtrelenmiş İndeksler):** Sistemde soft delete (`IsDeleted = true/false`) standarttır. Silinmemiş aktif kayıtları hedefleyen sorguların performansı için kısmi indeksler (partial indexes) kullanılmalıdır.
    * *Örnek SQL:* 
      ```sql
      CREATE INDEX IX_CrmAccount_TenantId_Active 
      ON "CrmAccounts" ("TenantId", "Id") 
      WHERE "IsDeleted" = false;
      ```
  * **Foreign Key Composite Indexes (Yabancı Anahtar İndeksleri):** Aggregate sınırları arasındaki ilişkilerde (örn: `FinanceJournalEntryLine` tablosundaki `FinanceJournalEntryId` logical FK'sı) sorgu hızını korumak için composite FK indeksleri tanımlanmalıdır.
* **Expected Gain (Beklenen Kazanım):**
  * Tenant bazlı veri izolasyon sorgularında %70-80 oranında gecikme (latency) azalması.
  * Silinmiş veriler (soft deleted) taranmayacağı için disk I/O ve RAM tüketiminde ciddi düşüş.
  * Tablo taramalarının (Full Table Scan) tamamen engellenmesi ve `Index Scan` kullanımının garanti edilmesi.
* **Priority (Öncelik):** **Critical**

---

### 2. Redis Strategy (Redis Stratejisi)

* **Recommendation (Öneri):**
  * **Tenant-Isolated Key Naming Standard:** Redis anahtarlarının çakışmaması ve güvenlik sınırı için şu şablon kullanılmalıdır: `emare:tenant:{tenantId}:{module}:{entity}:{key}`
    * *Örnek:* `emare:tenant:d3b07384:crm:account:1001`
  * **Hash Data Structures for Complex Objects:** Nesnelerin tamamını JSON string olarak Redis'e yazmak yerine, nesne alanlarına kısmi erişim gerekiyorsa `Redis Hash` veri yapısı tercih edilmelidir.
  * **Eviction Policy (Bellek Tahliye Politikası):** Redis sunucusunun OOM (Out of Memory) hatası alıp çökmesini önlemek için tahliye politikası `volatile-lru` (TTL'i olan en eski kullanılan anahtarları sil) veya `allkeys-lru` olarak yapılandırılmalıdır.
  * **Multiplexer Lifecycle:** `IConnectionMultiplexer` nesnesi .NET DI konteynerinde `Singleton` olarak kaydedilmeli ve `ConnectRetry=5`, `KeepAlive=60`, `SyncTimeout=5000` parametreleriyle yapılandırılmalıdır.
* **Expected Gain (Beklenen Kazanım):**
  * Oturum (Session) ve yetki (Permission) doğrulamalarında 1ms'nin altında yanıt süreleri.
  * Bellek sızıntılarının ve sunucu kaynak yetersizliği nedeniyle oluşabilecek kesintilerin önüne geçilmesi.
* **Priority (Öncelik):** **High**

---

### 3. Cache Strategy (Önbellekleme Stratejisi)

* **Recommendation (Öneri):**
  * **Hybrid (L1/L2) Caching Pattern:** 
    * **L1 (In-Memory / Local Cache):** Çok sık okunan ve nadir değişen veriler (Yetki listeleri, `HrLeaveType` listesi, `QcStandard` tanımları, Tenant ayarları) API sunucusunun RAM'inde `IMemoryCache` ile tutulmalıdır (TTL: 1-5 dk).
    * **L2 (Distributed Cache / Redis):** Kiracı bazlı dinamik veriler, aktif workflow durumları ve kullanıcı oturumları Redis üzerinde tutulmalıdır (TTL: 30 dk - 24 saat).
  * **Event-Driven Cache Invalidation (Olay Güdümlü Geçersiz Kılma):** Bir metadata veya tanım değiştiğinde (örn: `QcStandard` güncellendiğinde), Event Bus üzerinden `QcStandardUpdated` event'i yayınlanmalı ve tüm API instance'larındaki L1 cache'ler temizlenmelidir.
  * **Cache Stampede (Thundering Herd) Prevention:** Cache süresi dolduğunda veritabanına aynı anda yüzlerce sorgunun gitmesini engellemek için `SemaphoreSlim` veya `LazyCache` kütüphanesi ile kilitleme (locking) mekanizması uygulanmalıdır.
* **Expected Gain (Beklenen Kazanım):**
  * Statik veritabanı okumalarında %95 oranında azalma.
  * API sunucuları arasında anlık ve tutarlı önbellek geçersiz kılma.
  * Yoğun yük altında veritabanı darboğazlarının (CPU spike) önlenmesi.
* **Priority (Öncelik):** **High**

---

### 4. CQRS Read Optimization (CQRS Okuma Optimizasyonu)

* **Recommendation (Öneri):**
  * **Strict AsNoTracking Rule:** Tüm read query handler'larında (`Get*Query` ve `List*Query`) EF Core sorgularına `.AsNoTracking()` eklenmelidir.
  * **Direct DTO Projection (SQL SELECT Limit):** Domain entity'leri doğrudan çekip bellekte DTO'ya map etmek yerine, EF Core üzerinden `.Select()` veya AutoMapper `ProjectTo<DTO>()` kullanılarak yalnızca arayüze dönecek kolonların SQL seviyesinde çekilmesi sağlanmalıdır.
  * **Dapper for Heavy Queries / Dashboards:** CEO Dashboard KPI analitikleri (`DecisionLogs` analizleri gibi) ve büyük finansal raporlar (`FinanceJournalEntry` dökümleri) için EF Core yerine doğrudan **Dapper** ve read-replica veritabanı bağlantısı kullanılmalıdır.
* **Expected Gain (Beklenen Kazanım):**
  * Bellek (Memory) tüketiminde %50 ve CPU yükünde %40 tasarruf (Entity Change Tracker devre dışı bırakıldığı için).
  * SQL sorgularında gereksiz kolonların (örn: büyük metinler, loglar, binary metadata) ağ üzerinden taşınmasının engellenmesi.
* **Priority (Öncelik):** **Critical**

---

### 5. Event Throughput (Event İşleme Kapasitesi)

* **Recommendation (Öneri):**
  * **Outbox Pattern Batching & Skip Locked:** Outbox tablosundan event'leri okuyup Event Bus'a gönderen arka plan işleyicisi (Outbox Poller), verileri toplu (Batch size: 100-500) çekmeli ve PostgreSQL `FOR UPDATE SKIP LOCKED` ifadesini kullanarak paralel çalışan poller'ların kilitlenmesini engellemelidir.
  * **Non-Blocking Async Subscribers:** Event handler'ların tamamı asenkron olmalıdır. Uzun süren entegrasyon veya SMS/E-posta gönderimi gibi işlemler (örn: `CrmProposalSent` veya `HrLeaveApproved` esnasında e-posta tetiklenmesi) handler içinde doğrudan bekletilmemeli, bir arka plan kuyruğuna (Hangfire / MQ Queue) aktarılmalıdır.
  * **Aggregate-Based Partitioning:** RabbitMQ/Kafka geçişinde event mesajlarının partition key'i `AggregateId` (örn: `SalesOrderId`) olarak ayarlanmalıdır. Böylece aynı siparişe ait event'ler (Created -> Approved -> Completed) sırayla işlenirken, farklı siparişler paralel işlenebilir.
* **Expected Gain (Beklenen Kazanım):**
  * Saniyede 2000+ event işleme kapasitesine ulaşılması.
  * E-posta/SMS servislerindeki gecikmelerin ana veritabanı transaction sürelerini etkilemesinin önlenmesi.
  * Outbox tablosunun şişmesini önleme ve tutarlı event yayımı.
* **Priority (Öncelik):** **High**

---

### 6. EF Core Performance (EF Core Performans Kuralları)

* **Recommendation (Öneri):**
  * **DbContext Pooling:** API katmanında DbContext kaydı yapılırken `AddDbContextPool<AppDbContext>(options => ...)` kullanılmalıdır. Bu sayede her HTTP request için yeni DbContext oluşturma maliyeti sıfıra indirilir.
  * **Explicit Split Queries:** Bir sorguda birden fazla `.Include()` veya koleksiyon yüklemesi varsa, Cartesian product (Kartezyen çarpım) oluşmasını engellemek için `.AsSplitQuery()` ifadesi açıkça belirtilmelidir.
    * *Örnek:* `CrmProposal` + `CrmProposalItems` + `CrmContact` ilişkili sorgusunda split query kullanılmalıdır.
  * **EF Core 8 Bulk Operations:** Toplu veri güncellemelerinde entity'leri memory'e çekip döngüyle güncellemek yerine, EF Core 8 ile gelen `ExecuteUpdateAsync` ve `ExecuteDeleteAsync` metotları kullanılmalıdır.
    * *Örnek:* Belirli bir tarihten önceki taslak teklifleri silmek için:
      ```csharp
      await context.CrmProposals
          .Where(x => x.TenantId == tenantId && x.Status == ProposalStatus.Draft && x.CreatedAt < thresholdDate)
          .ExecuteDeleteAsync(cancellationToken);
      ```
* **Expected Gain (Beklenen Kazanım):**
  * DbContext pooling ile yüksek eşzamanlı yüklerde CPU tüketiminde %10-15 azalma.
  * Split query kullanımıyle veritabanından çekilen veri boyutunda (data volume) %90'a varan azalma.
  * Toplu güncellemelerde 10x-100x işlem hızı artışı.
* **Priority (Öncelik):** **High**

---

### 7. N+1 Riskleri (N+1 Sorgu Riskleri ve Önlenmesi)

* **Recommendation (Öneri):**
  * **Disable Lazy Loading:** Projede lazy loading (tembel yükleme) özellikleri tamamen kapalı tutulmalıdır. İlişkili veriler yalnızca Eager Loading (`.Include()`) veya Projection (`.Select()`) ile çekilmelidir.
  * **Architectural Architecture Tests:** `NetArchTest` özelliğini kullanarak, repository ve handler katmanları dışında (özellikle API Controller veya UI mapping sınıflarında) DB sorgulaması veya entity navigation property çağrımı yapılması engellenmelidir.
  * **Interceptor-Based Alerting:** Geliştirme ortamında (Development), tek bir HTTP isteğinde veritabanına atılan sorgu sayısı 10'u geçtiğinde loglara uyarı yazan veya hata fırlatan bir `DbCommandInterceptor` entegre edilmelidir.
* **Expected Gain (Beklenen Kazanım):**
  * Geliştirme aşamasında gözden kaçan ve canlı ortamda (production) veri miktarı arttıkça sistemi kilitleyen N+1 sorgu zincirlerinin %100 engellenmesi.
  * Yanıt sürelerinin öngörülebilir ve stabil kalması.
* **Priority (Öncelik):** **Critical**

---

### 8. Async Guidelines (Asenkron Kodlama Kılavuzu)

* **Recommendation (Öneri):**
  * **CancellationToken Propagation (İptal Belirteci Yayılımı):** API Controller seviyesinden başlayarak MediatR handler, application service ve repository katmanlarına kadar tüm asenkron metot imzalarına `CancellationToken ct` parametresi eklenmeli ve EF Core asenkron çağrılarına iletilmelidir (`ToListAsync(ct)`, `SaveChangesAsync(ct)` vb.).
  * **No Blocking Calls:** Kod tabanında `.Result`, `.Wait()`, veya `.GetAwaiter().GetResult()` kullanılması kesinlikle yasaktır. Bu bloklamalar ThreadPool thread'lerini tüketerek kilitlenmelere (Deadlock) yol açar.
  * **ConfigureAwait(false) Usage:** UI bağımlılığı olmayan Infrastructure ve Persistence projelerinde, asenkron await işlemlerine `.ConfigureAwait(false)` eklenerek ASP.NET Core senkronizasyon bağlamı (Synchronization Context) üzerindeki yük hafifletilmelidir.
  * **Task.WhenAll for Parallel I/O:** Bir handler içinde birbirinden bağımsız iki I/O işlemi yapılıyorsa (örn: hem `CrmAccount` verisini doğrulamak hem de `LogisticsWarehouse` durumunu sorgulamak), bunları sırayla await etmek yerine paralel başlatıp `Task.WhenAll` ile beklenmelidir.
* **Expected Gain (Beklenen Kazanım):**
  * Thread Pool Starvation (Thread Havuzu Açlığı) kaynaklı uygulama kilitlenmelerinin sıfıra indirilmesi.
  * Sunucu kaynaklarının (özellikle CPU ve RAM) yoğun istek altında verimli kullanılması.
  * Bağımsız I/O işlemlerinin paralel çalışmasıyla endpoint yanıt sürelerinin düşmesi.
* **Priority (Öncelik):** **Critical**

---

### 9. Pagination Standard (Sayfalama Standardı)

* **Recommendation (Öneri):**
  * **Keyset (Cursor) Pagination for High Volume:** Yüksek veri hacmine sahip akış tablolarda (örn: `LogisticsStockMovement`, `AuditLog`, `Calls/TelephonyEvents`), klasik offset sayfalama (`Skip/Take`) yerine cursor tabanlı sayfalama (Keyset Pagination) zorunlu tutulmalıdır.
    * *Örnek sorgu:* `Where(x => x.CreatedAt < lastItemTimestamp && x.Id < lastItemId).OrderByDescending(x => x.CreatedAt).Take(pageSize)`
  * **Offset Pagination Restrictions:** Düşük hacimli tanımlama tablolarında (örn: `HrLeaveType`, `QcStandard`) offset sayfalama kullanılabilir ancak maksimum sayfa sınırı konulmalıdır (örn: max 100 sayfa veya 5000 kayıt).
  * **Deferred Joins (Ertelenmiş Join):** Klasik offset sayfalama kullanılacaksa ve satır boyutu genişse, önce sadece ID'ler çekilmeli (`Select(x => x.Id).Skip(1000).Take(50)`), ardından bu ID'lere sahip satırlar join ile çekilmelidir.
* **Expected Gain (Beklenen Kazanım):**
  * Milyonlarca satırlık tablolarda son sayfalara gidildiğinde sorgu performansının düşmesinin önlenmesi (Keyset pagination her zaman \(O(1)\) veya \(O(\log N)\) indeks hızında çalışır).
  * Veritabanı disk I/O yükünün minimize edilmesi.
* **Priority (Öncelik):** **High**

---

### 10. Benchmark Plan (Performans Test Planı)

* **Recommendation (Öneri):**
  * **Micro-benchmarks (BenchmarkDotNet):** Event serialization/deserialization motoru, Rule Engine mantıksal ağaç değerlendirmeleri ve custom JSON mapper yazılımları için `BenchmarkDotNet` kütüphanesiyle test sınıfları yazılmalı, CI/CD pipeline'ına eşik (threshold) kontrolleri eklenmelidir.
  * **Integration / Load Tests (k6 / Locust):** API üzerinde en kritik iş süreçleri (End-to-End) için yük test senaryoları tasarlanmalıdır:
    * *Senaryo A (Yoğun Yazma):* Eşzamanlı 500 kullanıcının `CrmProposalCreated` -> `Approved` workflow sürecini tetiklemesi.
    * *Senaryo B (Yoğun Okuma):* Eşzamanlı 2000 kullanıcının dashboard KPI metriklerini ve proposal listelerini filtrelemesi.
  * **Performance Budget (Performans Bütçesi):** Sistem için aşağıdaki KPI bütçeleri kabul edilmeli ve aşılması durumunda build başarısız sayılmalıdır:
    * **P95 Latency (Read):** < 150ms
    * **P99 Latency (Write/Command):** < 400ms
    * **Event Processing Latency:** < 500ms (Event yayılma ve kuyrukta kalma süresi)
* **Expected Gain (Beklenen Kazanım):**
  * Canlıya çıkış öncesinde performans darboğazlarının erkenden tespit edilmesi.
  * Kod değişikliklerinin performansa etkisinin sayısal ve bilimsel olarak ölçülebilmesi.
* **Priority (Öncelik):** **Medium**

---

## 🛠️ Uygulama ve Denetim

Emare BOS platformunda görev alan tüm AI ajanları ve yazılımcılar, yazdıkları her repository metodunda, MediatR handler'ında ve veritabanı migration dosyasında bu kılavuzdaki kuralları **birebir uygulamakla yükümlüdür**. 

QA ajanları (`Agent 2`), her task sonundaki incelemelerinde bu kılavuzu referans alarak performans değerlendirmesi yapacak ve kurallara uymayan kodları doğrudan **FAIL** verdict ile geri çevirecektir.
