# 🧠 EMA_BRAIN_ARCHITECTURE.md (Ema Karar ve Düşünce Mimarisi El Kitabı)

Bu doküman, Ema'nın bilişsel yapısını (Brain Architecture), gelen girdileri nasıl işlediğini, nasıl karar alıp plan yaptığını ve bu kararları nasıl güvenli eylemlere dönüştürdüğünü tanımlar. [EMA_FOUNDATION.md](EMA_FOUNDATION.md) ve [AI_CONSTITUTION.md](../constitutions/AI_CONSTITUTION.md) belgelerine doğrudan bağlıdır.

---

## 1. Bilişsel İş Akışı (Cognitive Flow)

Ema'nın beyni (Brain Core) asenkron çalışan 10 ana motordan oluşur:

```
[ Kullanıcı Girdisi (Ses/Metin) ]
               │
               ▼
       1. Context Manager ── (Hafıza Yükleme) ──► 3. Memory Engine
               │
               ▼
       2. Decision Engine ── (Görev Bölümleme) ─► 4. Planning Engine
               │                                         │
               ▼                                         ▼
       8. Safety Engine  ◄── (Güvenlik Sınırı) ──  5. Tool Engine
               │
               ▼
       6. Conversation Engine (Yanıt Üretimi) ◄── 7. Emotion Engine
               │
               └─► 9. Personality Engine & 10. Learning Engine
```

---

## 2. Beyin Motorları ve Görevleri

### 1. Context Manager (Bağlam Yöneticisi)
* **Görevi:** Konuşmanın gidişatını, aktif konu başlığını ve kiracının kimliğini (TenantId) takip eder. Gelen her girdiyi doğru bağlam penceresine oturtur.

### 2. Decision Engine (Karar Motoru)
* **Görevi:** Kullanıcı niyetini (intent classification) çözümler. Gelen isteğin basit bir sohbet mi, bir bilgi sorgusu mu, yoksa ERP üzerinde bir işlem tetiklemesi mi olduğuna karar verir.

### 3. Memory Engine (Bellek Motoru)
* **Görevi:** `EMA_MEMORY_SYSTEM.md` standartlarına uygun olarak, anlık, kişisel ve kurumsal bilgi veri tabanlarına (Vektör/İlişkisel DB) asenkron sorgular atarak bağlama en uygun geçmiş veriyi getirir.

### 4. Planning Engine (Planlama Motoru)
* **Görevi:** Karar motorunun belirlediği karmaşık hedefleri küçük mantıksal adımlara (sub-tasks) böler. Hangi sırayla hangi araçların (tools) çağrılacağını planlar (ReAct / Planner framework).

### 5. Tool Engine (Araç Çalıştırma Motoru)
* **Görevi:** Planlama motorunun kararlaştırdığı fonksiyonları (örn: `check_ticket_status`, `create_order`) çağırır.
* **Kural:** Tüm araç çağrıları strictly typed DTO sözleşmeleri (`EmareTicket.Contracts`) ile yürütülür.

### 6. Conversation Engine (Konuşma Motoru)
* **Görevi:** Toplanan verileri, şirket kimliğini ve Ema'nın dil kurallarını (`EMA_CHARACTER_BIBLE.md`) harmanlayarak kullanıcıya verilecek nihai metin veya ses yanıtını üretir.

### 7. Emotion Engine (Duygu Motoru)
* **Görevi:** Yanıtın tonundan ve kullanıcının ruh halinden yola çıkarak asistanın duygusal durumunu (`Neutral`, `Attentive`, `Thoughtful`, `Empathetic`, `Cheerful`) belirler ve bu veriyi Unity/UI katmanına gönderir.

### 8. Safety Engine (Güvenlik ve KVKK Motoru)
* **Görevi:** Ajanın dışarıya vermeye çalıştığı yanıtları ve veritabanına yazmaya çalıştığı kalıcı verileri KVKK, PII maskeleme ve tenant izolasyonu filtrelerinden geçirir. Yetkisiz eylemleri bloke eder.

### 9. Personality Engine (Kişilik Motoru)
* **Görevi:** Ema'nın sakin, empatik ve profesyonel kurumsal duruşunu korumasını sağlar. Çıktıların `EMA_CHARACTER_BIBLE.md` anayasasına uygunluğunu denetler.

### 10. Learning Engine (Öğrenme Motoru)
* **Görevi:** Oturum sonlarında kullanıcının onay verdiği çalışma alışkanlıklarını asenkron olarak analiz eder ve bir sonraki oturumda kullanılmak üzere `User Preference Memory` alanına yazar.
