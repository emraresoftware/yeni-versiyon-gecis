# Agent Trigger Rules - AI Company OS v1

Bu doküman, Emare BOS AI İşletim Sistemi (AI Company OS v1) bünyesindeki tüm ajanların atandıkları yüksek seviyeli **Misyonlar (Missions)** çerçevesinde ne zaman tetikleneceğini, bekleyeceğini, duracağını ve iş devir kurallarını belirler.

---

## 1. Agent 0 (Coordinator / Orchestrator)
*Merkez yönetici ve otonom karar destek düzlemi yürütücüsü.*

- **Ne Zaman Başlar?**
  - `MISSION_BOARD.md` üzerinde atanan veya güncellenen aktif bir misyon olduğunda.
  - `TASK_QUEUE.md` üzerinde herhangi bir ajana atanan yeni veya durumu `READY` olan bir görev belirdiğinde.
  - Bir ajan `HANDOFF.md` üzerinden veya durumu `WAITING_ARCHITECT` / `WAITING_QA` yaparak görevi devrettiğinde.
- **Ne Zaman Bekler?**
  - Ajanlar görevleri yürütürken ve `IN_PROGRESS` / `QA_IN_PROGRESS` durumundayken.
  - Chief Architect'ten mimari onay (`WAITING_ARCHITECT`) veya otonom karar sınırlarını aşan iş kararı beklerken.
- **Ne Zaman Durur?**
  - Aktif tüm misyonlar `COMPLETED` veya `FAILED` durumuna ulaştığında.
- **Ne Zaman QA'ya Devreder?**
  - Misyon kapsamındaki bir görev tamamlandığında otonom olarak `WAITING_QA` durumuna çekilmesini koordine eder.
- **Ne Zaman Chief Architect'e Devreder?**
  - Mimari değişiklik, yeni teknoloji eklenmesi, domain modeli güncellenmesi veya güvenlik politikası revizyonu gerektiğinde.

---

## 2. Agent 1 (Developer)
*Misyon sahibi geliştirici birim.*

- **Ne Zaman Başlar?**
  - Atandığı misyona bağlı, `TASK_QUEUE.md` üzerinde `READY` durumda bir görev olduğunda.
  - `WORK_IN_PROGRESS.md` dosyasına misyon ve kilit kaydını girdikten hemen sonra.
- **Ne Zaman Bekler?**
  - Misyon hedeflerini bloklayan bir harici engel (`BLOCKERS.md`) oluştuğunda.
  - Kendi tamamladığı işlerin QA (`WAITING_QA`) veya Mimar incelemesinde (`WAITING_ARCHITECT`) geri bildirimlerini beklerken.
- **Ne Zaman Durur?**
  - Misyona bağlı atandığı tüm görevler başarıyla tamamlanıp, yerel build/test adımları geçildiğinde ve rapor oluşturulduğunda.
- **Ne Zaman QA'ya Devreder?**
  - Geliştirdiği görevler tamamlandığında, durumu `WAITING_QA` yaparak ve `HANDOFF.md` kaydı girerek.
- **Ne Zaman Chief Architect'e Devreder?**
  - Misyon hedeflerini gerçekleştirmek için standart dışı varsayımlar yapmak yerine mimari karar gerekçesiyle görevi `WAITING_ARCHITECT` durumuna aldığında.

---

## 3. Agent 2 (QA)
*Misyon doğrulama ve kabul testleri birimi.*

- **Ne Zaman Başlar?**
  - `TASK_QUEUE.md` üzerinde `WAITING_QA` durumunda bir görev olduğunda.
  - `WORK_IN_PROGRESS.md` dosyasına kilit kaydını girip görevi `QA_IN_PROGRESS` yaptığında.
- **Ne Zaman Bekler?**
  - Test ortamında veya deployment adımında bir sorun yaşandığında ve düzeltme beklerken.
- **Ne Zaman Durur?**
  - Testleri tamamlayıp test raporunu (`QA_TASK_XXX.md`) yazdıktan sonra.
- **Ne Zaman QA'ya Devreder?**
  - Kendisi QA ajanıdır; testi geçen işleri `DONE` yapar, geçemeyenleri ise `READY` / `IN_PROGRESS` durumuna çekerek Developer'a geri gönderir.
- **Ne Zaman Chief Architect'e Devreder?**
  - Testler sırasında kritik performans, güvenlik veya tasarım uyumsuzluğu bulduğunda görevi `WAITING_ARCHITECT` yapar.

---

## 4. Agent 3 (Product)
*Misyon planlama ve backlog birimi.*

- **Ne Zaman Başlar?**
  - Yeni misyonların tanımlanması (`INITIATED`) veya sprint backlog'unun oluşturulması gerektiğinde.
- **Ne Zaman Bekler?**
  - Kapsam veya iş öncelikleri için Chief Architect'ten (User) girdi beklerken.
- **Ne Zaman Durur?**
  - Misyon hedeflerini, kabul kriterlerini ve `MISSION_BOARD.md` dosyalarını güncellediğinde.
- **Ne Zaman QA'ya Devreder?**
  - Misyon başarı kriterlerini ve kabul test senaryolarını tanımladığında.
- **Ne Zaman Chief Architect'e Devreder?**
  - Misyon hedeflerinin fizibilitesi veya stratejik öncelikler konusunda karar gerektiğinde.

---

## 5. Agent 4 (Security)
*Misyon güvenliği ve audit birimi.*

- **Ne Zaman Başlar?**
  - Aktif misyonların güvenlik analizleri veya sızma testi görevleri verildiğinde.
- **Ne Zaman Bekler?**
  - Geliştiricinin veya altyapı ekibinin tespit edilen güvenlik bulgularını kapatmasını beklerken.
- **Ne Zaman Durur?**
  - Güvenlik raporunu tamamlayıp bulguları `BLOCKERS.md` veya `reports/` dizinine girdiğinde.
- **Ne Zaman QA'ya Devreder?**
  - Güvenlik yamalarının fonksiyonel testlere dahil edilmesini istediğinde.
- **Ne Zaman Chief Architect'e Devreder?**
  - Tespit edilen güvenlik açığı büyük bir yetkilendirme veya kimlik doğrulama mimarisi değişikliği gerektirdiğinde.

---

## 6. Agent 5 (Control Tower)
*Multi-tenancy ve dış entegrasyon misyonları birimi.*

- **Ne Zaman Başlar?**
  - Multi-tenancy entegrasyonu, frontend kabuk yapılandırması veya altyapı (VoIP, DNS, SSL) görevleri `READY` olduğunda.
- **Ne Zaman Bekler?**
  - Dış servislerin, ağ topolojilerinin veya sertifikaların hazır hale gelmesini beklerken.
- **Ne Zaman Durur?**
  - Entegrasyonları tamamlayıp test raporunu sunduğunda.
- **Ne Zaman QA'ya Devreder?**
  - Kurulum tamamlanıp uçtan uca QA testleri yapılması gerektiğinde.
- **Ne Zaman Chief Architect'e Devreder?**
  - Ağ topolojisi veya altyapı mimarisinde bir değişiklik kararı gerektiğinde.

---

## 7. Agent 6 (Legacy)
*Legacy bilgi ve veri göçü misyonları birimi.*

- **Ne Zaman Başlar?**
  - Eski kod tabanlarından analiz ve veri göçü misyonları tetiklendiğinde.
- **Ne Zaman Bekler?**
  - Eski sistemlere erişim yetkisi veya veri şeması belirsizlikleri nedeniyle karar beklerken.
- **Ne Zaman Durur?**
  - Bilgi entegrasyonunu ve gap analizlerini tamamlayıp `docs/legacy/` altına referans dokümanları çıkardığında.
- **Ne Zaman QA'ya Devreder?**
  - Aktarılan veya dönüştürülen eski mantığın doğruluk testleri için QA süreci gerektiğinde.
- **Ne Zaman Chief Architect'e Devreder?**
  - Eski mimarinin yeni platform domain modelleriyle nasıl eşleştirileceği konusunda mimari karar gerektiğinde.
