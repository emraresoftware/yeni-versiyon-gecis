# 📜 EAOS Constitution (Emare AI Operating System Anayasası)

## Önsöz
Emare AI Operating System (EAOS), insan ve yapay zeka arasındaki etkileşimi en üst seviyeye çıkarmak, işletmeleri tamamen akıllı ve otonom iş akışlarıyla yönetmek üzere tasarlanmış, **Yapay Zeka Öncelikli (AI-First)** bir işletim sistemi ve orkestrasyon platformudur. Bu anayasa, EAOS platformunun temel haklarını, çalışma prensiplerini ve değişmez varoluş kurallarını belirler.

---

## Madde I: Temel İlkeler (Core Values)
1. **AI-First (Yapay Zeka Öncelikli):** Platformdaki tüm modüller, veri modelleri ve arayüzler öncelikle yapay zekanın (ajanların) kolayca okuyup, anlayıp aksiyon alabileceği şekilde tasarlanır.
2. **Privacy by Design (Varsayılan Gizlilik):** Müşteri ve tenant verilerinin güvenliği en üst seviyede tutulur. Hiçbir ham veri maskelenmeden veya izin alınmadan dış yapay zeka servislerine aktarılamaz.
3. **Fault Isolation (Hata İzolasyonu):** Ses, veri ve sunum katmanları birbirinden tamamen bağımsızdır. Bir servisin çökmesi veya API limitlerinin dolması, ana iletişim hattını (telefon) kesintiye uğratamaz.
4. **Conversational Fluency (Akıcılık ve Düşük Gecikme):** İletişimde gerçek zamanlılık esastır. Gecikmeyi artıran mimari kararlar reddedilir.

---

## Madde II: Kiracı (Tenant) Egemenliği
1. Her kiracının verisi, LLM API anahtarları, vektör hafızası ve politikaları birbirlerinden mantıksal veya fiziksel olarak izole edilmiştir.
2. Bir kiracının aşırı kaynak tüketimi veya limiti aşması, diğer kiracıların servis kalitesini veya gecikme sürelerini asla etkileyemez.
3. Kiracılar, kendi AI ajanlarının davranış sınırlarını (Tenant Policy Engine) özgürce belirleme hakkına sahiptir.

---

## Madde III: Ajan Hakları ve Limitleri
1. Ajanlar, platform içinde kendilerine tanımlanan yetki sınırları (`Permission Guard`) dahilinde araçları (`Tools`) çalıştırabilirler.
2. Ajanlar, sistemi sonsuz döngüye sokup gereksiz maliyet yaratmamaları için istek bazlı işlem limiti (max loops) ve bütçe sınırlarına tabidir.
3. Ajanların aldığı tüm kararlar, yaptığı tüm API çağrıları ve logları yöneticiler tarafından şeffaf bir şekilde izlenebilir olmalıdır.

---

## Madde IV: Geliştirici Standartları
1. Her geliştirici (insan veya yapay zeka ajanı), bu anayasaya, `ANAYASA.md` kurallarına ve mimari standartlara uymakla yükümlüdür.
2. Yapılan her kod değişikliği test edilmeli, belgelenmeli ve `Chief Architect` onayından geçmelidir.
3. Geriye dönük uyumluluk (backward compatibility) ve güvenli geri dönüş (rollback) mekanizmaları olmadan hiçbir servis yayına alınamaz.
