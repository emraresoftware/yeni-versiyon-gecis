# 📊 OBSERVABILITY_CONSTITUTION.md (EAOS İzlenebilirlik ve SLA Anayasası)

Bu anayasa, EAOS platformundaki tüm sistemlerin sağlık durumunu, performans metriklerini ve operasyonel kalitesini (SLA/SLO) izleme standartlarını belirler. [CONSTITUTION.md](../CONSTITUTION.md) Madde I.3 ve Faz 1 hedeflerine doğrudan bağlıdır.

---

## 1. Metrics, Logs, Traces (Üç Altın Sütun)
* **Metrics:** Prometheus uyumlu formatta CPU, Bellek, HTTP istek sayısı, ses gecikmesi (latency) ve hata oranları gerçek zamanlı toplanmalıdır.
* **Logs (Structured Logging):** Loglar düz metin yerine JSON formatında (Structured Logging) yazılmalıdır. Her log satırı `TenantId`, `CorrelationId` (istek takip ID'si) ve `Environment` (dev/prod) alanlarını içermelidir.
* **Traces (Dağıtık İzleme):** Dağıtık mikroservis çağrı zincirleri OpenTelemetry kullanılarak baştan sona izlenmeli, ağdaki tıkanıklık noktaları görselleştirilmelidir.

---

## 2. Alarm Kuralları (Alerting) ve Grafana Dashboards
* **Alarm Seviyeleri:**
  * **Warning (Uyarı):** Slack / E-posta bildirimi (örn: disk doluluğu %80'e ulaştı).
  * **Critical (Kritik):** PagerDuty / SMS araması (örn: ses köprüsü WebSocket bağlantısı koptu veya hata oranı > %5).
* **Merkezi Paneller:** Tüm operasyonel ve iş metrikleri merkezi Grafana panelleri üzerinden anlık izlenmelidir.

---

## 3. SLA, SLO ve Hata Bütçesi (Error Budget)
* **SLA (Service Level Agreement):** Müşterilere taahhüt edilen sistem ayakta kalma süresi aylık minimum **%99.9** olmalıdır.
* **SLO (Service Level Objectives):**
  * Sesli çağrı başlatma süresi: %95 oranında < 300ms.
  * Webchat AI yanıt süresi: %99 oranında < 1500ms.
* **Error Budget (Hata Bütçesi):** Kiracılara taahhüt edilen SLO'ların aşılması durumunda (hata bütçesi tükendiğinde), ilgili servis için yeni özellik (feature) dağıtımı durdurulur; öncelik sistem kararlılığı ve hata düzeltmeye (bug-fixing) verilir.
