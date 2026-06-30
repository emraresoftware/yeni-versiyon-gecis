# ⏱️ PERFORMANCE_BUDGET.md (EAOS Performans Bütçeleri Standartları)

Bu doküman, EAOS bünyesindeki tüm servislerin, veritabanı sorgularının ve gerçek zamanlı kanalların uymak zorunda olduğu maksimum yanıt süresi (latency) ve kaynak tüketimi sınırlarını belirler. [VOICE_CONSTITUTION.md](../constitutions/VOICE_CONSTITUTION.md) ve [API_CONSTITUTION.md](../constitutions/API_CONSTITUTION.md) belgelerine doğrudan bağlıdır.

---

## 1. Gecikme ve Yanıt Süresi Bütçeleri (SLA / SLO)

| Kanal / Servis | Metrik Açıklaması | Maksimum Bütçe | Hedef (Target) |
|---|---|---|---|
| **Voice Call Core** | Arama başladıktan sonra ilk ses çıkışı (First Audio). | < 400ms | **300ms** |
| **Voice Barge-in** | Kullanıcı konuşunca asistan sesinin kesilme süresi. | < 150ms | **80ms** |
| **Webchat AI Reply** | Canlı sohbet yapay zeka cevap süresi. | < 2000ms | **1200ms** |
| **Database Query** | PostgreSQL ilişkisel sorgu süresi. | < 250ms | **50ms** |
| **Cache (Redis)** | Bellek içi veri okuma/yazma süresi. | < 15ms | **5ms** |
| **gRPC internal** | Mikroservisler arası RPC çağrı süresi. | < 50ms | **15ms** |
| **Unity Video Sync** | AI avatar dudak ve sahne senkronizasyon gecikmesi. | < 100ms | **40ms** |
| **Video Generation** | Asenkron video render (HeyGen/Tavus vb.) süresi. | Kuyruk bazlı | SLA'e bağlı |

---

## 2. Maksimum Kaynak Tüketim Limitleri

* **Voice Bridge Container:** Maksimum **0.5 CPU Core** ve **512 MB RAM**. Bu sınırların aşılması memory leak göstergesidir.
* **API Gateway:** Maksimum **0.2 CPU Core** ve **256 MB RAM** (Yüksek eşzamanlılığı gRPC ile hafif yükte taşımak için).
* **Vektör Arama:** Qdrant arama sorguları istek başına en fazla **50ms** CPU zamanı tüketebilir.

---

## 3. Bütçe Aşım Politikası (Out of Budget)
Canlı testlerde veya production izleme panellerinde performans bütçesinin aşıldığı tespit edilirse:
1. İlgili servis için otomatik alarm tetiklenir.
2. Platform Guardian servisi incelemeye alır.
3. Hata bütçesi (`Error Budget`) sıfırlanır ve bütçe iyileştirilene kadar servise yeni kod gönderimi durdurulur.
