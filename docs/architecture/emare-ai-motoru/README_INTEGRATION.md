# Gemini Live Standalone Entegrasyon Detayları

Bu belgede, standalone Gemini Live ses köprüsü (`standalone_bridge.py`) üzerinde gerçekleştirilen veritabanı entegrasyonu, dinamik karşılama, araç kullanımı (tool calling) ve ses eşleme geliştirmelerinin detayları yer almaktadır.

---

## 📂 Proje Konumları

- **Lokal Geliştirme Klasörü:** `/Users/emre/elyafgroup/gemini-live-standalone`
- **107 Sunucusu Canlı Klasörü:** `/opt/gemini-live-standalone`

---

## 🛠 Yapılan Geliştirmeler ve Mimari Detaylar

### 1. Veritabanı Bağlantı Yönetimi
- **Bağımlılık:** `requirements.txt` dosyasına `asyncpg` kütüphanesi eklendi.
- **Havuz Yönetimi:** Köprü başlatılırken `asyncpg.create_pool` kullanılarak PostgreSQL (`EmareTicketProd`) için asenkron bağlantı havuzu oluşturuldu.
- **Ağ Entegrasyonu:** `compose.yml` üzerinde köprü konteyneri `emareticket-prod_emareticket-prod-net` ağına dahil edildi ve veritabanı bağlantı bilgileri ortam değişkenleri olarak tanımlandı.

### 2. Arayıcı Kimliği ve Kiracı (Tenant) Çözümleme
- **Özel UUID Protokolü:** Asterisk tarafında arayanın DID (Hedef Numara) ve CallerID (Arayan Numara) bilgileri AudioSocket UUID formatına uygun şekilde paketlendi:
  `DID_PART1(8)-DID_PART2(4)-4000-8000-CALLERID(12)`
- **UUID Ayrıştırma:** Köprü gelen bağlantıdaki UUID değerini çözerek DID ve CallerID bilgilerini elde eder.
- **Trunk & Tenant Bulma:** DID üzerinden `SipTrunks` tablosunda aktif kayıt sorgulanarak ilgili `TenantId` çözümlenir.
- **Müşteri Tanıma:** Arayan numaranın son 7 hanesi kullanılarak sırasıyla `CustomerContacts` ve `Customers` tablolarında arama yapılır.
- **Türkçe Cinsiyet Ünvanı:** Bulunan ismin ilk kelimesi Türkçe kadın isimleri listesi (`FEMALE_NAMES`) ile karşılaştırılıp kişiye göre otomatik olarak **"Bey"** veya **"Hanım"** ünvanı atanır.

### 3. Dinamik Eğitim Promptu ve Karşılama
- **Prompt Çekme:** Veritabanındaki `Tenants` tablosundan kiracıya ait `AgentSystemPromptOverride` (sistem eğitimi) ve `AgentCustomSettings` (karşılama ayarları) dinamik olarak çekilir.
- **Acar Telekom Örneği:** Acar Telekom (`232100` DID'li arama) kiracısı için veritabanında kayıtlı olan *"Burcu"* isimli sesli asistan promptu ve sanal santral/metro ethernet ürün bilgileri dinamik olarak yüklenir.
- **Kişiselleştirilmiş Karşılama:** `greetingText` ayarındaki `{CustomerName}` şablonu çözülür. Şablon yoksa karşılama mesajının başına arayanın adı ve ünvanı eklenerek selamlanır (*ör: "Emre Bey merhaba..."*).

### 4. Fonksiyon Çağrıları (Tool Calling)
Müşteriyle konuşma esnasında asistanın kullanabileceği iki adet yerel veritabanı aracı entegre edildi:

#### A. `check_ticket_status` (Bilet Sorgulama)
- Gemini Live asistanına `check_ticket_status` fonksiyon bildirimi sunulur.
- Tetiklendiğinde, müşterinin (`CustomerId`) veritabanındaki son 5 aktif biletini sorgular ve aşama bilgilerini (Açıldı, Çalışılıyor, Tamamlandı) asistanın sesli okuması için geri döner.

#### B. `create_support_ticket` (Destek Talebi Oluşturma)
- Asistanın bilet oluşturabilmesi için `create_support_ticket(title, description)` aracı sunulur.
- Tetiklendiğinde:
  1. Veritabanındaki son bilet numarasını alarak `ST000001` formatında yeni bir bilet numarası üretir.
  2. Bilet tablosuna (`SupportTickets`) yeni kaydı ekler.
  3. Bilet geçmişine (`SupportTicketActivities`) arama kanalıyla oluşturulduğuna dair başlangıç notunu yazar.
  4. Oluşturulan bilet numarasını sesli asistanın arayana bildirmesi için geri döner.

### 5. Dinamik Ses Eşleştirici (Voice Mapper)
- Veritabanındaki `AgentVoiceId` kolonu sorgulanır.
- Gemini Live yalnızca Google prebuilt seslerini kabul ettiği için (örn: `Kore`, `Puck`, `Aoede`), veritabanında kayıtlı olan harici sesler (örneğin Acar Telekom'un kullandığı `"EdaVoice"`) dinamik olarak Türkçe destekleyen sıcak kadın sesi olan **`Kore`** sesine eşleştirilir.

### 6. Ağ Çakışması Düzeltmesi (Bugfix)
- Canlı Docker ortamında aynı ağda iki adet `voice-bridge` isimli servis bulunmasından kaynaklanan DNS çakışması çözüldü.
- Standalone köprünün servis adı `standalone-voice-bridge` ve Asterisk AudioSocket yönlendirmesi `standalone-voice-bridge:8095` olarak güncellenerek izole edildi.

---

## 🚀 Değişiklikleri Canlıya Alma Adımları

Herhangi bir kod güncellemesi yapıldığında 107 sunucusunda şu komutlar çalıştırılır:

```bash
# 1. Güncel dosyaları sunucuya kopyalayın
scp gemini-live-standalone/standalone_bridge.py root@185.189.54.107:/opt/gemini-live-standalone/standalone_bridge.py
scp gemini-live-standalone/compose.yml root@185.189.54.107:/opt/gemini-live-standalone/compose.yml
scp gemini-live-standalone/asterisk_config/extensions.conf root@185.189.54.107:/opt/gemini-live-standalone/asterisk_config/extensions.conf

# 2. Sunucuya bağlanın ve konteynerleri yeniden derleyip ayağa kaldırın
ssh root@185.189.54.107 "cd /opt/gemini-live-standalone && docker compose up -d --build --remove-orphans"

# 3. Asterisk Dialplan'ını reload edin
ssh root@185.189.54.107 "docker exec -t standalone-asterisk asterisk -rx 'dialplan reload'"
```
