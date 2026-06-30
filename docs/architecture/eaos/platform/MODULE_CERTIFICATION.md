# 📜 MODULE_CERTIFICATION.md (EAOS Modül Sertifikasyon Standartları)

Bir modülün veya servisin test/staging ortamından canlı (production) ortamına geçebilmesi için tamamlaması zorunlu olan sertifikasyon (onay) adımlarını içerir. [GOVERNANCE.md](../GOVERNANCE.md) Madde 4'e doğrudan bağlıdır.

---

## 1. Mimari İnceleme (Architecture Review)
* Modülün veri akış diyagramı ve mimari uygunluğu `Platform Guardian` tarafından gözden geçirilmeli ve onaylanmalıdır.
* Event-driven modellerin event bus kurallarına uyumu doğrulanmalıdır.

---

## 2. Güvenlik İncelemesi (Security Review)
* Statik Kod Analizi (SAST) taramalarında hiçbir kritik (high/critical) açık kalmamış olmalıdır.
* Veritabanı sorgularında SQL Injection riskine karşı parametrik yapı (`Parameterized Queries`) kullanıldığı onaylanmalıdır.

---

## 3. Performans ve Yük Testleri (Performance & Load Test)
* Modül, maksimum yük altında (SLA sınırları: normal yükün 3 katı) test edilmeli ve gecikme sürelerinde `PERFORMANCE_BUDGET.md` limitlerinin aşılmadığı teyit edilmelidir.
* Veritabanı index'lerinin optimize edildiği ve sorguların timeout vermediği doğrulanmalıdır.

---

## 4. AI ve Ses Doğrulama Testleri (AI & Voice Test)
* Canlı aramalar esnasında asistanın ses kalitesi, barge-in hassasiyeti ve ElevenLabs tts gecikmesi test edilmelidir.
* Dil modelinin uydurma (hallucination) veya KVKK maskelemesini baypas etme durumları test senaryolarıyla doğrulanmalıdır.

---

## 5. Regresyon ve Rollback Testleri (Regression & Rollback)
* Yeni kodun eklenmesiyle mevcut stabil çalışan sesli çağrı sisteminde veya CRM ekranlarında regresyon (gerileme) hatası oluşmadığı doğrulanmalıdır.
* Feature Flag kapatıldığında sistemin anında eski stabil haline döndüğü (rollback) canlı simülasyonla test edilmelidir.
