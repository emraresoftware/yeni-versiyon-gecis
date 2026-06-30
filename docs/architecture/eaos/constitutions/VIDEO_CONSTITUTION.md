# 📹 VIDEO_CONSTITUTION.md (EAOS Video Üretim Anayasası)

Bu anayasa, EAOS bünyesinde çalışan video üretim servisleri, asenkron render kuyrukları ve dijital sunucu (avatar) entegrasyonlarının standartlarını tanımlar. [CONSTITUTION.md](../CONSTITUTION.md) Faz 2 ve Faz 3 hedeflerine doğrudan bağlıdır.

---

## 1. Provider Abstraction (Sağlayıcı Soyutlaması)
* Sistem, video sentezleme sağlayıcılarına (HeyGen, Synthesia, Tavus, Simli) bağımlı değildir.
* Tüm video üretme komutları ortak bir `VideoGenerationRequest` şeması üzerinden soyutlanarak adaptörler vasıtasıyla hedefe yönlendirilir.

---

## 2. Storyboard ve Uzun Video İşleme (Long Video Pipeline)
* Ajanlar uzun bir video rapor veya onboarding eğitimi hazırlarken, videoyu küçük mantıksal sahnelere (storyboard) böler.
* Her sahne için metin, görsel ve ses bileşenleri tanımlanır. Pipeline bunları asenkron olarak render eder ve en sonda FFmpeg gibi araçlarla kesintisiz tek bir video dosyası olarak birleştirir.

---

## 3. Seslendirme (Voiceover) ve Altyazı (Subtitle)
* Video üzerindeki seslendirme, kiracının ses politikasına uygun olarak seçilen ses motoru (örn: ElevenLabs) ile üretilir.
* Ses dalgasından üretilen milisaniye bazlı kelime zamanlamaları (word timestamps) kullanılarak altyazılar (SRT/VTT) otomatik oluşturulur ve videoya gömülür (hardcode) veya oynatıcıda (softcode) gösterilir.

---

## 4. Render Queue (Yükleyici Kuyruk) ve Asset Library
* **Render Kuyruğu:** Video üretimi CPU/GPU yoğun bir iştir. İstekler anında işlenmek yerine bir kuyruğa (Celery / RabbitMQ) alınır. Kiracılar öncelik seviyelerine (SLA) göre kuyrukta sıraya sokulur.
* **Asset Library:** Tekrarlanan arka plan görselleri, logolar ve müzikler sistemin ortak veya kiracıya özel dosya kütüphanesinde (S3 / Local Storage) önbelleğe alınarak tekrar indirme/oluşturma maliyetleri önlenir.
