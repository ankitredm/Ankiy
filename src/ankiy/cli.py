"""Friendly command-line entry point for the local-first starter experience."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import httpx

from .companion import Companion
from .config import PROJECT_ROOT, Settings
from .images import ImageError, OpenAICompatibleImages
from .personality import load_personality
from .voice import ElevenLabsVoice, VoiceError

LOCAL_CONVERSATION_ID = "local:owner"
HELP = """Commands
  /help                 Show this menu
  /profiles             List personalities
  /profile <name>       Switch personality (starts a fresh chat context)
  /clear                Clear this companion's local chat context
  /voice on|off         Toggle ElevenLabs voice notes for this conversation
  /selfie [scene]       Generate a fictional companion selfie (optional image key)
  /quit                 Leave the chat

Tip: “send me a selfie at a rainy café” also works when image generation is set up.
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ankiy",
        description="A local-first, customizable AI companion.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    subcommands.add_parser("init", help="create a private .env from the example")
    subcommands.add_parser("doctor", help="check profiles, providers, and optional features")

    chat = subcommands.add_parser("chat", help="start a chat in this terminal")
    chat.add_argument("--profile", help="personality profile to use for this local conversation")

    telegram = subcommands.add_parser("telegram", help="run the optional Telegram bot")
    telegram.add_argument("--drop-pending", action="store_true", help="ignore messages sent while offline")

    profiles = subcommands.add_parser("profiles", help="list editable personality profiles")
    profiles.add_argument("--show", metavar="NAME", help="print details for one profile")
    return parser


def _init(settings: Settings) -> int:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        print(f"✓ {env_path.name} already exists; I left it untouched.")
    else:
        shutil.copyfile(PROJECT_ROOT / ".env.example", env_path)
        print("✓ Created .env from .env.example — add only the integrations you want.")
    settings.ensure_directories()
    print("✓ Created private data/ and media/ folders.")
    print("\nNext, for local chat:\n  1. Install Ollama: https://ollama.com\n  2. ollama pull llama3.2\n  3. ankiy chat")
    return 0


def _doctor(settings: Settings, companion: Companion) -> int:
    print("Ankiy checkup\n" + "─" * 42)
    profiles = companion.available_profiles()
    if settings.default_profile in profiles:
        print(f"✓ Profile: {settings.default_profile} (found {len(profiles)} profile(s))")
    else:
        print(f"✗ Default profile '{settings.default_profile}' is missing from {settings.profile_dir}")

    # `/models` is lightweight and implemented by Ollama and most OpenAI-compatible APIs.
    try:
        response = httpx.get(
            f"{settings.llm_base_url}/models",
            headers={"Authorization": f"Bearer {settings.llm_api_key}"} if settings.llm_api_key else {},
            timeout=4,
        )
        response.raise_for_status()
        print(f"✓ Chat endpoint: reachable at {settings.llm_base_url} (model: {settings.llm_model})")
    except httpx.HTTPError:
        print(f"! Chat endpoint: not reachable at {settings.llm_base_url}")
        print("  For the default local setup: start Ollama, then run `ollama pull llama3.2`.")

    print(
        "✓ ElevenLabs voice: configured" if settings.voice_enabled else
        "○ ElevenLabs voice: optional — add ELEVENLABS_API_KEY + ELEVENLABS_VOICE_ID to enable"
    )
    print(
        "✓ AI selfies: configured" if settings.images_enabled else
        "○ AI selfies: optional — add IMAGE_API_KEY to enable"
    )
    if settings.telegram_bot_token:
        if settings.telegram_allowed_user_ids:
            print("✓ Telegram: token and private allow-list configured")
        else:
            print("! Telegram: token exists, but TELEGRAM_ALLOWED_USER_IDS is empty (bot will stay locked)")
    else:
        print("○ Telegram: optional — add TELEGRAM_BOT_TOKEN to enable")
    return 0 if settings.default_profile in profiles else 1


def _show_profiles(companion: Companion, selected: str | None) -> int:
    if selected:
        try:
            profile = load_personality(companion.settings.profile_dir, selected)
        except (FileNotFoundError, ValueError) as error:
            print(f"Profile error: {error}", file=sys.stderr)
            return 1
        print(f"{profile.name} — {profile.tagline}\n\n{profile.description}")
        print("\nTraits: " + ", ".join(profile.traits))
        print("\nVisual style: " + profile.visual_style)
        return 0
    print("Available personalities:")
    for key in companion.available_profiles():
        profile = load_personality(companion.settings.profile_dir, key)
        marker = " (default)" if key == companion.settings.default_profile else ""
        print(f"  {key:<12} {profile.name} — {profile.tagline}{marker}")
    print("\nDuplicate and edit a YAML file in profiles/ to create your own.")
    return 0


def _image_service(settings: Settings) -> OpenAICompatibleImages | None:
    if not settings.images_enabled or not settings.image_api_key:
        return None
    return OpenAICompatibleImages(
        api_key=settings.image_api_key,
        base_url=settings.image_base_url,
        model=settings.image_model,
        size=settings.image_size,
        media_dir=settings.media_dir,
    )


def _voice_service(settings: Settings) -> ElevenLabsVoice | None:
    if not settings.voice_enabled or not settings.elevenlabs_api_key or not settings.elevenlabs_voice_id:
        return None
    return ElevenLabsVoice(
        api_key=settings.elevenlabs_api_key,
        voice_id=settings.elevenlabs_voice_id,
        model_id=settings.elevenlabs_model,
    )


def _make_selfie(companion: Companion, conversation_id: str, scene: str) -> None:
    profile = companion.profile_for(conversation_id)
    service = _image_service(companion.settings)
    if not service:
        print(
            "Selfies are not configured yet. Add IMAGE_API_KEY (and optionally IMAGE_MODEL) "
            "to .env; then run `/selfie a rainy café`.",
        )
        return
    print(f"{profile.name} is finding the good light…")
    try:
        result = service.generate_selfie(profile.selfie_prompt(scene))
    except ImageError as error:
        print(f"Selfie error: {error}")
        return
    print(f"Fictional {profile.name} avatar saved to: {result.path}")


def _save_voice(companion: Companion, text: str) -> None:
    if not companion.voice_is_on(LOCAL_CONVERSATION_ID):
        return
    service = _voice_service(companion.settings)
    if not service:
        print("(Voice is toggled on, but ElevenLabs is not configured in .env.)")
        return
    print("(Turning that into a voice note…)")
    try:
        audio = service.synthesize(text)
    except VoiceError as error:
        print(f"(Voice note unavailable: {error})")
        return
    path = companion.settings.media_dir / "latest-reply.mp3"
    path.write_bytes(audio)
    print(f"(Voice note saved to {path}; play it with your usual audio app.)")


def _handle_slash_command(companion: Companion, line: str) -> bool:
    command, _, argument = line.partition(" ")
    command = command.lower()
    argument = argument.strip()
    if command in {"/quit", "/exit"}:
        return False
    if command == "/help":
        print(HELP)
    elif command == "/profiles":
        _show_profiles(companion, None)
    elif command == "/profile":
        if not argument:
            print("Usage: /profile <name>  (or use /profiles)")
        else:
            try:
                profile = companion.switch_profile(LOCAL_CONVERSATION_ID, argument)
                print(f"\nSwitched to {profile.name}. {companion.greeting(LOCAL_CONVERSATION_ID)}\n")
            except (FileNotFoundError, ValueError) as error:
                print(f"Profile error: {error}")
    elif command == "/clear":
        companion.clear(LOCAL_CONVERSATION_ID)
        print("Fresh page. Your saved conversation context is cleared. ✦")
    elif command == "/voice":
        if argument.lower() not in {"on", "off"}:
            state = "on" if companion.voice_is_on(LOCAL_CONVERSATION_ID) else "off"
            print(f"Voice is {state}. Use /voice on or /voice off.")
        else:
            companion.set_voice(LOCAL_CONVERSATION_ID, argument.lower() == "on")
            print(f"Voice turned {argument.lower()} for this conversation.")
            if argument.lower() == "on" and not companion.settings.voice_enabled:
                print("Add ELEVENLABS_API_KEY and ELEVENLABS_VOICE_ID in .env to generate audio.")
    elif command == "/selfie":
        _make_selfie(companion, LOCAL_CONVERSATION_ID, argument or "a cozy everyday moment")
    else:
        print("I don’t know that command. Type /help for the little map.")
    return True


def _chat(settings: Settings, profile: str | None) -> int:
    companion = Companion(settings)
    if profile:
        try:
            companion.switch_profile(LOCAL_CONVERSATION_ID, profile)
        except (FileNotFoundError, ValueError) as error:
            print(f"Profile error: {error}", file=sys.stderr)
            return 1
    try:
        personality = companion.profile_for(LOCAL_CONVERSATION_ID)
    except (FileNotFoundError, ValueError) as error:
        print(f"Setup error: {error}", file=sys.stderr)
        return 1
    print(f"\n{personality.name} · {personality.tagline}\nType /help for companion controls; /quit to leave.\n")
    print(f"{personality.name} > {companion.greeting(LOCAL_CONVERSATION_ID)}\n")
    while True:
        try:
            line = input("you > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSee you soon. ✦")
            return 0
        if not line:
            continue
        if line.startswith("/"):
            if not _handle_slash_command(companion, line):
                print("See you soon. ✦")
                return 0
            continue
        if companion.asks_for_selfie(line):
            _make_selfie(companion, LOCAL_CONVERSATION_ID, companion.selfie_scene(line))
            continue
        try:
            result = companion.reply(LOCAL_CONVERSATION_ID, line)
        except ValueError as error:
            print(f"{personality.name} > {error}")
            continue
        print(f"\n{result.personality.name} > {result.text}\n")
        if result.warning:
            print(f"  [Starter note: {result.warning}]\n")
        _save_voice(companion, result.text)


def _telegram(settings: Settings, drop_pending: bool) -> int:
    if not settings.telegram_bot_token:
        print("Telegram is not configured. Add TELEGRAM_BOT_TOKEN to .env, then try again.", file=sys.stderr)
        return 1
    try:
        from .telegram_bot import run_telegram_bot
    except ImportError:
        print("Install the Telegram extra first: pip install -e '.[telegram]'", file=sys.stderr)
        return 1
    companion = Companion(settings)
    run_telegram_bot(companion, drop_pending=drop_pending)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = Settings.from_env()
    if args.command == "init":
        return _init(settings)
    companion = Companion(settings)
    if args.command == "doctor":
        return _doctor(settings, companion)
    if args.command == "profiles":
        return _show_profiles(companion, args.show)
    if args.command == "chat":
        return _chat(settings, args.profile)
    if args.command == "telegram":
        return _telegram(settings, args.drop_pending)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
