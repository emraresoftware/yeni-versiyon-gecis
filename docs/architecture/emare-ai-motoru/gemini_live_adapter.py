"""
gemini_live_adapter.py — Gemini Live API Ses Sağlayıcı Adaptörü

Google GenAI SDK (client.aio.live.connect) WebSocket oturumunu
Voice Provider Abstraction Layer (VoiceSession) protokolüne uyumlu hale getirir.
"""

from __future__ import annotations
import asyncio
from typing import Any, AsyncIterator
from google import genai
from voice_provider import VoiceSession, VoiceProvider


class GeminiLiveSession(VoiceSession):
    """Gemini Live WebSocket oturumunu sarmalar."""

    def __init__(self, raw_session: Any) -> None:
        self._session = raw_session

    async def send_realtime_input(self, audio: Any) -> None:
        """Mikrofon sesini doğrudan Gemini Live API'ye iletir."""
        await self._session.send_realtime_input(audio=audio)

    async def send(self, input: Any, end_of_turn: bool = True) -> None:
        """Metin enjekte eder."""
        await self._session.send(input=input, end_of_turn=end_of_turn)

    async def send_client_content(self, turns: Any, turn_complete: bool = True) -> None:
        """Dinamik kullanıcı komutlarını iletir."""
        await self._session.send_client_content(turns=turns, turn_complete=turn_complete)

    async def receive(self) -> AsyncIterator[Any]:
        """Gemini Live WebSocket'tan gelen akışı dinler."""
        async for response in self._session.receive():
            yield response

    async def close(self) -> None:
        """Bağlantıyı kapatır."""
        # GenAI SDK'da close aio.live.connect context manager tarafından otomatik yapılır.
        # Manuel kapatma gerekirse eklenebilir.
        pass


class GeminiLiveAdapter(VoiceProvider):
    """Google Gemini Live ses sağlayıcı adaptörü."""

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    async def connect(self, model: str, config: dict) -> VoiceSession:
        """Gemini Live API'ye WebSocket bağlantısı kurar."""
        client = genai.Client(api_key=self.api_key)
        
        # dynamic_connect ile asenkron aio.live.connect başlatılır.
        # Bu nesne normalde bir async context manager'dır.
        # Onu manuel olarak __aenter__ ile tetikleyerek session'ı alırız.
        context_mgr = client.aio.live.connect(model=model, config=config)
        raw_session = await context_mgr.__aenter__()
        
        # Bağlam yöneticisini kapatabilmek için oturum referansını saklarız.
        session = GeminiLiveSession(raw_session)
        session._context_mgr = context_mgr
        return session
