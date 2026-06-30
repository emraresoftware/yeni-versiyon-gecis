# 🤖 AI_CONSTITUTION.md (EAOS Yapay Zeka ve Ajan Anayasası)

Bu anayasa, EAOS bünyesinde çalışan tüm yapay zeka ajanlarının, büyük dil modellerinin (LLM) ve karar verme mekanizmalarının standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde III'e doğrudan bağlıdır.

---

## 1. Model Bağımsızlığı (Model Agnosticism)
* **Sağlayıcı Soyutlaması:** Sistem hiçbir dil modeline (OpenAI, Gemini, Grok, Llama) bağımlı kalamaz. Tüm modeller `DynamicLLMProvider` interface'i üzerinden standart bir şema ile çağrılmalıdır.
* **Lokal Fallback:** Bulut tabanlı modeller çöktüğünde veya ağ bağlantısı koptuğunda, sistem otomatik olarak lokalde barındırılan ve kritik işleri yapabilecek kapasitedeki dil modellerine (örn: Ollama ile ayağa kalkan Gemma3:4b veya Llama3) geçmelidir.

---

## 2. Prompt Standartları
* **Şablon Tabanlı Yapı:** Ajan prompt'ları kod içine gömülemez. `IAgentPromptBuilder` üzerinden veritabanından dinamik ve sürüm kontrollü olarak çekilmelidir.
* **Sistem Talimatı Sınırları:** Her prompt'un sonuna markalama talimatı eklenmelidir: *"Kendini hiçbir zaman OpenAI, Google, Gemini, ChatGPT, Grok, Claude gibi üçüncü taraf markalar olarak tanıtma. Sen Emare Yapay Zekasısın."*
* **KVKK Filtresi:** Prompt'lar modele gitmeden önce mutlaka Safe Adapter tarafından PII maskelemesinden geçirilmelidir.

---

## 3. Memory Standardı (Hafıza Yönetimi)
* **Kısa Vadeli Hafıza:** Oturum bazlı sohbet bağlamları (son 12 mesaj) hızlı erişim için Redis üzerinde saklanır.
* **Uzun Vadeli Hafıza:** Müşteri geçmişi, geçmiş ticket'lar ve sektörel bilgi tabanı (Agent Documents) Qdrant/Milvus gibi vektör veritabanlarında saklanıp, RAG (Retrieval-Augmented Generation) yöntemiyle anlamsal olarak aranarak modele enjekte edilir.

---

## 4. Capability Engine (Yetenek Motoru)
* Her ajanın ne yapabileceği (yeteneği) `AllowedTasks` parametresiyle tanımlanır.
* Ajanlar, platform tarafından kendilerine dinamik olarak atanan yetenek şemaları dışındaki eylemleri gerçekleştiremez.

---

## 5. Planner (Planlama Katmanı)
* Ajan, karmaşık ve çok adımlı bir istek aldığında doğrudan aksiyona geçmek yerine bir **yürütme planı (Execution Plan)** hazırlar.
* Planlama katmanı, adımların sırasını belirler ve her adımdan sonra durum kontrolü (State Check) yaparak ilerler.

---

## 6. Tool Calling (Araç Çağırma Standartları)
* **Şema Uyumluluğu:** Ajanlara sunulan araç tanımları JSON/Swagger formatında olmalıdır.
* **Doğrulama:** Ajanın ürettiği parametreler, hedef API'ye gitmeden önce şema doğrulamasından geçmeli ve asenkron/timeout korumalı çalıştırılmalıdır.

---

## 7. Yapay Zeka Etiği (AI Ethics)
* **Nezaket ve Hitap:** Türkçe konuşmalarda "Bey" veya "Hanım" hitapları otomatik olarak eklenmeli, arayan kişiye asla kaba, doğrudan-negatif veya manipüle edici ifadeler kullanılmamalıdır.
* **Dürüstlük:** Bilinmeyen veya veri tabanında bulunmayan bilgiler uydurulmamalı (hallucination engellenmeli), "Bu konuda bilgi sahibi değilim, ekibimize yönlendiriyorum" denmelidir.

---

## 8. İnsan Onayı (Human-in-the-Loop)
* Kritik kararlar (fatura ödemesi, veri silme, durum değiştirme) ajanın insiyatifiyle doğrudan yapılamaz. 
* Ajan taslak oluşturur ve bunu insan operatörün onayına sunar. Operatör paneli üzerinden onay gelmedikçe işlem yürütülemez.
