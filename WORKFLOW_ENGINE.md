# 🔄 Workflow Engine Mimarisi

**Title:** Workflow Engine Mimarisi
**Version:** 1.0.0
**Status:** Approved
**Owner:** Architecture Board
**Last Updated:** 2026-06-27
**Dependencies:** EVENT_BUS.md
**Related Documents:** RULE_ENGINE.md, NOTIFICATION_ENGINE.md

---

## Change History
| Version | Date | Author | Description |
| ------- | ---- | ------ | ----------- |
| 1.0.0   | 2026-06-27 | Architecture Team | Formatted header and standardized metadata. |

---

## Amaç

Workflow Engine, Emare Business Operating System (BOS) içerisinde tüm iş süreçlerini yöneten merkezi otomasyon motorudur.

Sistemde hiçbir iş süreci manuel olarak modüller içerisine gömülmez.

Tüm onay mekanizmaları, görev atamaları, SLA kuralları, eskalasyonlar ve otomasyonlar Workflow Engine tarafından yönetilir.

---

# Temel Prensip

Bir işlem gerçekleşir.

↓

Workflow tetiklenir.

↓

Kurallar değerlendirilir.

↓

Görev oluşturulur.

↓

Onay alınır.

↓

Sonraki adım çalıştırılır.

↓

İşlem tamamlanır.

---

## Workflow Matrix (Süreç Matrisi)

| Workflow Name | Owner Context | Trigger Event / Action | Steps | SLA | Escalation | Required Permissions | Output Events |
| ------------- | ------------- | ---------------------- | ----- | --- | ---------- | -------------------- | ------------- |
| `CrmProposalApproval` | CRM / Sales | `CrmProposalSent` | 1. Limit kontrolü (Rule Engine)<br>2. %20 üstü indirim ise SalesManager onayı<br>3. Büyük tutarlarda CEO onayı | 24 Saat | 24 saat onaylanmazsa SalesManager'a, 48 saatte CEO'ya eskalasyon. | `CRM.Proposal.Approve` | `CrmProposalApproved`, `CrmProposalDeclined` |
| `FinanceJournalEntryPosting` | Finance | Fiş onay talebi | 1. Bakiye kontrolü (Rule Engine)<br>2. FinanceManager onayı | 48 Saat | 48 saat onaylanmazsa CEO'ya eskalasyon / bildirim. | `Finance.JournalEntry.Post` | `FinanceJournalEntryPosted` |
| `HrLeaveApproval` | HR | `HrLeaveRequested` | 1. Kalan gün kontrolü (Rule Engine)<br>2. Departman Yöneticisi onayı<br>3. HRManager onayı | 72 Saat | 72 saat onaylanmazsa HRManager'a eskalasyon. | `HR.Leave.Approve` | `HrLeaveApproved`, `HrLeaveRejected` |
| `LogisticsStockTransferApproval` | Logistics | `StockTransferRequested` | 1. Kaynak depo stok seviyesi kontrolü (Rule Engine)<br>2. Kaynak depo sorumlusu onayı<br>3. Hedef depo sorumlusu teslimat onayı | 12 Saat | 12 saatte tamamlanmazsa LogisticsManager'a uyarı. | `Logistics.StockTransfer.Approve`, `Logistics.StockTransfer.Complete` | `LogisticsStockTransferCompleted`, `LogisticsStockTransferRejected` |
| `QcClaimResolution` | QC | `QcClaimCreated` | 1. Kalite Standardına göre inceleme<br>2. Rework/Hurda aksiyonu belirleme<br>3. QCManager sonuçlandırması | 5 İş Günü | 5 gün aşılırsa CEO ve QCManager'a acil alarm. | `QC.Claim.Resolve` | `QcClaimResolved` |
| `DecisionLogApproval` | CEO | `DecisionLogCreated` | 1. AI ön değerlendirme analizi<br>2. CEO onayı | 24 Saat | Uygulanmaz (CEO inisiyatifi). | `CEO.DecisionLog.Approve` | `DecisionLogApproved` |

---

## 🛠️ Rule / Workflow / Event Entegrasyon Ayrımı

Sistem süreç otomasyonunda görevler şu şekilde ayrılmıştır:
1. **Rule Engine (Karar Verici):** Girdi parametrelerini ve eşik değerlerini değerlendirerek mantıksal kararlar üretir (Örn: "İndirim oranı limit aşımı: Evet").
2. **Workflow Engine (Süreç İşletici):** Süreç adımlarını, SLA sürelerini, insan görevlerini (tasks) ve eskalasyon yollarını koordine eder.
3. **Event Bus (Sonuç Dağıtıcı):** Süreç adımlarının tamamlanmasıyla üretilen event'leri (Örn: `HrLeaveApproved`) asenkron olarak diğer modüllere dağıtır.

---

## 🤖 AI Workflow Sınırları

* **Analiz ve Öneri:** AI Ajanı, workflow süreçlerinde risk analizi yapabilir, öncelik atayabilir ve yöneticilere akıllı onay/ret önerileri sunabilir.
* **Nihai Onay Yasağı:** AI hiçbir zaman nihai onay verme yetkisine sahip olamaz. Onaylar her zaman fiziksel bir sorumlu tarafından verilmelidir.
* **Tetikleme Sınırı:** AI ancak `AI.Agent.Execute` veya ilgili modül yetkilerine sahip olması durumunda sadece sistem üzerinden görev veya workflow önerisi başlatabilir.

---

# Workflow Bileşenleri

## Workflow Definition

Sürecin tanımıdır.

Örnek

```text
Satın Alma Süreci

↓

Talep

↓

Müdür Onayı

↓

Finans Onayı

↓

Satın Alma

↓

Teslim

↓

Kapanış
```

---

## Workflow Instance

Her çalışan süreç bir instance oluşturur.

Örnek

```text
Workflow

↓

Purchase Approval

↓

Instance #5842
```

---

## Workflow Step

Her süreç adımı bağımsızdır.

Desteklenen adımlar

* Approval
* Task
* Notification
* Decision
* Integration
* Script
* Delay
* AI Decision

---

## Workflow Variables

Her süreç değişken taşıyabilir.

Örnek

```text
PurchaseAmount

Department

EmployeeId

WarehouseId

Currency

ManagerId
```

---

# Desteklenen Adım Tipleri

## Approval

Bir veya daha fazla kullanıcının onayını bekler.

---

## Multi Approval

Örnek

```text
Finans

↓

Satın Alma

↓

CEO
```

Hepsi onaylamadan süreç devam etmez.

---

## Sequential Approval

```text
Manager

↓

Director

↓

CEO
```

Sıralı çalışır.

---

## Parallel Approval

```text
HR

Finance

Legal

Production
```

Aynı anda çalışır.

---

## Decision

Koşul değerlendirir.

Örnek

```text
Amount > 100000

↓

CEO Onayı

↓

Devam
```

---

## Timer

Belirli süre bekler.

Örnek

```text
24 Saat

↓

Hatırlatma Gönder
```

---

## Escalation

Süre dolarsa

↓

Üst yöneticiye aktar.

---

## Notification

Desteklenen kanallar

* Email
* SMS
* Push
* WhatsApp
* Telegram
* Teams
* Slack

---

## Integration

REST

Webhook

Kafka

RabbitMQ

gRPC

çağrıları yapılabilir.

---

## AI Decision

AI öneri oluşturabilir.

Örnek

```text
Satın alma riskli mi?

↓

AI Analizi

↓

Risk %

↓

Workflow devam eder.
```

AI tek başına nihai onay vermez; politika izin veriyorsa öneri sunar veya belirli sınırlar içinde otomatik karar verebilir.

---

# Workflow Durumları

```text
Draft

↓

Published

↓

Running

↓

Waiting

↓

Completed

↓

Cancelled

↓

Failed
```

---

# SLA Yönetimi

Her Workflow SLA tanımlayabilir.

Örnek

```text
İzin Talebi

↓

24 Saat

↓

Aşıldı

↓

Escalation
```

---

# Görev Motoru

Workflow görev üretir.

Görev özellikleri

* Atanan Kullanıcı
* Departman
* Öncelik
* Başlangıç
* Bitiş
* SLA
* Durum
* Açıklama

---

# Workflow Versiyonlama

Her süreç versiyon taşır.

```text
Purchase Approval v1

Purchase Approval v2

Purchase Approval v3
```

Eski instance eski versiyonla çalışmaya devam eder.

---

# Yetkilendirme

Workflow aşağıdaki yetkileri kontrol eder.

* Kullanıcı
* Rol
* Departman
* Tenant
* Organizasyon
* Tutar Limiti
* Lokasyon
```

---

# BPMN Uyumluluğu

Workflow Engine aşağıdaki BPMN kavramlarını destekleyecek şekilde tasarlanmalıdır.

* Start Event
* End Event
* User Task
* Service Task
* Exclusive Gateway
* Parallel Gateway
* Timer Event
* Message Event
* Signal Event

---

# Event Bus Entegrasyonu

Workflow Event Bus ile haberleşir.

Örnek

```text
PurchaseApproved

↓

Workflow

↓

StockReserveRequested

↓

FinanceJournalRequested

↓

NotificationRequested
```

---

# AI Entegrasyonu

AI aşağıdaki alanlarda Workflow'u destekler.

* Risk Analizi
* Öncelik Belirleme
* Tahminleme
* Otomatik Kategori
* Doküman Analizi
* SLA İhlal Tahmini
* İş Yükü Tahmini

---

# No-Code Workflow Designer

Yönetici kullanıcılar sürükle bırak ile süreç oluşturabilir.

Desteklenen öğeler

* Node
* Connection
* Condition
* Approval
* Delay
* Script
* Integration
* AI Node

Kod yazmadan yeni süreç geliştirilebilir.

---

# Audit

Her adım kayıt altına alınır.

Kaydedilen bilgiler

* Kim başlattı
* Kim onayladı
* Kim reddetti
* Ne zaman gerçekleşti
* Eski değer
* Yeni değer
* Süre

---

# Performans

Workflow Engine

* Asenkron çalışmalıdır.
* Event Bus kullanmalıdır.
* Uzun süren işlemleri Queue üzerinden yürütmelidir.
* Tek transaction içerisinde gereksiz bekleme yapmamalıdır.

---

# Temel Mimari İlkeleri

* Workflow tanımları kod içerisine gömülmez.
* Süreçler metadata olarak saklanır.
* Tüm süreçler versiyonlanır.
* Event Bus ile entegre çalışır.
* Yetkilendirme merkezi güvenlik katmanı üzerinden yapılır.
* AI yalnızca tanımlı politika ve yetki sınırları içinde karar mekanizmasına katkı sağlar.
* Workflow Engine, Emare BOS içerisindeki tüm modüllerin ortak süreç yönetim altyapısıdır.
