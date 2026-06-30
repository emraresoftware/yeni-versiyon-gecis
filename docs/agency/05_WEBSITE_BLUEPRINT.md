# 🌐 05_WEBSITE_BLUEPRINT.md (Web Sitesi ve Widget Standartları)

Bu kılavuz, kiracıların web sitelerine entegre edilecek olan **Emare Live Chat Widget** bileşeninin standartlarını belirler.

---

## 1. Widget Tasarımı
* Sağ alt köşede konumlanan, yuvarlak hatlara sahip, yüzen (floating) chat butonu.
* Kullanıcı butona tıkladığında açılan pencere, kiracının kurumsal renklerine otomatik adapte olmalıdır.

---

## 2. Sohbet Akışı ve Otomasyon
* Widget açıldığında ilk karşılama mesajı `LiveChatWidgetAutomationService` üzerinden **Gemini** tarafından üretilir.
* Eğer kiracı ataması yapılmış bir insan operatör varsa, yapay zeka aradan çekilir ve sohbeti operatör devralır.
