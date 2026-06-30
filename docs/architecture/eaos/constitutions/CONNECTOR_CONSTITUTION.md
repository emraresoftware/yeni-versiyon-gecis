# 🔗 CONNECTOR_CONSTITUTION.md (EAOS Bağlayıcılar ve Entegrasyon Anayasası)

Bu anayasa, EAOS platformunun dış dünyadaki ERP, CRM, Ödeme sistemleri ve iletişim kanalları ile kuracağı tüm bağlantıların (connectors) standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde I.3 ve Madde II.3'e doğrudan bağlıdır.

---

## 1. Bağlayıcı Türleri ve Mimari
* **ERP Connectors:** Stok sorgulama, fiyat alma ve sipariş aktarımı için SAP, Logo, Netsis gibi sistemlere giden bağlantılar.
* **CRM Connectors:** Müşteri kartları ve aktivitelerini senkronize eden modüller.
* **Payment Connectors:** Kredi kartı, 3D Secure ve tahsilat süreçlerini yöneten banka/ödeme geçidi (örn: iyzico) entegrasyonları.

---

## 2. İletişim Kanalları Bağlayıcıları (WhatsApp, Google, Microsoft)
* **WhatsApp Connector:** WhatsApp Business API veya webhook'lar üzerinden gelen mesajları okuyup AI otomasyonuna ileten kararlı köprü.
* **Google/Microsoft Connector:** Kullanıcı takvimleri (Calendar), e-postalar (IMAP/SMTP/OAuth) ve dosyalar (Drive/OneDrive) için yetkilendirilmiş API entegrasyonları.

---

## 3. Bağlayıcı Güvenliği ve Yetkilendirme
* **OAuth Entegrasyonu:** Google ve Microsoft gibi servislerde kullanıcı şifresi saklanamaz. Zorunlu olarak OAuth 2.0 akışı uygulanmalı ve `AccessToken/RefreshToken` çifti DB'de şifreli saklanmalıdır.
* **IP Kısıtlaması:** ERP ve lokal sistemlere (SAP/Logo) giden bağlantılar, sadece kiracının veya EAOS'un tanımlı sabit IP adresleri üzerinden yapılandırılmış güvenli tüneller (VPN/IPsec) ile kurulmalıdır.

---

## 4. Performans ve Hata Yönetimi
* **Asenkron Çalışma:** ERP sistemleri yavaş yanıt verebilir. Bağlayıcılar üzerinden yapılan tüm veri çekme işlemleri asenkron olmalı ve **maksimum 2000ms timeout** ile sınırlandırılmalıdır.
* **Polly Retry & Circuit Breaker:** Bağlantı koptuğunda, bağlayıcı ardışık isteklerle dış sistemi yormamalı, katlanarak artan bekleme süresiyle (exponential backoff) yeniden denemelidir.
