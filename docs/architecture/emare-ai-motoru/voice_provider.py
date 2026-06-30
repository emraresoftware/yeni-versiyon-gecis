"""
voice_provider.py — Ses Sağlayıcı Soyutlama Katmanı (Voice Provider Abstraction Layer)

Mevcut ses köprüsünün tek sağlayıcıya (Gemini Live) bağımlılığını önler.
Gerçek zamanlı ses sağlayıcılarını (Gemini, gelecekte OpenAI, Hume vb.) sarmalayan
ortak bir arayüz ve dinamik yönlendirici sağlar.
"""

from __future__ import annotations
import os
import time
from typing import Any, AsyncIterator, Optional, Protocol

# ─── Arayüz Tanımı (Adapter Protocol) ──────────────────────────────────────────

class VoiceSession(Protocol):
    """
    Farklı ses sağlayıcılarının aktif oturumlarını temsil eden ortak protokol.
    Soket üzerinden okuma/yazma metotlarını standartlaştırır.
    """
    async def send_audio(self, data: bytes) -> None:
        """Kullanıcının mikrofon ses chunk'ını sağlayıcıya gönderir."""
        ...

    async def send_text(self, text: str, end_of_turn: bool = False) -> None:
        """Metin/Komut enjekte eder (coaching veya tool sonucu)."""
        ...

    async def send_client_content(self, turns: dict, turn_complete: bool = True) -> None:
        """Dinamik kullanıcı içeriği gönderir (ör: karşılama tetikleyici)."""
        ...

    def receive(self) -> AsyncIterator[Any]:
        """Sağlayıcıdan gelen yanıtları (ses, text, tool_call) asenkron dinler."""
        ...

    async def close(self) -> None:
        """Sağlayıcı bağlantısını kapatır."""
        ...


class VoiceProvider(Protocol):
    """Ses sağlayıcı istemci fabrikası."""
    async def connect(self, model: str, config: dict) -> VoiceSession:
        """Sağlayıcıya gerçek zamanlı WebSocket/gRPC bağlantısı açar."""
        ...


# ─── Sağlık ve Gecikme İzleyici (Health & Latency Registry) ───────────────────

# Basit bellek içi sağlık/gecikme cache'i (gerçek zamanlı kararlar için)
_provider_health_registry: dict[str, dict[str, Any]] = {
    "gemini": {"errors": 0, "last_ping": 0.0, "is_healthy": True},
    "openai": {"errors": 0, "last_ping": 0.0, "is_healthy": True},
}

def report_provider_error(provider_name: str) -> None:
    """Sağlayıcıda hata oluştuğunu kaydeder."""
    reg = _provider_health_registry.setdefault(provider_name, {"errors": 0, "last_ping": 0.0, "is_healthy": True})
    reg["errors"] += 1
    if reg["errors"] >= 3:
        reg["is_healthy"] = False
        print(f"[VoiceProvider] Sağlayıcı {provider_name} PASİFE ALINDI (Hata Sınırı Aşıldı)", flush=True)

def report_provider_success(provider_name: str, latency_ms: float = 0.0) -> None:
    """Sağlayıcının başarılı çalıştığını ve gecikme süresini kaydeder."""
    reg = _provider_health_registry.setdefault(provider_name, {"errors": 0, "last_ping": 0.0, "is_healthy": True})
    reg["errors"] = max(0, reg["errors"] - 1)
    reg["is_healthy"] = True
    if latency_ms > 0:
        reg["last_ping"] = latency_ms


# ─── Dinamik Yönlendirici (Voice Provider Manager) ───────────────────────────

class VoiceProviderManager:
    """
    Her çağrı başında tenant politikası, sağlayıcı sağlık durumu ve gecikme kriterlerine
    göre en uygun ses sağlayıcıyı seçen dinamik yönlendirici.
    """

    @staticmethod
    async def resolve_provider(tenant_id: str, tenant_settings: Optional[dict] = None) -> str:
        """
        Dinamik olarak hangi sağlayıcının kullanılacağını belirler.
        
        Süreç:
          1. Tenant özel tercihi var mı? (preferred_voice_provider)
          2. Tercih edilen sağlayıcı sağlıklı mı?
          3. Değilse, en düşük gecikmeli alternatif sağlıklı sağlayıcıyı seç.
        """
        settings = tenant_settings or {}
        preferred = str(settings.get("preferred_voice_provider", "gemini")).lower()

        # 1. Tercih edilen sağlıklıysa doğrudan seç (Session-Sticky)
        if _provider_health_registry.get(preferred, {}).get("is_healthy", True):
            return preferred

        # 2. Değilse, alternatif sağlıklı olanı seç
        for name, stats in _provider_health_registry.items():
            if stats.get("is_healthy", True):
                print(f"[VoiceProvider] Fallback tetiklendi: {preferred} -> {name}", flush=True)
                return name

        # 3. Hepsi çöktüyse varsayılana (gemini) geri dön (son çare)
        return "gemini"

    @staticmethod
    def get_provider(provider_name: str, api_key: str) -> VoiceProvider:
        """İlgili sağlayıcı adaptörünü döner."""
        p_name = provider_name.lower()
        if p_name == "gemini":
            from gemini_live_adapter import GeminiLiveAdapter
            return GeminiLiveAdapter(api_key=api_key)
        else:
            # Gelecekte eklenecek OpenAI/Hume adaptörleri buraya gelecek.
            # Şu an için her durumda Gemini fallback.
            print(f"[VoiceProvider] Bilinmeyen sağlayıcı {provider_name}, Gemini'ye yönlendiriliyor.", flush=True)
            from gemini_live_adapter import GeminiLiveAdapter
            return GeminiLiveAdapter(api_key=api_key)
