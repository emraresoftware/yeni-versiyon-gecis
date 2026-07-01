# Implementation Plan - TASK-EMA-MIGRATION-001 Ema Migration Plan

Ema Desktop Assistant ve Voice Bridge altyapısının `emaredestek/emaredestek` monolit deposundan tamamen ayrılarak bağımsız bir ürün repository'si haline getirilmesi için hazırlanan geçiş ve mimari ayrıştırma planı.

## 1. Mevcut Bağımlılık Haritası
Ema bileşenleri şu an iki ana katmandan oluşmaktadır:
1. **Client Katmanı (macOS Assistant - Swift):**
   - ElevenLabs ConvAI WebSocket uç noktasına doğrudan veya local ağ geçidine (`ws://localhost:8096`) bağlanır.
   - CoreAudio ve AVFoundation dışında dış bağımlılığı yoktur.
2. **Bridge Katmanı (standalone-voice-bridge - Python):**
   - **Veritabanı Bağımlılığı:** `EmareTicketProd` PostgreSQL veritabanına doğrudan `asyncpg` havuzuyla bağlanır.
   - **API Bağımlılığı:** `bridge_api_client.py` üzerinden `EMARE_API_URL` (port 5002) üzerinden kiracı ve asistan ayarlarını çeker.
   - **Kanal/Ağ Bağımlılığı:** Asterisk AudioSocket (`8095`) ve Redis (`6379`) servisleriyle konuşur.

---

## 2. Taşınacak Dosyalar
Yeni oluşturulacak bağımsız `ema-companion` deposuna taşınacak dizin ve dosyalar:
- `gemini-live-standalone/` dizini altındaki tüm içerik:
  - `macos-assistant/` (Swift Client projesi ve build betikleri)
  - `standalone_bridge.py` (Ses köprüsü ve Asterisk entegrasyonu)
  - `assistant_gateway.py` (Masaüstü WebSocket geçidi)
  - `ema_brain.py` (Ema Brain orkestratörü)
  - `action_engine.py`, `room_brain.py`, `agent_registry.py` (Ajan motorları)
  - Entegrasyon testleri, ses testleri (`test_ema_brain.py`, `scenario_runner.py` vb.)
  - `compose.yml` (Docker Compose orkestrasyon dosyası)
  - `Dockerfile.bridge` ve Asterisk konfigürasyon şablonları (`asterisk_config/`)

---

## 3. Taşınmayacak Dosyalar
Ana monolit depoda (`emaredestek/emaredestek`) kalacak dosyalar:
- `.NET 8` Clean Architecture C# API kaynak kodları (`src/` altındaki tüm projeler)
- `Next.js 16` Frontend web dashboard projesi (`web/` dizini)
- Ana veri tabanı migrasyonları, Docker Compose prod konfigürasyonları ve ortak proje yönetim belgeleri.

---

## 4. Import Değişiklikleri
- **Swift Projesi:** Herhangi bir import değişikliği gerektirmez (çünkü tamamen self-contained Cocoa/Swift projesidir).
- **Python Projesi:** Göreli importlar (`from action_engine import ActionEngine` vb.) aynı dizinde kalacağı için kod içi değişiklik gerektirmez. Sadece `.env` ve docker ortam değişkenlerinde tanımlı absolute yol referansları (örneğin `/app/recordings` gibi hacim eşlemeleri) güncellenecektir.

---

## 5. Build Etkisi
- **Ema Companion:** Ayrı bir repository haline geldiğinde `swift build` veya Docker build adımları tamamen bağımsız çalışacaktır.
- **Monolit Proje:** `gemini-live-standalone/` altındaki dosyaların silinmesi, monolit backend (.NET 8) veya frontend (Next.js) projelerinin derlenmesini hiçbir şekilde etkilemez.

---

## 6. Test Etkisi
- Entegrasyon testleri (`test_ema_brain.py`) artık yeni deponun CI aşamasında veya lokalde çalıştırılacaktır.
- Veritabanı ve API erişimini taklit eden mock testlerin kapsamı genişletilecektir.

---

## 7. CI/CD Etkisi
- GitHub Actions üzerinde `standalone-voice-bridge` imajının build alıp `185.189.54.107` ve staging sunucularına deploy edilmesini sağlayan deployment betikleri yeni depoya taşınacak ve deploy anahtarları (SSH deploy keys) güncellenecektir.

---

## 8. Rollback Planı
Geçiş esnasında bir hata oluşması durumunda:
1. `emaredestek` ana deposundaki `gemini-live-standalone/` dizini geçiş stabil olana kadar silinmeyip dondurulacaktır.
2. Sunucu tarafındaki Docker servisleri, yeni deponun deployment'ı stabil olana kadar eski container'ları çalıştırmaya devam edecektir.
3. Hata anında DNS/WebSocket endpoint yönlendirmeleri eski sunucu portlarına yönlendirilecektir.

---

## 9. Risk Analizi
- **Veritabanı Bağlantı Kesintisi:** Ayrı depoya geçildiğinde DB şemasındaki değişiklikler (örn: `SupportTickets` veya `Customers` kolon güncellemeleri) Ema'yı etkileyebilir. **Önlem:** Database şema kontratı sabitlemesi yapılacak.
- **Ağ Latansı:** Ayrı sunuculara konumlandırma durumunda gecikme artabilir. **Önlem:** Asistan sunucuları veritabanıyla aynı lokal ağda (aynı VPC/subnet) barındırılacaktır.

---

## 10. Geçiş Sırası (Migration Sequence)
1. GitHub üzerinde `ema-companion` adında yeni bir private repository oluşturulması.
2. Lokal geliştirme ortamında `git clone` ile yeni deponun çekilmesi.
3. `gemini-live-standalone/` altındaki dosyaların kopyalanması.
4. Yeni depoda build ve entegrasyon testlerinin (`test_ema_brain.py`) çalıştırılması.
5. Deploy betiklerinin (`sync_deploy.sh` vb.) yeni repoya göre düzenlenmesi.
6. Testlerin onayından sonra monolit depodaki eski dizinin silinmesi.
