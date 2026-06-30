# ⚙️ COMPLIANCE_ENGINE.md (EAOS Uyumluluk Denetim Sistemi)

Bu doküman, EAOS platformuna eklenecek her yeni modülün geçmek zorunda olduğu otomatik ve manuel kalite kontrol standartlarını (Compliance Rules) tanımlar. [CONSTITUTION.md](../CONSTITUTION.md) Madde IV.1'e doğrudan bağlıdır.

---

## 1. Mimari (Architecture) Uyumluluğu
* Modül Clean Architecture ve CQRS prensiplerine uygun olarak tasarlanmış mı?
* Modüller arası doğrudan veritabanı bağımlılığı var mı? (Tüm iletişimler sadece `Contracts` veya `Event Bus` üzerinden yapılmalıdır).

---

## 2. Güvenlik (Security) Uyumluluğu
* Tüm veri tabanı sorgularında `TenantId` doğrulaması yapılıyor mu?
* Dış LLM sağlayıcılarına giden veriler `Safe Adapter` (Hassas Veri Maskeleme) süzgecinden geçiyor mu?
* API anahtarları ve şifreler `SECURITY_CONSTITUTION.md` standartlarına uygun olarak AES-256-GCM ile şifrelenmiş mi?

---

## 3. Performans (Performance) Uyumluluğu
* Modülün yanıt süreleri `PERFORMANCE_BUDGET.md` limitlerinin altında mı?
* Bellekte sızıntıya (Memory Leak) yol açacak açık nesne referansları veya kapatılmamış soketler var mı?

---

## 4. Ses Güvenliği (Voice Safety) Uyumluluğu
* Ses hattı üzerinde hiçbir engelleyici (blocking) işlem bulunmuyor mu?
* Barge-in kesme RMS algoritmaları ve comfort noise üretimi stabil çalışıyor mu?

---

## 5. İzlenebilirlik ve Metrikler (Observability / Monitoring)
* Modül içindeki tüm kritik hata ve işlem adımları Prometheus metrikleri olarak dışarıya sunuluyor mu?
* Hata loglarında `TenantId` ve `CorrelationId` alanları yapılandırılmış mı?

---

## 6. Fiyatlandırma ve Faturalandırma (Billing / Usage Meter)
* Modülün tükettiği API, token veya işlem süreleri `Usage Meter` (Billing) katmanına bildirilerek kiracı cüzdanından düşülüyor mu?

---

## 7. Entegrasyon Uyumlulukları
* **Plugin Compatibility:** WASM veya Docker sandbox limitlerine uygun mu?
* **Unity Compatibility:** Protobuf formatında hafif gRPC streams destekliyor mu?
* **Video Compatibility:** Storyboard parçalama ve asenkron render kuyruğuna uyumlu mu?
* **AI Compatibility:** `DynamicLLMProvider` interface'i ile model bağımsız çalışabiliyor mu?
