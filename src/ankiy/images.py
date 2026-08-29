"""Optional image generation for clearly fictional companion selfies."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import httpx


class ImageError(RuntimeError):
    """The configured image provider could not generate an avatar image."""


@dataclass(frozen=True, slots=True)
class ImageResult:
    path: Path
    revised_prompt: str | None = None


@dataclass(frozen=True, slots=True)
class OpenAICompatibleImages:
    """Connector for OpenAI-compatible `/images/generations` endpoints.

    It supports `b64_json` responses and URL responses, which covers common hosted
    implementations. Keep this connector optional: local chat itself needs no cloud API.
    """

    api_key: str
    base_url: str
    model: str
    size: str
    media_dir: Path

    def generate_selfie(self, prompt: str) -> ImageResult:
        try:
            response = httpx.post(
                f"{self.base_url}/images/generations",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "size": self.size,
                    "n": 1,
                    "response_format": "b64_json",
                },
                timeout=150,
            )
            response.raise_for_status()
        except httpx.TimeoutException as error:
            raise ImageError("The image provider took too long. Try a simpler selfie scene.") from error
        except httpx.RequestError as error:
            raise ImageError("Could not reach the image provider. Check IMAGE_BASE_URL.") from error
        except httpx.HTTPStatusError as error:
            raise ImageError(
                f"The image provider returned HTTP {error.response.status_code}: "
                f"{error.response.text[:350]}"
            ) from error

        try:
            item = response.json()["data"][0]
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ImageError("The image provider returned an unexpected response format.") from error

        data: bytes
        extension = ".png"
        if isinstance(item.get("b64_json"), str):
            try:
                data = base64.b64decode(item["b64_json"], validate=True)
            except ValueError as error:
                raise ImageError("The image provider returned invalid image data.") from error
        elif isinstance(item.get("url"), str):
            # Some compatible APIs return a temporary image URL instead of b64 data.
            try:
                download = httpx.get(item["url"], timeout=90, follow_redirects=True)
                download.raise_for_status()
            except httpx.HTTPError as error:
                raise ImageError("The generated image URL could not be downloaded.") from error
            data = download.content
            content_type = download.headers.get("content-type", "")
            if "jpeg" in content_type:
                extension = ".jpg"
            elif "webp" in content_type:
                extension = ".webp"
        else:
            raise ImageError("The image provider returned neither image data nor a download URL.")

        if not data:
            raise ImageError("The image provider returned an empty image.")
        self.media_dir.mkdir(parents=True, exist_ok=True)
        path = self.media_dir / f"selfie-{uuid4().hex[:12]}{extension}"
        path.write_bytes(data)
        revised = item.get("revised_prompt")
        return ImageResult(path=path, revised_prompt=revised if isinstance(revised, str) else None)
