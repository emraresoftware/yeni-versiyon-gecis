# 🔌 Integration Engine Mimarisi

## Amaç

Integration Engine, Emare Business Operating System (BOS) ile dış sistemler arasındaki tüm veri alışverişini yöneten merkezi entegrasyon platformudur.

Hiçbir Business Engine üçüncü taraf sistemlere doğrudan bağlanmaz.

Tüm entegrasyonlar Integration Engine üzerinden gerçekleştirilir.

Bu mimari;

* gevşek bağlı (Loose Coupling)
* yüksek ölçeklenebilir
* güvenli
* versiyonlanabilir
* yönetilebilir

bir entegrasyon katmanı oluşturur.

---

# Temel Mimari

```text
Business Engine

↓

Event Bus

↓

Integration Engine

↓

Connector

↓

External System
```

Business Engine dış sistemi tanımaz.

Yalnızca Integration Engine ile haberleşir.

---

# Desteklenen Entegrasyon Tipleri

## REST API

JSON tabanlı servisler.

---

## GraphQL

Tek endpoint üzerinden veri erişimi.

---

## gRPC

Yüksek performanslı servisler.

---

## Webhook

Gerçek zamanlı olay bildirimleri.

---

## Message Queue

Desteklenen altyapılar

* Kafka
* RabbitMQ
* Azure Service Bus
* AWS SQS
* Redis Streams

---

## File Transfer

* FTP
* SFTP
* FTPS

---

## EDI

Kurumsal veri değişimi.

Desteklenen standartlar

* EDIFACT
* ANSI X12
* XML
* CSV
```

---

# Connector Mimarisi

Her dış sistem bağımsız Connector olarak geliştirilir.

Örnek

```text
SAP Connector

Oracle Connector

Logo Connector

Netsis Connector

Nebim Connector

Shopify Connector

WooCommerce Connector

Trendyol Connector

Hepsiburada Connector
```

Connector'lar birbirinden bağımsızdır.

---

# Banka Entegrasyonları

Desteklenebilir.

* Havale
* EFT
* SWIFT
* Sanal POS
* Hesap Ekstresi
* Mutabakat

---

# e-Dönüşüm

Desteklenen servisler

* e-Fatura
* e-Arşiv
* e-İrsaliye
* e-Müstahsil
* e-Defter

---

# Kargo Entegrasyonları

Örnek

* Yurtiçi
* MNG
* Aras
* DHL
* UPS
* FedEx

Gönderi oluşturma

↓

Takip numarası

↓

Durum sorgulama

↓

Teslim bilgisi

---

# Pazaryeri Entegrasyonları

Desteklenebilir.

* Trendyol
* Hepsiburada
* Amazon
* eBay
* Etsy
* Shopify

---

# ERP Entegrasyonları

Gerekirse aşağıdaki sistemlerle veri alışverişi yapılabilir.

* SAP
* Oracle
* Microsoft Dynamics
* IFS
* Logo
* Netsis
* Mikro

---

# IoT Entegrasyonu

Desteklenebilir.

* PLC
* SCADA
* OPC-UA
* MQTT
* Sensörler
* RFID Okuyucular

---

# Kimlik Doğrulama

Desteklenen yöntemler

* OAuth2
* OpenID Connect
* JWT
* API Key
* Basic Authentication
* Mutual TLS

---

# API Gateway

Tüm dış istekler API Gateway üzerinden geçer.

Gateway görevleri

* Kimlik doğrulama
* Yetkilendirme
* Rate Limiting
* Logging
* Monitoring
* Routing

---

# Mapping Engine

Dış sistem alanları ile BOS alanları eşleştirilir.

Örnek

```text
External CustomerCode

↓

Internal CrmAccount.Code
```

Kod içerisinde dönüşüm yapılmaz.

---

# Data Transformation

Desteklenen dönüşümler

* JSON
* XML
* CSV
* Excel

Gerekirse özel dönüştürücüler eklenebilir.

---

# Retry Mekanizması

Başarısız entegrasyon

↓

Retry

↓

Retry

↓

Retry

↓

Dead Letter Queue

---

# Monitoring

Her entegrasyon izlenir.

Takip edilen bilgiler

* Süre
* Başarı oranı
* Hata
* Retry sayısı
* Trafik
* Son senkronizasyon

---

# Senkronizasyon Türleri

## Real-Time

Event oluştuğu anda.

---

## Scheduled

Belirli aralıklarla.

---

## Manual

Kullanıcı tetikler.

---

## Hybrid

Gerçek zamanlı + zamanlanmış.

---

# Tenant İzolasyonu

Her tenant kendi bağlantı bilgilerini kullanır.

Örnek

* API URL
* API Key
* Secret
* Sertifika
* Webhook URL

Hiçbir tenant başka tenant'ın entegrasyon bilgisine erişemez.

---

# Audit

Her entegrasyon işlemi kayıt altına alınır.

Kaydedilen bilgiler

* Connector
* Tenant
* İşlem tipi
* İstek zamanı
* Yanıt zamanı
* Durum
* Hata mesajı

---

# Güvenlik

Integration Engine;

* Tenant Isolation
* RBAC
* ABAC
* API Gateway
* Audit
* Encryption
* Secret Vault

ile korunmalıdır.

---

# Performans

Integration Engine;

* Asenkron çalışmalıdır.
* Queue desteklemelidir.
* Paralel işlem yapabilmelidir.
* Yatay ölçeklenebilir olmalıdır.

---

# SDK

Üçüncü taraf geliştiriciler için SDK sağlanmalıdır.

Desteklenebilir diller

* .NET
* Java
* Python
* JavaScript
* Go

---

# Temel Mimari İlkeleri

* Business Engine dış sistemleri tanımaz.
* Tüm entegrasyonlar Connector üzerinden yapılır.
* Mapping merkezi yönetilir.
* Event Bus ile entegre çalışır.
* Retry ve DLQ zorunludur.
* Tüm entegrasyonlar denetlenebilir olmalıdır.

---

# Nihai Vizyon

Integration Engine sayesinde Emare BOS;

* bankalar,
* e-Dönüşüm servisleri,
* kargo firmaları,
* pazaryerleri,
* ERP sistemleri,
* IoT cihazları,
* üçüncü taraf uygulamalar

ile güvenli, ölçeklenebilir ve sürdürülebilir şekilde haberleşebilen kurumsal bir entegrasyon platformuna sahip olur.

Bu motor, Emare BOS'un dış dünya ile iletişim kuran standart entegrasyon katmanıdır.
