# 👨💻 Developer Platform Mimarisi

## Amaç

Developer Platform, Emare Business Operating System (BOS) için geliştirici deneyimini (Developer Experience - DX) standartlaştıran platform katmanıdır.

Amaç;

* hızlı geliştirme,
* ortak kod standartları,
* eklenti geliştirme,
* API yönetimi,
* SDK desteği,
* otomatik kod üretimi

sağlamaktır.

---

# Temel Mimari

```text
Developer

↓

CLI

↓

SDK

↓

Code Generator

↓

Plugin SDK

↓

BOS Platform
```

---

# Platform Bileşenleri

## CLI

Komut satırı aracı.

Örnek komutlar

```bash
bos new module Sales

bos new entity Customer

bos new workflow PurchaseApproval

bos new plugin WarehouseAI

bos build

bos validate

bos publish
```

---

## Code Generator

Otomatik oluşturabilir.

* Entity
* DTO
* Validator
* Repository
* Service
* API Controller
* React Page
* Form
* Unit Test

Kod üretimi metadata tabanlıdır.

---

## SDK

Desteklenen diller

* .NET
* JavaScript
* TypeScript
* Python
* Java
* Go

---

## Plugin SDK

Plugin geliştiricileri için.

Desteklenen bileşenler

* Menu
* Dashboard
* Widget
* API
* Workflow
* Event Subscriber
* AI Agent

---

# API Geliştirme

Desteklenen yapılar

* REST
* GraphQL
* Webhook
* gRPC

API sözleşmeleri OpenAPI üzerinden yayınlanır.

---

# Kod Standartları

Zorunlu

* Clean Architecture
* SOLID
* Async/Await
* Result Pattern
* Dependency Injection
* UTC DateTime
* Tenant Isolation

---

# Test Altyapısı

Desteklenen testler

* Unit Test
* Integration Test
* API Test
* UI Test
* Performance Test
* Load Test

CLI üzerinden çalıştırılabilir.
```

---

# Dokümantasyon

Her modül otomatik olarak;

* API
* Entity
* Event
* Workflow
* Permission

dokümantasyonunu üretebilir.

---

# Versioning

Her SDK ve Plugin;

* Semantic Versioning
* Backward Compatibility
* Deprecation Policy

kurallarına uyar.

---

# Geliştirici Portalı

Portal üzerinden;

* Dokümantasyon
* API Explorer
* SDK İndirme
* Örnek Kodlar
* Plugin Yayınlama
* Paket Yönetimi

sunulur.

---

# Güvenlik

Geliştirici erişimleri; API Key, OAuth2, RBAC ve Audit Log ile korunur. Bu konu için ana kaynak: [SECURITY_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_ARCHITECTURE.md).

---

# Temel Mimari İlkeleri

* Tekrarlanan kod otomatik üretilmelidir.
* Geliştiriciler ortak standartlara uymalıdır.
* SDK ve CLI platformun resmi geliştirme araçlarıdır.
* Kod üretimi metadata ve sözleşmeler üzerinden yapılmalıdır.
* Tüm geliştirmeler sürümlenebilir ve denetlenebilir olmalıdır.

---

# Nihai Vizyon

Developer Platform sayesinde Emare BOS;

* yeni modüllerin,
* yeni entegrasyonların,
* yeni AI ajanlarının,
* yeni eklentilerin

hızlı, güvenli ve standart şekilde geliştirilebildiği kurumsal bir geliştirme ekosistemine dönüşür.
