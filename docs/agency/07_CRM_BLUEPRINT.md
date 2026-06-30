# 👥 07_CRM_BLUEPRINT.md (CRM Entegrasyon Standartları)

Bu kılavuz, müşteri ilişkileri verilerinin (Müşteriler, Kişiler, Aktiviteler, Biletler) EAOS ile nasıl senkronize olacağını tanımlar.

---

## 1. CRM İlişkisel Modeli
* **Customers:** Şirket veya bireysel müşteri ana kartı.
* **Contacts:** Şirket altındaki yetkili kişiler ve iletişim bilgileri.
* **Activities:** Telefon görüşmesi özetleri, gönderilen mailler, yapılan toplantılar.

---

## 2. Ajan Etkileşimi
* Telefon araması bittiğinde, `CallSummaryAgent` ses kaydının özetini otomatik çıkartır ve bunu ilgili müşterinin `Activities` geçmişine bir log olarak ekler.
* Ajan, konuşma esnasında müşteriden aldığı bilgileri (örn: e-posta veya adres değişikliği) `update_customer_context` aracı ile sessizce CRM'e işler.
