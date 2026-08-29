from __future__ import annotations

from pathlib import Path

from ankiy.companion import Companion
from ankiy.config import Settings
from ankiy.llm import LLMError
from ankiy.memory import MemoryStore
from ankiy.personality import load_personality


ROOT = Path(__file__).resolve().parents[1]


def settings_for(tmp_path: Path) -> Settings:
    return Settings(
        llm_base_url="http://localhost:11434/v1",
        llm_model="test-model",
        llm_api_key=None,
        owner_name="Sam",
        default_profile="luna",
        data_dir=tmp_path / "data",
        profile_dir=ROOT / "profiles",
        media_dir=tmp_path / "media",
        telegram_bot_token=None,
    )


def test_profile_renders_owner_and_fictional_selfie_prompt() -> None:
    luna = load_personality(ROOT / "profiles", "luna")

    assert "Sam" in luna.first_message.format(owner_name="Sam")
    selfie = luna.selfie_prompt("reading by a rainy window")
    assert "Luna" in selfie
    assert "clearly fictional" in selfie
    assert "rainy window" in selfie


def test_memory_switches_profile_and_resets_context(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path / "ankiy.sqlite3")
    store.initialize()
    assert store.profile_for("local", "luna") == "luna"
    store.append("local", "user", "hello")
    store.append("local", "assistant", "hi")

    assert [message.content for message in store.recent("local")] == ["hello", "hi"]
    store.switch_profile("local", "pip")

    assert store.profile_for("local", "luna") == "pip"
    assert store.recent("local") == []


def test_companion_passes_recent_history_and_remembers_reply(tmp_path: Path) -> None:
    companion = Companion(settings_for(tmp_path))

    class FakeLLM:
        def __init__(self) -> None:
            self.calls: list[tuple[str, list[dict[str, str]]]] = []

        def chat(self, system: str, messages: list[dict[str, str]]) -> str:
            self.calls.append((system, messages))
            return "A warm answer."

    fake = FakeLLM()
    companion.llm = fake  # type: ignore[assignment]

    first = companion.reply("local:owner", "Hello there")
    second = companion.reply("local:owner", "What should we do?")

    assert first.text == "A warm answer."
    assert second.warning is None
    system, second_request = fake.calls[1]
    assert "Sam" in system
    assert second_request == [
        {"role": "user", "content": "Hello there"},
        {"role": "assistant", "content": "A warm answer."},
        {"role": "user", "content": "What should we do?"},
    ]


def test_companion_uses_transparent_starter_message_when_model_is_offline(tmp_path: Path) -> None:
    companion = Companion(settings_for(tmp_path))

    class BrokenLLM:
        def chat(self, system: str, messages: list[dict[str, str]]) -> str:
            raise LLMError("Could not reach the chat model")

    companion.llm = BrokenLLM()  # type: ignore[assignment]
    result = companion.reply("local:owner", "Are you there?")

    assert result.warning == "Could not reach the chat model"
    assert "offline starter mode" in result.text
    assert "Are you there?" in result.text


def test_selfie_detector_requires_a_request_not_a_casual_mention() -> None:
    assert Companion.asks_for_selfie("Could you send a selfie by the lake?")
    assert Companion.asks_for_selfie("A selfie of you, please")
    assert not Companion.asks_for_selfie("I saw a selfie trend today")
    assert Companion.selfie_scene("Send a selfie at a rainy cafe") == "at a rainy cafe"
