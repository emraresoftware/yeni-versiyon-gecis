# 💻 EAOS Developer Handbook (Geliştirici Rehberi)

EAOS platformuna hoş geldiniz! Bu rehber, lokal ortamınızı kurmanıza, projeyi çalıştırmanıza ve standartlara uygun kod geliştirmenize yardımcı olacaktır.

---

## 1. Lokal Geliştirme Ortamı Kurulumu

### Gereksinimler:
* **.NET 8 SDK** (Backend API için)
* **Node.js v20+** & npm (Frontend ve Webchat Widget için)
* **Python 3.11+** (Voice Bridge için)
* **Docker & Docker Compose** (PostgreSQL, Redis ve ses servisleri için)

### Depoyu Klonlama ve Ayağa Kaldırma:
```bash
# 1. Projeyi klonlayın
git clone git@github.com:emaredestek/emaredestek.git
cd emaredestek

# 2. Docker bağımlılıklarını başlatın (DB & Redis)
docker compose -f compose.dev.yml up -d postgres redis
```

---

## 2. Projeyi Çalıştırma

### Backend (.NET API):
```bash
# Bağımlılıkları geri yükleyin ve derleyin
dotnet restore
dotnet build

# API'yi çalıştırın (Port 5002)
cd src/EmareTicket.API
dotnet run --urls http://127.0.0.1:5002
```

### Frontend (Next.js):
```bash
cd web
npm install
npm run dev # Next.js Turbopack modunda başlar (Port 3000)
```

### Standalone Voice Bridge (Python):
```bash
cd gemini-live-standalone
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Köprüyü yerel modda başlatın
python3 standalone_bridge.py
```

---

## 3. Yeni Bir Alet (Tool) veya Servis Ekleme Kuralları
1. Ajanların kullanması için yeni bir araç geliştirecekseniz, aracı `agent_registry.py` içinde tanımlayın.
2. Yazdığınız aracın (tool) çalışması için harici bir servise gitmesi gerekiyorsa, bunu **asenkron** yapın ve kesinlikle **1500ms timeout** uygulayın.
3. Araca ait parametrelerin isimlerini `camelCase` formatında yazın ve açıklayıcı desc açıklamaları ekleyin (LLM'in anlaması için kritik).

---

## 4. Test Çalıştırma Protokolü
Değişiklik yaptıktan sonra testleri çalıştırmadan commit atmayın:
```bash
# Backend testlerini çalıştır
dotnet test

# Ses köprüsü testlerini çalıştır
python3 -m unittest discover -s tests/
```
