# 🔄 CHANGE_MANAGEMENT.md (EAOS Değişiklik ve Sürüm Yönetimi Standartları)

Bu doküman, sistemde yapılacak büyük ölçekli altyapısal veya fonksiyonel değişikliklerin nasıl planlanacağını, analiz edileceğini ve yayına alınacağını belirler. [GOVERNANCE.md](../GOVERNANCE.md) Madde 1 ve 2'ye doğrudan bağlıdır.

---

## 1. Değişiklik Talep Paketi (Change Request Bundle)
Her büyük değişiklik (Örn: Voice Abstraction Layer veya yeni ödeme connector'ı eklenmesi) şu bileşenleri içeren bir paket olarak sunulmalıdır:

1. **ADR (Mimari Karar Belgesi):** Değişikliğin teknik gerekçeleri.
2. **RFC (Request for Comments):** Geliştirici ekibinin görüşleri ve mimari tartışmalar.
3. **Risk Analizi:** Olası performans düşüşleri, güvenlik açıkları ve bütçe etkileri.
4. **Veritabanı Migration Planı:** EF Core veya PostgreSQL seviyesindeki şema değişikliklerinin kesintisiz geçiş adımları.
5. **Rollback (Geri Dönüş) Planı:** İşlerin ters gitmesi durumunda saniyeler içinde eski sürüme dönme yöntemi (Örn: feature flag kapatma veya DB rollback scripti).

---

## 2. Yayın Stratejileri (Deployment Strategies)

EAOS platformunda kesintisiz yayına alma için şu stratejiler uygulanır:

* **Canary Deployment (Kanarya Dağıtımı):** Değişiklik önce sadece seçilmiş %5'lik bir kullanıcı/kiracı grubuna açılır. Observability metrikleri izlenir, hata yoksa kademeli olarak %100'e yayılır.
* **Blue-Green Deployment:** Yeni sürüm (Green) tamamen izole bir ortamda ayağa kaldırılır. Testler başarılı olduğunda, yönlendirici (Nginx/Gateway) trafiği eski sürümden (Blue) yeni sürüme anında aktarır.
* **Gölge Çalıştırma (Shadow Run):** Yeni AI servisleri veya veri analizörleri gelen gerçek trafiği arka planda asenkron olarak dinler ancak dışarıya yanıt vermez (yalnızca doğruluk testi için kullanılır).
