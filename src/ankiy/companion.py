"""The application service that joins personality, local memory, and integrations."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .config import Settings
from .llm import LLMClient, LLMError
from .memory import MemoryStore
from .personality import Personality, list_personalities, load_personality


SELFIE_PATTERN = re.compile(
    r"\b(?:send|show|take|make|create|generate|want|can i have|give me|share)\b[^.?!]{0,80}\bselfie\b"
    r"|\bselfie\b[^.?!]{0,80}\b(?:please|now|of you|with|at|in)\b",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class ChatResult:
    text: str
    personality: Personality
    warning: str | None = None


class Companion:
    """A stateful companion facade; each channel receives an isolated conversation."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.settings.ensure_directories()
        self.memory = MemoryStore(settings.database_path)
        self.memory.initialize()
        self.llm = LLMClient(
            base_url=settings.llm_base_url,
            model=settings.llm_model,
            api_key=settings.llm_api_key,
        )

    def profile_for(self, conversation_id: str) -> Personality:
        key = self.memory.profile_for(conversation_id, self.settings.default_profile)
        return load_personality(self.settings.profile_dir, key)

    def available_profiles(self) -> list[str]:
        return list_personalities(self.settings.profile_dir)

    def switch_profile(self, conversation_id: str, key: str) -> Personality:
        personality = load_personality(self.settings.profile_dir, key)
        self.memory.switch_profile(conversation_id, key)
        return personality

    def greeting(self, conversation_id: str) -> str:
        personality = self.profile_for(conversation_id)
        return personality.first_message.format(owner_name=self.settings.owner_name)

    def reply(self, conversation_id: str, user_text: str) -> ChatResult:
        clean = user_text.strip()
        if not clean:
            raise ValueError("Say something first — I’m listening.")
        if len(clean) > 8_000:
            raise ValueError("That message is a little long. Please send it in smaller pieces.")

        personality = self.profile_for(conversation_id)
        history = [
            {"role": message.role, "content": message.content}
            for message in self.memory.recent(conversation_id)
        ]
        prompt_messages = [*history, {"role": "user", "content": clean}]
        warning: str | None = None
        try:
            answer = self.llm.chat(personality.system_prompt(self.settings.owner_name), prompt_messages)
        except LLMError as error:
            answer = self._offline_reply(personality, clean)
            warning = str(error)

        self.memory.append(conversation_id, "user", clean)
        self.memory.append(conversation_id, "assistant", answer)
        return ChatResult(text=answer, personality=personality, warning=warning)

    def clear(self, conversation_id: str) -> None:
        self.memory.clear(conversation_id)

    def voice_is_on(self, conversation_id: str) -> bool:
        return self.memory.voice_enabled(conversation_id, self.settings.default_profile)

    def set_voice(self, conversation_id: str, enabled: bool) -> None:
        self.memory.set_voice_enabled(conversation_id, self.settings.default_profile, enabled)

    @staticmethod
    def asks_for_selfie(text: str) -> bool:
        """Recognize an unambiguous request without charging for casual mentions."""
        return bool(SELFIE_PATTERN.search(text))

    @staticmethod
    def selfie_scene(text: str) -> str:
        """Turn either `/selfie scene` or a natural request into a scene hint."""
        scene = re.sub(r"^/selfie\s*", "", text.strip(), flags=re.IGNORECASE)
        scene = re.sub(r"\b(?:please|can you|could you|send|show|take|make|create|generate)\b", "", scene, flags=re.I)
        scene = re.sub(r"\b(?:a |an |me |your |you |of you )?selfie\b", "", scene, flags=re.I)
        return scene.strip(" ,.-") or "a cozy everyday moment"

    @staticmethod
    def _offline_reply(personality: Personality, user_text: str) -> str:
        """A transparent graceful state while onboarding a local model."""
        excerpt = user_text.strip().replace("\n", " ")[:120]
        return (
            f"I caught “{excerpt}.” I’m in a tiny offline starter mode right now, "
            f"so I can’t give you {personality.name}’s full model-powered reply yet. "
            "Start Ollama and pull the model from the quick-start guide, then try me again — "
            "I’ll keep this conversation waiting here."
        )
