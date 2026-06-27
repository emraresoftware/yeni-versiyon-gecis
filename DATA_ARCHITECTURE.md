# 🗄️ Data Architecture

## Amaç

Data Architecture, Emare Business Operating System (BOS) platformundaki tüm verilerin yaşam döngüsünü, depolanmasını, erişimini, güvenliğini ve yönetimini tanımlar.

Bu doküman yalnızca veritabanını değil;

* OLTP
* OLAP
* Event Store
* Cache
* Search
* Object Storage
* AI Knowledge
* Data Lake

katmanlarını kapsar.

---

# Veri Katmanları

```text
Applications
        │
Business Engines
        │
Repositories
        │
──────────────────────────────
OLTP Database
──────────────────────────────
Event Store
──────────────────────────────
Cache
──────────────────────────────
Search Index
──────────────────────────────
Object Storage
──────────────────────────────
Data Warehouse
──────────────────────────────
Data Lake
──────────────────────────────
AI Knowledge Store
```

Her katmanın amacı farklıdır.

---

# OLTP (Transactional Database)

Operasyonel veriler burada tutulur.

Teknoloji (varsayılan)

* PostgreSQL

Örnek tablolar

* Customer
* Product
* SalesOrder
* JournalEntry
* Employee
* Warehouse
* StockMovement

Kurallar

* ACID
* UTC DateTime
* Foreign Key
* Optimistic Concurrency
* Soft Delete
* Audit

---

# Event Store

Tüm Domain Event'ler saklanır.

Örnek

```text
CustomerCreated
SalesOrderApproved
StockReserved
InvoicePosted
```

Amaç

* Audit
* Replay
* Analytics
* AI Learning

---

# Cache Layer

Teknoloji

* Redis

Kullanım

* Session
* Permission
* Metadata
* Dashboard
* Frequently Used Data

Kurallar

* TTL
* Cache Invalidation
* Tenant Isolation

---

# Search Engine

Teknoloji

* OpenSearch
* Elasticsearch

Arama yapılabilecek örnek alanlar

* Customer
* Product
* Invoice
* Document
* Ticket
* Knowledge Base

---

# Object Storage

Dosyalar burada tutulur.

Desteklenebilir

* S3
* Azure Blob
* MinIO

Dosya türleri

* PDF
* Excel
* Images
* CAD
* Videos
* Contracts

Metadata veritabanında tutulur.

Dosya binary olarak Object Storage'da tutulur.

---

# Data Warehouse

Analitik veriler.

Katmanlar

```text
Raw

↓

Staging

↓

Business

↓

Analytics
```

Amaç

* KPI
* BI
* Forecast
* AI Analytics

---

# Data Lake

Yapısal olmayan büyük veri.

Örnek

* IoT
* PLC
* Log
* OCR
* Kamera
* Sensör
* AI Eğitim Verisi

---

# AI Knowledge Store

RAG sistemi için.

İçerik

* SOP
* Dokümanlar
* Eğitim
* Sözleşmeler
* Politika
* Wiki

Vector Database desteği planlanmalıdır.

Örnek teknolojiler

* pgvector
* Qdrant
* Milvus
* Pinecone

---

# Veri Yaşam Döngüsü

```text
Create

↓

Update

↓

Archive

↓

Retention

↓

Delete
```

Her adım politikaya tabidir.

---

# Master Data Management (MDM)

Merkezi yönetilecek veriler

* Customer
* Supplier
* Product
* Employee
* Currency
* Tax
* Unit
* Warehouse

Tek doğruluk kaynağı (Single Source of Truth) esas alınır.

---

# Data Quality

Kontroller

* Duplicate Detection
* Mandatory Fields
* Reference Integrity
* Business Validation
* AI Assisted Cleansing

---

# Veri Saklama Politikası

Her veri tipi için

* Retention
* Archive
* Purge

kuralları tanımlanır.

Örnek

* Audit: 10 yıl
* Finans: Yasal gerekliliklere göre
* Log: 90 gün (örnek varsayılan, tenant politikasıyla değiştirilebilir)
* AI Prompt Log: Politika bazlı

---

# Çok Kiracılı Veri Modeli

Her kayıt

* TenantId
* CreatedAtUtc
* UpdatedAtUtc
* CreatedBy
* UpdatedBy
* RowVersion

alanlarını içerir.

Hiçbir sorgu Tenant filtresi olmadan çalışmaz.

---

# Veri Güvenliği

Desteklenir

* Encryption At Rest
* Encryption In Transit
* Row Level Security
* Column Masking
* Immutable Audit
* Backup Encryption

---

# Veri Entegrasyonu

Veri aşağıdaki katmanlardan gelebilir.

* REST
* GraphQL
* Webhook
* Kafka
* RabbitMQ
* CSV
* Excel
* ERP Connector

---

# Veri İzleme

İzlenecek metrikler

* DB Size
* Growth Rate
* Index Usage
* Slow Queries
* Deadlocks
* Connection Pool
* Cache Hit Ratio

---

# Backup ve Recovery

Desteklenir

* Full Backup
* Incremental Backup
* Point-in-Time Recovery
* Geo Replication
* Immutable Backup

Recovery testleri düzenli yapılmalıdır.

---

# Performans İlkeleri

* Read/Write ayrımı desteklenebilir.
* Büyük raporlar OLTP üzerinde çalıştırılmaz.
* Sık erişilen metadata cache'lenir.
* Event'ler Analytics'e asenkron aktarılır.
* Search Index operasyonel sorguların yerine kullanılmaz.

---

# İlgili Dokümanlar

* ERP_MIMARISI.md
* EVENT_BUS.md
* ANALYTICS_ENGINE.md
* METADATA_ENGINE.md
* SECURITY_ARCHITECTURE.md
* OBSERVABILITY.md
* INTEGRATION_ENGINE.md

---

# Nihai Vizyon

Data Architecture sayesinde Emare BOS;

* operasyonel veriyi,
* analitik veriyi,
* AI bilgisini,
* olay geçmişini,
* dosya yönetimini,
* arama altyapısını

tek bir kurumsal veri mimarisi altında yönetebilen, ölçeklenebilir ve geleceğe hazır bir Business Operating System olur.

Veri, platformun en değerli varlığıdır ve bu mimari tüm Business Engine'ler için ortak referans olarak kabul edilir.
