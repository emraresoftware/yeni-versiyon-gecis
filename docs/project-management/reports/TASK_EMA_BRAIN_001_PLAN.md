# Implementation Plan - TASK-EMA-BRAIN-001 Ema Brain Orchestrator

Ema Desktop Assistant'ı bir dijital çalışma arkadaşı (AI Agent) seviyesine getirmek üzere "Ema Brain" orkestrasyon katmanının tasarlanması ve yerel Python ses köprüsü entegrasyonu.

## Technical Scope
- **Intent Engine & Planner:** Kullanıcının girdilerini çözümleyerek niyet/aksiyon kodu belirleme ve karmaşık istekleri alt görev listelerine bölme.
- **Tool Router:** GitHub, ERP, CRM, Unity, Memory, Calendar, Mail, Browser araçlarına yönlendirme.
- **Response Generator:** Yanıtın ses, kısa metin, uzun metin veya UI (kullanıcı arayüzü) formatlarından hangisine en uygun olduğuna karar verme.
- **Context Builder:** Aktif görev, konuşma geçmişi ve proje bağlamını birleştirerek LLM'e sunma.
- **Safety Layer:** Silme, para ve kritik işlemlerde açık kullanıcı onayı (`requires_approval`) isteme.
- **Task Queue:** Sıralı görev listesini (onay süreçleri dahil) adım adım yönetme.

## Proposed Changes

### [New] [ema_brain.py](file:///Users/emre/Elyafgroup/gemini-live-standalone/ema_brain.py)
Tüm 7 orkestrasyon katmanını barındıran asenkron Python sınıfı.

### [New] [test_ema_brain.py](file:///Users/emre/Elyafgroup/gemini-live-standalone/test_ema_brain.py)
Intent, planlama, güvenlik kontrolü ve araç yönlendirme senaryolarını test eden entegrasyon script'i.

## Verification Plan
- `python3 test_ema_brain.py` entegrasyon testinin çalıştırılarak tüm adımların doğrulanması.
