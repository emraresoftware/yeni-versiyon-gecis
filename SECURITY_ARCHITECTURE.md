# 🔐 Security Architecture

## Amaç

Security Architecture, Emare Business Operating System (BOS) platformunun güvenlik standartlarını, erişim modelini, veri koruma stratejisini ve güvenlik yaşam döngüsünü tanımlar.

Güvenlik sonradan eklenen bir özellik değildir.

Platformun her katmanında uygulanır.

---

# Güvenlik Katmanları

```text
Kullanıcı

↓

Identity

↓

Authentication

↓

Authorization

↓

Business Rules

↓

Data Security

↓

Infrastructure

↓

Monitoring

↓

Audit
```

Her katman bağımsız korunmalıdır.

---

# Zero Trust

BOS aşağıdaki prensibi uygular.

> Never Trust
> Always Verify

Her istek doğrulanır.

Hiçbir kullanıcı varsayılan olarak güvenilir değildir.

---

# Identity Management

Desteklenen yöntemler

* Local User
* LDAP
* Active Directory
* Azure AD
* OpenID Connect
* OAuth2
* SAML

---

# Authentication

Desteklenen yöntemler

* Username / Password
* MFA
* FIDO2
* Passkey
* JWT
* API Key
* Service Account

---

# Authorization

Desteklenen modeller

## RBAC

Role Based Access Control

---

## ABAC

Attribute Based Access Control

---

## Policy Based Access

Koşula göre yetki.

Örnek

```text
Department = Finance

AND

Country = TR

↓

Allow
```

---

# Tenant Isolation

Her tenant tamamen izole edilir.

İzolasyon kapsamı

* Database
* Storage
* Cache
* Queue
* Search
* AI Context
* Audit

Tenant'lar birbirlerinin verilerine erişemez.

---

# Data Classification

Veriler sınıflandırılır.

* Public
* Internal
* Confidential
* Restricted

Her sınıf farklı koruma politikası uygular.

---

# Encryption

## In Transit

TLS 1.3

---

## At Rest

AES-256

---

## Secret Management

Parolalar

API Key

Certificate

Token

Vault içerisinde tutulmalıdır.

---

# API Security

Her API aşağıdaki kontrollerden geçer.

* Authentication
* Authorization
* Rate Limiting
* Input Validation
* Output Filtering
* Audit

---

# Input Validation

Tüm girişler doğrulanmalıdır.

Korunacak saldırılar

* SQL Injection
* XSS
* CSRF
* SSRF
* Command Injection
* Path Traversal

---

# Session Management

Desteklenir

* Session Timeout
* Sliding Expiration
* Device Tracking
* Concurrent Session Control

---

# Password Policy

Minimum

* 12 karakter
* Büyük harf
* Küçük harf
* Rakam
* Özel karakter

Desteklenir

* Password History
* Password Expiration
* Breached Password Check

---

# Audit Log

Her kritik işlem kayıt altına alınır.

Örnek

* Login
* Logout
* Role Change
* Permission Change
* Data Export
* Delete
* Approval
* AI Action

Audit kayıtları değiştirilemez.

---

# Data Masking

Örnek

```text
TC Kimlik

↓

********1234

Kart

↓

************4582
```

Yetkisiz kullanıcı tam veriyi göremez.

---

# Row Level Security

Örnek

```text
Tenant = A

↓

Yalnızca Tenant A verisi
```

---

# Column Level Security

Örnek

Muhasebe

↓

Salary

Görebilir

Satış

↓

Salary

Göremez

---

# File Security

Yüklenen dosyalar

* Virüs taramasından geçmelidir.
* Tür doğrulaması yapılmalıdır.
* Boyut limiti uygulanmalıdır.
* Yetkili kullanıcılar tarafından indirilebilir.

---

# AI Security

AI aşağıdaki kurallara uyar.

* Prompt Isolation
* Tenant Isolation
* Data Masking
* Permission Check
* Prompt Audit
* Model Audit

AI yetkisiz veriye erişemez.

---

# Integration Security

Entegrasyonlar

* OAuth2
* Mutual TLS
* API Key Rotation
* Certificate Rotation

ile korunmalıdır.

---

# Observability Entegrasyonu

Tüm güvenlik olayları

↓

Observability Platform

↓

SIEM

↓

Alert Engine

ile entegre çalışmalıdır.

---

# Disaster Recovery

Güvenlik kapsamında

* Backup Encryption
* Key Rotation
* Recovery Verification
* Immutable Backup

uygulanmalıdır.

---

# Uyumluluk

Platform aşağıdaki standartları destekleyecek şekilde tasarlanmalıdır.

* ISO 27001
* SOC 2
* GDPR
* KVKK
* NIST Cybersecurity Framework
* CIS Controls

---

# Güvenlik Testleri

Her sürümde uygulanmalıdır.

* Static Analysis
* Dependency Scan
* Secret Scan
* Container Scan
* Penetration Test
* API Security Test

---

# Temel Mimari İlkeleri

* Zero Trust varsayılandır.
* Least Privilege uygulanır.
* Varsayılan olarak tüm erişimler reddedilir.
* Tenant izolasyonu zorunludur.
* Tüm kritik işlemler denetlenebilir olmalıdır.
* Şifreleme tüm katmanlarda uygulanmalıdır.
* Güvenlik kuralları koddan bağımsız yönetilebilir olmalıdır.

---

# Nihai Vizyon

Security Architecture sayesinde Emare BOS;

* Zero Trust yaklaşımını benimseyen,
* çok kiracılı güvenli çalışan,
* kurumsal uyumluluk standartlarını destekleyen,
* AI destekli tehdit analizi yapabilen,
* denetlenebilir ve sürdürülebilir

bir kurumsal platform haline gelir.

Bu doküman, Emare BOS'un tüm güvenlik tasarımının temel referansıdır.
