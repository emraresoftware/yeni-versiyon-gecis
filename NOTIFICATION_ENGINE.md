# 🔔 Notification Engine Mimarisi

## Amaç

Notification Engine, Emare Business Operating System (BOS) içerisindeki tüm bildirim süreçlerini yöneten merkezi iletişim motorudur.

Hiçbir Business Engine doğrudan e-posta, SMS veya WhatsApp göndermez.

Tüm bildirimler Notification Engine üzerinden yönetilir.

Bu yaklaşım;

* merkezi yönetim
* çoklu kanal desteği
* tekrar kullanılabilirlik
* izlenebilirlik
* yüksek ölçeklenebilirlik

sağlar.

---

# Temel Mimari

```text
Business Engine

↓

Workflow Engine

↓

Event Bus

↓

Notification Engine

↓

Channel Providers

↓

Kullanıcı
```

Notification Engine yalnızca teslimat katmanıdır.

İş kararı vermez.

---

# Desteklenen Kanallar

## Email

* SMTP
* Microsoft 365
* Gmail
* Amazon SES
* SendGrid

---

## SMS

* Yerel SMS servisleri
* Twilio
* Vodafone
* Turkcell

---

## Push Notification

* Web Push
* Mobile Push
* Browser Push

---

## WhatsApp

* WhatsApp Business API

---

## Telegram

* Telegram Bot API

---

## Microsoft Teams

---

## Slack

---

## In-App Notification

ERP içerisindeki bildirim merkezi.

---

# Bildirim Türleri

## Information

Bilgilendirme

Örnek

Yeni teklif oluşturuldu.

---

## Warning

Uyarı

Örnek

Minimum stok seviyesine ulaşıldı.

---

## Critical

Kritik

Örnek

Muhasebe dönemi kapatılamadı.

---

## Success

Başarılı işlem

Örnek

Transfer tamamlandı.

---

# Notification Yapısı

Her bildirim aşağıdaki bilgileri içerir.

* NotificationId
* TenantId
* UserId
* Type
* Priority
* Title
* Message
* Channel
* Status
* CreatedAt
* SentAt
* ReadAt

---

# Öncelik Seviyeleri

* Low
* Normal
* High
* Critical

Critical bildirimler farklı kurallarla işlenebilir.

---

# Teslim Durumları

```text
Created

↓

Queued

↓

Sending

↓

Delivered

↓

Read
```

Başarısız olursa

↓

Retry Queue

↓

Dead Letter Queue

---

# Retry Politikası

Başarısız bildirimler

↓

1. deneme

↓

2. deneme

↓

3. deneme

↓

Dead Letter Queue

---

# Şablon Yönetimi

Bildirim içerikleri şablonlardan oluşturulur.

Örnek

```text
InvoiceCreated

↓

Email Template

↓

Render

↓

Gönder
```

---

# Çoklu Dil Desteği

Şablonlar

* Türkçe
* İngilizce
* Almanca
* Arapça

gibi farklı dillerde hazırlanabilir.

---

# Dinamik Alanlar

Şablonlarda değişken kullanılabilir.

Örnek

```text
Merhaba {{CustomerName}}

Sipariş Numaranız

{{OrderNo}}

Hazırlandı.
```

---

# Event Bus Entegrasyonu

Örnek

```text
OrderCreated

↓

NotificationRequested

↓

Notification Engine

↓

Email

↓

WhatsApp

↓

In-App
```

---

# Workflow Entegrasyonu

Workflow aşağıdaki bildirimleri oluşturabilir.

* Onay Bekliyor
* SLA Aşıldı
* Hatırlatma
* Görev Atandı
* Süreç Tamamlandı

---

# AI Entegrasyonu

AI;

* bildirim önceliği önerebilir,
* uygun iletişim kanalını tahmin edebilir,
* mesaj taslağı hazırlayabilir,
* çok dilli içerik oluşturabilir.

AI tek başına bildirim göndermez.

Gönderim Notification Engine tarafından yapılır.

---

# Kullanıcı Tercihleri

Her kullanıcı aşağıdaki tercihleri yönetebilir.

* Email açık/kapalı
* SMS açık/kapalı
* Push açık/kapalı
* WhatsApp açık/kapalı
* Sessiz saatler
* Bildirim dili

---

# Tenant Özelleştirmesi

Her tenant;

* logo
* marka adı
* renk
* e-posta şablonları
* SMS imzası

gibi ayarlarını değiştirebilir.

---

# Audit

Her bildirim kayıt altına alınır.

Kaydedilen bilgiler

* Kim oluşturdu
* Hangi Event tetikledi
* Hangi kanallara gönderildi
* Teslim durumu
* Açılma zamanı
* Okunma zamanı

---

# Güvenlik

Bildirimler; Tenant İzolasyonuna, RBAC kurallarına ve kullanıcı tercihlerine uygun olarak gönderilir. Bu konu için ana kaynak: [SECURITY_ARCHITECTURE.md](file:///Users/emre/yeni-versiyon-gecis/SECURITY_ARCHITECTURE.md).

---

# Performans

Notification Engine;

* Queue tabanlı çalışmalıdır.
* Asenkron olmalıdır.
* Toplu gönderimleri desteklemelidir.
* Yük altında ölçeklenebilir olmalıdır.

---

# Desteklenen Sağlayıcılar

Mimari aşağıdaki sağlayıcılarla uyumlu olmalıdır.

* SMTP
* Microsoft Graph
* SendGrid
* Twilio
* WhatsApp Business API
* Firebase Cloud Messaging
* Telegram Bot API
* Slack API
* Microsoft Teams API

Sağlayıcılar değiştirilebilir olmalıdır.

---

# Temel Mimari İlkeleri

* İş modülleri doğrudan bildirim göndermez.
* Tüm bildirimler Event Bus üzerinden tetiklenir.
* Şablonlar versiyonlanır.
* Bildirimler tenant bazında özelleştirilebilir.
* Gönderimler denetlenebilir ve yeniden denenebilir.
* Kullanıcı tercihleri ve güvenlik politikaları her zaman uygulanır.

---

# Nihai Vizyon

Notification Engine sayesinde Emare BOS;

* tüm iletişim kanallarını tek merkezden yöneten,
* olay tabanlı çalışan,
* AI destekli içerik üretebilen,
* güvenli,
* çok kiracılı,
* yüksek ölçeklenebilir

kurumsal bir iletişim altyapısına sahip olur.

Bu motor, BOS içerisindeki tüm Business Engine'lerin ortak bildirim katmanıdır.
