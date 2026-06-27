# 🤖 AI Engine Mimarisi

**Title:** AI Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** EVENT_BUS_MIMARISI.md
**Related Documents:** WORKFLOW_ENGINE_MIMARISI.md, INTEGRATION_ENGINE.md

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
