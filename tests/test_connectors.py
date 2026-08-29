from __future__ import annotations

import base64
from pathlib import Path

import httpx

from ankiy.images import OpenAICompatibleImages
from ankiy.llm import LLMClient
from ankiy.voice import ElevenLabsVoice


def test_llm_client_uses_openai_compatible_messages(monkeypatch) -> None:
    captured: dict = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={"choices": [{"message": {"content": "hello!"}}]},
        )

    monkeypatch.setattr("ankiy.llm.httpx.post", fake_post)
    client = LLMClient("http://local/v1", "tiny", "secret")

    assert client.chat("be warm", [{"role": "user", "content": "hi"}]) == "hello!"
    assert captured["url"] == "http://local/v1/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer secret"
    assert captured["json"]["messages"][0] == {"role": "system", "content": "be warm"}


def test_elevenlabs_connector_posts_voice_and_returns_mp3(monkeypatch) -> None:
    captured: dict = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return httpx.Response(200, request=httpx.Request("POST", url), content=b"fake-mp3")

    monkeypatch.setattr("ankiy.voice.httpx.post", fake_post)
    voice = ElevenLabsVoice(api_key="key", voice_id="voice-id")

    assert voice.synthesize("Hello!") == b"fake-mp3"
    assert captured["url"].endswith("/voice-id")
    assert captured["headers"]["xi-api-key"] == "key"
    assert captured["json"]["model_id"] == "eleven_multilingual_v2"


def test_image_connector_decodes_base64_response(tmp_path: Path, monkeypatch) -> None:
    expected = b"not-really-a-png"

    def fake_post(url, **kwargs):
        return httpx.Response(
            200,
            request=httpx.Request("POST", url),
            json={"data": [{"b64_json": base64.b64encode(expected).decode("ascii")}]} ,
        )

    monkeypatch.setattr("ankiy.images.httpx.post", fake_post)
    images = OpenAICompatibleImages(
        api_key="key",
        base_url="https://example.test/v1",
        model="image-model",
        size="1024x1024",
        media_dir=tmp_path,
    )

    result = images.generate_selfie("An original fictional companion")
    assert result.path.suffix == ".png"
    assert result.path.read_bytes() == expected
