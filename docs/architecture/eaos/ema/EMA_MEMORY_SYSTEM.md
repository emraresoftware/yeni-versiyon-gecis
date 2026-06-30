# 🧠 EMA_MEMORY_SYSTEM.md (Ema Hafıza ve Öğrenme Sistemi Standartları)

Bu doküman, Ema'nın kullanıcılardan edindiği bilgileri nasıl işleyeceğini, saklayacağını, unutacağını ve farklı platformlar arasında nasıl güvenle senkronize edeceğini belirler. Ema'nın öğrenme yeteneği, kiracı gizlilik sınırları ve veri koruma anayasaları dâhilinde sınırlandırılmıştır. [EMA_FOUNDATION.md](EMA_FOUNDATION.md) ve [DATA_CONSTITUTION.md](../constitutions/DATA_CONSTITUTION.md) belgelerine doğrudan bağlıdır.

---

## 1. Hafıza Katmanları (Memory Layers)

Ema'nın hafızası 5 izole katmandan oluşur:

### A. Session Memory (Oturum Hafızası)
* **Kapsam:** Aktif telefon araması veya chat oturumu süresince konuşulan anlık detaylar.
* **Yaşam Süresi:** Oturum sonlandığında (telefon kapandığında veya tarayıcı sekmesi kapandığında) tamamen silinir.

### B. User Preference Memory (Kullanıcı Tercih Hafızası)
* **Kapsam:** Kullanıcının çalışma alışkanlıkları (örn: "Ema bana raporları her sabah 09:00'da getir", "Dark modu tercih ediyorum").
* **Kural:** İzinsiz kalıcı kişisel hafıza yazılamaz. Tercih kaydından önce kullanıcıya sorulmalıdır: *"Bu tercihinizi bir sonraki görüşmelerimiz için kaydedeyim mi?"*

### C. Project Memory (Proje Hafızası)
* **Kapsam:** Sorumlu olunan projelerdeki görevler, bitiş tarihleri ve ekip atamaları.
* **İzolasyon:** Kişisel tercihlerden tamamen izole, kiracı ortak veri tabanında saklanır.

### D. Customer Memory (Müşteri Hafızası)
* **Kapsam:** Müşteri temsilcilerinin CRM üzerinde tuttuğu geçmiş aktiviteler, cari kart detayları ve bilet (ticket) geçmişleri.

### E. Company Knowledge (Şirket Bilgi Dağarcığı)
* **Kapsam:** Kiracının yüklediği el kitapları, fiyat listeleri, SSS (Sıkça Sorulan Sorular) dokümanları (RAG / Vector DB tabanlı).

---

## 2. Onay Gerektiren Hafıza (Approval Required Memory)
* Ema, konuşma esnasında edindiği önemli bir iş bilgisini (örn: "Fiyat listesi değişti", "Yeni tedarikçi Ahmet Bey oldu") doğrudan kalıcı hafızaya yazamaz.
* Bu tür verileri önce *Taslak Hafıza (Staging Memory)* olarak kaydeder ve kullanıcı panelinde onay kutusu çıkarır: *"Görüşmemizde fiyat listesinin güncellendiğini belirttiniz. Bunu şirket hafızasına eklememi onaylıyor musunuz?"*

---

## 3. Unutma ve Silme Kuralları (Forget & Delete Rules)
* **Kullanıcı Hakkı:** Kullanıcı Ema'ya "Bu konuşmada söylediğim X bilgisini unut" dediğinde veya panelden silme talebi gönderdiğinde, ilgili vektör/metin kaydı **milisaniyeler içinde** fiziksel olarak veritabanından (PostgreSQL/Redis/Milvus) silinmelidir (Logical delete kabul edilemez).
* **KVKK/GDPR Uyum Kapısı:** Ema, kişisel verilerin (PII) korunması yasalarına tam uyumlu olarak "Beni Unut" (Right to be Forgotten) protokolünü destekler.

---

## 4. Güvenlik ve Maskeleme (Privacy & Masking)
* **KVKK Maskesi:** Telefon aramalarında veya yazışmalarda geçen T.C. Kimlik No, Kredi Kartı No ve şifre gibi hassas veriler asistanın kalıcı belleğine alınmadan önce Safe Adapter regex KVKK filtresiyle **[MASKED]** haline getirilir.
* **Şifreleme:** Kalıcı hafızadaki tüm veriler kiracıya özel benzersiz şifreleme anahtarları (tenant-specific keys) kullanılarak **AES-256-GCM** ile şifrelenir.

---

## 5. Platformlar Arası Senkronizasyon (Cross-Platform Sync)
* Sesli çağrı merkezi, macOS masaüstü asistanı ve Unity Companion Kiosk ekranı aynı merkezi `EAOS Memory Service` katmanı üzerinden beslenir.
* Bir kullanıcının macOS uygulamasında Ema'ya verdiği kişisel bir komut veya tercih, Unity Kiosk ekranında da anında geçerli olur (örn: "Hoş geldiniz Emre Bey, ses tonumu her zamanki gibi sakin moda ayarladım").
