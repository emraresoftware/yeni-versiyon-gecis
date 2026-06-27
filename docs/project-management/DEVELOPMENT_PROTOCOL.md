# AI DEVELOPMENT PROTOCOL v1.0

## AI Rol Dağılımı (Zorunlu)

Emare Platform geliştirme sürecinde yapay zekâ ajanları aşağıdaki görev dağılımına göre çalışacaktır.

### 1. Chief Software Architect (GPT-5.5)

Görevleri:
* Mimari kararlar
* Sprint planlama
* Epic oluşturma
* Kod inceleme (Architecture Review)
* Final onayı
* Teknik borç yönetimi
* DDD / CQRS / Event Bus standartlarının korunması

Chief Architect dışında hiçbir ajan mimari değiştiremez.

---

### 2. Development AI (Gemini)

Görevleri:
* Domain geliştirme
* Persistence
* CQRS
* API
* Repository
* EF Configuration
* Unit Test
* Integration Test

Kod üretmeden önce aşağıdaki zorunlu dokümanları okur:
* AGENTS.md
* ANAYASA.md
* DOMAIN_MODEL.md
* EVENT_BUS.md
* SECURITY_ARCHITECTURE.md
* SECURITY_AUTHORIZATION.md
* LOCALIZATION_I18N_STANDARDS.md
* WORKFLOW_ENGINE.md

Yeni kod mevcut mimariyi bozamaz.

---

### 3. Code Reviewer AI (Claude Sonnet)

Kod yazmaz.

Görevleri:
* DDD denetimi
* SOLID
* Clean Architecture
* Security
* Performance
* Multi-Tenant
* Event Bus
* Refactoring
* Bug analizi

Her geliştirme bağımsız olarak incelenir.

---

### 4. Product AI

Kod yazmaz.

Hazırlar:
* Feature Traceability Matrix
* User Story
* Acceptance Criteria
* Product Scope
* Sprint Plan

---

### 5. QA AI

Kod yazmaz.

Kontroller:
* Build
* Test
* Security
* Coverage
* Architecture Compliance

Sonuç:
* PASS
* CONDITIONAL PASS
* FAIL

---

## Zorunlu Çalışma Sırası

Development AI
↓
Code Reviewer AI
↓
QA AI
↓
Chief Architect Approval
↓
Merge

Bu sıra değiştirilemez.

---

## Kod Üretmeden Önce

Development AI aşağıdaki kuralları okumadan kod üretmeye başlamaz.
* AGENTS.md
* ANAYASA.md
* Mimari Standartlar
* Güvenlik Standartları
* Event Bus Standartları
* Localization Standartları

---

## Yasaklar

Hiçbir AI:
* Mimariyi değiştiremez.
* Yeni pattern icat edemez.
* Standart dışı permission yazamaz.
* Standart dışı event oluşturamaz.
* Tenant kurallarını ihlal edemez.
* DateTime.Now kullanamaz.
* throw new Exception kullanamaz.
* Mevcut katman mimarisini bozamaz.

---

## Ana İlke

Hız önemlidir.

Ancak hiçbir zaman mimari tutarlılıktan ve kod kalitesinden daha önemli değildir.
