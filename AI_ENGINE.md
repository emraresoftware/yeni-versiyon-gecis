# 🤖 AI Engine Mimarisi

**Title:** AI Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** EVENT_BUS.md
**Related Documents:** WORKFLOW_ENGINE.md, INTEGRATION_ENGINE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

AI Engine, Emare Business Operating System (BOS) içerisindeki tüm yapay zekâ yeteneklerini yöneten merkezi platformdur.

Yapay zekâ sisteme sonradan eklenen bir sohbet botu değildir.

AI, BOS mimarisinin çekirdek bileşenlerinden biridir.

Her modül AI servislerini ortak olarak kullanır.

---

## AI Terminology & Capability Matrix

| Term / Capability | Definition | Owner Layer | Allowed Actions | Forbidden Actions | Related Permissions | Notes |
| ----------------- | ---------- | ----------- | --------------- | ----------------- | ------------------- | ----- |
| `AI Engine` | Merkezi yapay zekâ platformu. | Shared Platform | AI servislerini barındırma ve koordine etme. | Doğrudan veritabanı okuma ve yazma. | `AI.Agent.Execute` | BOS genel AI çekirdeğidir. |
| `AI Copilot` | Kullanıcının doğal dil arayüzü. | Presentation / UI | Soru cevaplama, arayüz komut önerileri sunma. | Doğrudan veri kaydetme veya silme. | `AI.Copilot.Use` | Doğal dil ile kontrol paneli. |
| `AI Agent` | Belirli role/departmana bağlı görev yürüten AI bileşeni. | Application | İşlemleri asistan olarak yürütme, analiz ve öneri. | Nihai onay ve yetki verme. | `AI.Agent.Execute` | CEOAgent, SalesAgent vb. |
| `LLM Provider` | OpenAI, Azure OpenAI, Gemini vb. model sağlayıcı. | Infrastructure | Doğal dil işleme ve üretme kabiliyetleri sunma. | İş kurallarını doğrudan belirleme. | Yok | Gateway üzerinden bağlanır. |
| `Prompt Engine` | Promptların merkezi yönetildiği katman. | Application | Şablon yönetimi, prompt versiyonlama ve dinamik enjeksiyon. | Dinamik parametre dışı prompt değiştirme. | `AI.Prompt.Manage` | Sistem promptları. |
| `Context Engine` | Kullanıcı, tenant, rol, workflow, veri ve izin bağlamını oluşturan katman. | Application | Session ve yetki bilgilerini promptlara güvenli ekleme. | İzin sınırlarını aşma veya bypass etme. | `AI.Memory.Read` | Güvenli context sağlar. |
| `Memory Engine` | Session, conversation, business ve knowledge memory katmanı. | Persistence | Geçmiş sohbet geçmişini ve karar hafızasını tutma. | Dış veri sızıntısı / izinsiz bellek paylaşımı. | `AI.Memory.Read`, `AI.Memory.Write` | Bellek yönetimi. |
| `RAG` | Doküman/bilgi tabanı destekli cevap üretimi. | Shared | Şirket içi belgelerden arama ve cevaplama yapma. | İzin verilmeyen belgelere erişim. | `AI.Memory.Read` | Vektör veritabanı kullanır. |
| `AI Gateway` | Tüm AI isteklerinin geçtiği güvenlik, kota ve model yönlendirme kapısı. | Infrastructure | Model rotalama, kota denetimi, güvenlik filtreleme. | Token limitlerini ve izinleri aşma. | Yok | API Gateway alt bileşenidir. |

---

## 🤖 Kilitlenen AI Agent Listesi
Sistemde tanımlı ve otonom yetkileri belirlenmiş AI Ajanları şunlardır:
* `CEOAgent`: Tepe kararlar ve performans analizi.
* `SalesAgent`: Fırsat, teklif ve CRM analizi.
* `FinanceAgent`: Yevmiye fiş dengeleme ve anomali tespiti.
* `HRAgent`: Personel izin ve performans planlama.
* `ProductionAgent`: İş emri ve üretim optimizasyonu.
* `QCAgent`: Kalite test sonuç analizi ve şikâyet/CAPA takibi.
* `LogisticsAgent`: Stok transfer ve depo optimizasyonu.
* `AnalyticsAgent`: İş zekası ve anomali tespiti.
* `LegalAgent`: Sözleşme ve mevzuat kontrolü.
* `ComplianceAgent`: Uyum ve tenant izolasyon denetimi.
* `AIOrchestrator`: Ajanlar arası görev dağıtımı ve yönetim.

---

## 🔒 AI İşlem Sınırları ve Kuralları
1. **Veritabanı İzolasyonu:** AI doğrudan `DbContext`, raw SQL veya repository kullanamaz. Doğrudan veritabanına erişimi kesinlikle yasaktır.
2. **Uygulama Katmanı Zorunluluğu:** AI yalnızca yetkili Application Service, Command veya Query (MediatR) üzerinden işlem yapabilir.
3. **Nihai Onay Yasağı:** AI süreçlerde nihai onay veremez. Sadece onay önerisi üretebilir.
4. **Denetim:** AI ürettiği her aksiyon için audit kaydı bırakmalıdır.
5. **Güvenlik Politikası:** AI tenant isolation, RBAC ve ABAC kontrollerine tabidir.

---

## 🔌 AI Engine'in Diğer Motorlarla İlişkisi
* **Workflow Engine:** Risk, öncelik ve akıllı onay önerileri üretir; yetkisi varsa onay sürecini başlatabilir.
* **Rule Engine:** Risk puanı, anomali skoru ve parametrik kural önerileri üretir.
* **Event Bus:** Event'leri dinleyerek reaksiyon verir ve sadece yetkilendirilmiş entegrasyon event'lerini yayınlar.
* **Analytics Engine:** Geleceğe dönük tahminlemeler ve veri anomalisi tespiti sağlar.
* **Notification Engine:** Bildirimler için dinamik içerik şablonu ve gönderim kanalı önerir.
* **Integration Engine:** Sadece izin verilen entegrasyon konnektörleri üzerinden dış sistemlerle haberleşir.

---

# AI Native Architecture

Emare BOS aşağıdaki mimariyi kullanır.

```text
Kullanıcı

↓

AI Copilot

↓

Context Engine

↓

Reasoning Engine

↓

Business Engine

↓

Workflow Engine

↓

Event Bus

↓

Business Modules
```

AI bütün sistemi bilir.

Hiçbir modül AI'dan bağımsız değildir.

---

# AI Katmanları

## 1. AI Gateway

Tüm AI istekleri önce AI Gateway'e gelir.

Görevleri

* Kimlik doğrulama
* Tenant kontrolü
* Kota kontrolü
* Model seçimi
* Prompt güvenliği
* Audit

---

## 2. Prompt Engine

Prompt'lar merkezi yönetilir.

Prompt türleri

* System Prompt
* Business Prompt
* Agent Prompt
* User Prompt
* Workflow Prompt

Kod içerisine prompt yazılmaz.

Prompt'lar versiyonlanır.

---

## 3. Context Engine

AI yalnızca soruyu değil;

* kullanıcıyı
* tenant'ı
* departmanı
* yetkileri
* açık görevleri
* aktif workflow'ları
* son işlemleri

birlikte değerlendirir.

Buna Context denir.

---

## 4. Memory Engine

AI hafızası.

Katmanlar

### Session Memory

Geçici.

---

### Conversation Memory

Sohbet bazlı.

---

### Business Memory

Kurumsal hafıza.

Örneğin

* müşteri geçmişi
* siparişler
* teklifler
* bakım kayıtları
* kalite raporları

---

### Knowledge Memory

Dokümanlar

Politikalar

Prosedürler

Sözleşmeler

Eğitim içerikleri

---

# Reasoning Engine

AI karar verirken

* kuralları
* workflow'u
* geçmişi
* olayları

birlikte değerlendirir.

Bu katman LLM'den bağımsızdır.

---

# Planning Engine

Karmaşık görevleri parçalar.

Örnek

```text
Yeni bayi aç

↓

CRM

↓

Finance

↓

Warehouse

↓

HR

↓

Tasks

↓

Workflow
```

AI plan üretir.

---

# Agent Manager

Her departmanın kendi ajanı vardır.

## CEO Agent

Yönetim

Kararlar

KPI

Risk

---

## Sales Agent

CRM

Teklif

Sipariş

Tahminleme

---

## Finance Agent

Muhasebe

Bütçe

Risk

Nakit Akışı

---

## HR Agent

İzin

Personel

Eğitim

Performans

---

## Production Agent

MRP

BOM

OEE

İş Emirleri

---

## QC Agent

Kalite

CAPA

Şikayet

Analiz

---

## Logistics Agent

Depo

Transfer

Sevkiyat

FIFO

---

## Legal Agent

Sözleşme

Risk

KVKK

Uyum

---

## Analytics Agent

Dashboard

Forecast

Trend

KPI

---

# AI Vision

Desteklenen özellikler

* OCR
* Barcode
* QR
* Image Classification
* Damage Detection
* Quality Inspection
* Invoice Reading
* Contract Reading

---

# AI Voice

Desteklenen özellikler

* Speech To Text
* Text To Speech
* Voice Commands
* Meeting Summary
* Call Analysis

---

# AI Analytics

AI aşağıdaki analizleri yapabilir.

* Demand Forecast
* Inventory Forecast
* Sales Forecast
* Budget Forecast
* Cash Flow Forecast
* Root Cause Analysis
* Anomaly Detection
* Trend Analysis

---

# AI Automation

AI aşağıdaki otomasyonları başlatabilir.

* Görev oluşturma
* Workflow başlatma
* Hatırlatma
* Doküman sınıflandırma
* Mail taslağı oluşturma
* Rapor hazırlama

Not: Kritik işlemler yalnızca tanımlı onay politikaları kapsamında otomatik yürütülebilir.

---

# RAG (Retrieval Augmented Generation)

AI cevap üretirken

* ERP verisi
* Dokümanlar
* Workflow
* Bilgi Bankası
* SOP
* Politikalar

üzerinden bilgi toplar.

LLM tek başına karar vermez.

---

# Model Katmanı

Desteklenebilir modeller

* OpenAI
* Azure OpenAI
* Anthropic Claude
* Gemini
* Mistral
* Llama
* Yerel LLM

Model değiştirilebilir.

Kod değişmez.

---

# AI Güvenliği

AI aşağıdaki kurallara uyar.

* Tenant Isolation
* RBAC
* ABAC
* Prompt Injection Protection
* Data Masking
* Audit Logging
* Rate Limiting

AI yetkisi olmayan veriyi göremez.

---

# AI Audit

Her AI işlemi kayıt altına alınır.

Kaydedilen bilgiler

* Kullanıcı
* Tenant
* Model
* Prompt sürümü
* Yanıt süresi
* Kullanılan araçlar
* Başarı durumu

---

# AI Marketplace

Yeni Agent eklenebilir.

Örnek

* Procurement Agent
* Maintenance Agent
* Energy Agent
* Sustainability Agent
* Retail Agent

Sistem çekirdeği değiştirilmeden genişletilebilir.

---

# Temel Mimari İlkeleri

* AI doğrudan veritabanına yazmaz.
* AI servis katmanı üzerinden işlem yapar.
* AI tüm yetki kontrollerine uyar.
* AI Event Bus ve Workflow Engine ile entegre çalışır.
* AI cevapları kurumsal bilgi (RAG) ile desteklenir.
* Prompt'lar merkezi yönetilir ve versiyonlanır.
* Tüm AI işlemleri denetlenebilir (Audit) olmalıdır.

---

# Nihai Vizyon

Emare BOS'ta AI;

* kullanıcıya cevap veren bir chatbot değil,
* süreçleri anlayan,
* görev planlayan,
* riskleri öngören,
* öneriler sunan,
* departmanlarla birlikte çalışan

kurumsal bir dijital iş ortağıdır.

Bu mimari sayesinde AI, ERP'nin ayrılmaz bir parçası haline gelir ve platformun tüm modüllerine ortak akıl katmanı sağlar.
