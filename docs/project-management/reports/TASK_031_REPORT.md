# Task 031 Report

## Objective

1. Görsel senaryo akışı (visual scenario) ile yapılan test aramalarında, veritabanına kaydedilen senaryo grafik verisinin (GraphDataJson) yapay zeka tarafından eksik/kesik üretilip kaydedilmesinden kaynaklanan JSON format bozukluğunun (truncation) tespit edilmesi ve düzeltilmesi.
2. `VoiceBridgeService` tarafından veritabanından çekilen senaryo grafiğinin doğru şekilde ayrıştırılması ve görsel akıştaki ilk konuşma (speak) düğümünden okunan dinamik karşılama cümlesinin (`greetingText`) santral karşılama ayarına başarıyla enjekte edilmesinin sağlanması.
3. Özel tasarımlarda karşılama metninin başına ziyaretçi ismi/unvanı eklenmesi gibi otomatik kişiselleştirme adımlarının devre dışı bırakılarak, şablondaki karşılama metninin birebir okunmasının sağlanması.
4. Demo Ajanı paneli (`/demo-agent`) üzerinde kullanıcının kendisinin tasarladığı özel demo akışlarını silmesini sağlayacak 'Demoyu Sil' butonunun ve entegrasyonunun eklenmesi.

## Scope

- `src/EmareTicket.API` (VoiceBridgeService.cs)
- `gemini-live-standalone` (standalone_bridge.py)
- `web` (page.tsx)
- `PostgreSQL Database` (VoiceScenarioVersions.GraphDataJson)

## Files Created

- Yok.

## Files Modified

- `src/EmareTicket.API/Services/VoiceBridgeService.cs`
- `gemini-live-standalone/standalone_bridge.py`
- `web/src/app/(dashboard)/demo-agent/page.tsx`

## Architecture Decisions

- **Veritabanı JSON Verisi Onarımı:** `06a32a2c-9397-46cc-a95c-4ded9c256f66` ID'li demo senaryosunun `VoiceScenarioVersions` tablosundaki `GraphDataJson` kolonunda bulunan eksik/kesilmiş JSON verisi tespit edilmiştir. JSON dizesinin sonundaki eksik bağlantı dizisi kapatılarak veritabanı kaydı valid bir JSON nesnesine onarılmıştır.
- **Dinamik Karşılama Enjeksiyonu:** `VoiceBridgeService` içerisinde, görsel senaryo aktif olduğunda grafiğin `nodes` listesindeki ilk `speak` düğümü taranarak içindeki `prompt` metni asenkron olarak okunur ve santral ses köprüsü ayarlarındaki `greetingText` alanına başarıyla enjekte edilir.
- **Süreç Yönlendirme ve Fallback:** Eğer veri tabanındaki senaryo verisi bir sebeple bozuksa veya yüklenemediyse, sistemin çökmesini engellemek amacıyla try-catch bloklarıyla fallback mekanizması işletilerek standart tenant karşılama metnine güvenli dönüş sağlanmıştır.
- **Kişiselleştirme Bypass:** `standalone_bridge.py` üzerinde yapılan geliştirmeyle, arama akışı görsel senaryodan (GUID) tetiklendiğinde `is_custom_scenario` bayrağı aktif edilerek karşılama metninin başına müşteri ismi, 'merhaba' kelimesi veya unvan ekleyen otomatik kişiselleştirme bloğu bypass edilmiş ve kullanıcının tasarladığı şablon metninin birebir okunması sağlanmıştır.
- **Demo Silme Entegrasyonu:** Demo Ajanı arayüzünde, özel akış listesindeki her bir ögeye SweetAlert entegrasyonlu ve React Query mutasyonunu tetikleyen bir silme butonu eklenmiştir. Kart seçimiyle çakışmaması için event propagation önlenmiş ve silme işlemi sonrasında seçili demo otomatik olarak varsayılan ilk şablona yönlendirilmiştir.

## Dependencies Added

- Yok.

## Build Result

| Komut | Sonuç |
|-------|--------|
| `dotnet build EmareTicket.sln` | PASS |

## Test Result

| Komut | Sonuç |
|-------|--------|
| `dotnet test EmareTicket.sln` | PASS — 331/331 test başarıyla tamamlandı |

## Performance Notes

- Grafik verisinin boyutu ve karmaşıklığı ne olursa olsun, ilk düğümün bulunması ve enjeksiyon işlemi doğrusal zamanda O(N) gerçekleştirilerek arama başlatma gecikmesi (latency) minimize edilmiştir.

## Security Notes

- Çoklu kiracı (multi-tenant) veri izolasyonu ve yetkilendirmesi, `CurrentTenantId` ve `IgnoreQueryFilters` kuralları gözetilerek korunmuştur.

## Technical Debt

- Yok — bkz. debt/TECHNICAL_DEBT.md

## Risks

- Yok — bkz. risks/RISK_REGISTER.md

## Known Limitations

- Yapay zeka ile senaryo üretilirken veya güncellenirken, modelin döndüreceği JSON verisinin `MaxTokens` limiti veya bağlantı kopmaları sebebiyle kesik (truncated) gelme ihtimaline karşı veritabanı kayıt aşamasında JSON şeması doğrulama (validation) mekanizması eklenmesi önerilir.

## Breaking Changes

- Yok.

## Next Recommended Task

- Görsel senaryo kaydetme/oluşturma endpoints (`VoiceScenariosController`) seviyesinde gelen JSON string'inin geçerliliğinin (validity) kaydedilmeden önce şema kontrolüyle zorunlu kılınması.
