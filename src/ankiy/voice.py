"""Optional ElevenLabs text-to-speech connector (uses its documented REST API)."""

from __future__ import annotations

from dataclasses import dataclass

import httpx


class VoiceError(RuntimeError):
    """The configured voice could not be generated."""


@dataclass(frozen=True, slots=True)
class ElevenLabsVoice:
    api_key: str
    voice_id: str
    model_id: str = "eleven_multilingual_v2"

    def synthesize(self, text: str) -> bytes:
        """Return an MP3 rendering of one assistant response."""
        clipped = text.strip()[:4_500]
        if not clipped:
            raise VoiceError("There is no text to turn into speech.")
        try:
            response = httpx.post(
                f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}",
                params={"output_format": "mp3_44100_128"},
                headers={"xi-api-key": self.api_key, "Content-Type": "application/json"},
                json={
                    "text": clipped,
                    "model_id": self.model_id,
                    "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
                },
                timeout=90,
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            raise VoiceError("ElevenLabs took too long to generate that voice note.") from error
        except httpx.RequestError as error:
            raise VoiceError("Could not reach ElevenLabs. Check your connection and try again.") from error
        except httpx.HTTPStatusError as error:
            detail = error.response.text[:300]
            raise VoiceError(
                f"ElevenLabs returned HTTP {error.response.status_code}: {detail}"
            ) from error
        if not response.content:
            raise VoiceError("ElevenLabs returned an empty audio file.")
        return response.content
