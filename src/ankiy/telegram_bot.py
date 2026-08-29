"""Optional private Telegram bridge for Ankiy.

It deliberately supports polling first: that is the quickest way to run a personal bot
from a laptop or home server without exposing a webhook endpoint.
"""

from __future__ import annotations

import asyncio
import io
import logging

from .companion import Companion
from .images import ImageError, OpenAICompatibleImages
from .voice import ElevenLabsVoice, VoiceError

logger = logging.getLogger(__name__)
TELEGRAM_TEXT_LIMIT = 4096


def _image_service(companion: Companion) -> OpenAICompatibleImages | None:
    settings = companion.settings
    if not settings.images_enabled or not settings.image_api_key:
        return None
    return OpenAICompatibleImages(
        api_key=settings.image_api_key,
        base_url=settings.image_base_url,
        model=settings.image_model,
        size=settings.image_size,
        media_dir=settings.media_dir,
    )


def _voice_service(companion: Companion) -> ElevenLabsVoice | None:
    settings = companion.settings
    if not settings.voice_enabled or not settings.elevenlabs_api_key or not settings.elevenlabs_voice_id:
        return None
    return ElevenLabsVoice(
        api_key=settings.elevenlabs_api_key,
        voice_id=settings.elevenlabs_voice_id,
        model_id=settings.elevenlabs_model,
    )


def _chunks(text: str, limit: int = TELEGRAM_TEXT_LIMIT) -> list[str]:
    """Split replies on a friendly word boundary for Telegram's message limit."""
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    remainder = text
    while len(remainder) > limit:
        split_at = remainder.rfind(" ", 0, limit)
        if split_at < limit // 2:
            split_at = limit
        parts.append(remainder[:split_at].strip())
        remainder = remainder[split_at:].strip()
    if remainder:
        parts.append(remainder)
    return parts


def run_telegram_bot(companion: Companion, *, drop_pending: bool = False) -> None:
    """Run Ankiy until Ctrl+C. Requires the optional python-telegram-bot extra."""
    from telegram import BotCommand, Update
    from telegram.constants import ChatAction, ChatType
    from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

    async def is_allowed(update: Update) -> bool:
        message = update.effective_message
        user = update.effective_user
        chat = update.effective_chat
        if not message or not user or not chat:
            return False
        if chat.type != ChatType.PRIVATE:
            return False
        allowed_ids = companion.settings.telegram_allowed_user_ids
        if not allowed_ids:
            await message.reply_text(
                "This Ankiy bot is locked until its owner sets TELEGRAM_ALLOWED_USER_IDS.\n"
                f"Your numeric Telegram ID is: {user.id}\n\n"
                "Ask the owner to add it to .env, then restart the bot."
            )
            return False
        if user.id not in allowed_ids:
            await message.reply_text("This is a private companion bot. Sorry, this chat is not authorized.")
            return False
        return True

    def conversation_id(update: Update) -> str:
        assert update.effective_user is not None
        return f"telegram:{update.effective_user.id}"

    async def send_text(message, text: str) -> None:
        for chunk in _chunks(text):
            await message.reply_text(chunk)

    async def maybe_send_voice(message, cid: str, text: str) -> None:
        if not companion.voice_is_on(cid):
            return
        service = _voice_service(companion)
        if not service:
            await message.reply_text("Voice is toggled on, but ElevenLabs is not configured by the owner yet.")
            return
        try:
            audio = await asyncio.to_thread(service.synthesize, text)
        except VoiceError as error:
            logger.warning("Voice generation failed: %s", error)
            await message.reply_text("I couldn’t make the voice note this time. The text reply is still here.")
            return
        stream = io.BytesIO(audio)
        stream.name = "ankiy-reply.mp3"
        await message.reply_voice(voice=stream, caption="A little voice note from your companion ✦")

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        cid = conversation_id(update)
        profile = companion.profile_for(cid)
        await update.effective_message.reply_text(
            f"{companion.greeting(cid)}\n\n"
            f"You’re chatting with {profile.name}. I keep this bot private and store its "
            "conversation data locally on the machine running it. Use /clear anytime.\n\n"
            "Try /profiles, /profile luna, /voice on, or /selfie at a rainy café."
        )

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        await update.effective_message.reply_text(
            "/profiles — see personalities\n"
            "/profile <name> — switch personality (fresh context)\n"
            "/clear — erase this chat’s saved context\n"
            "/voice on or /voice off — toggle optional ElevenLabs audio\n"
            "/selfie [scene] — create a fictional companion avatar\n"
            "/whoami — show your Telegram ID for the bot allow-list"
        )

    async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        chat = update.effective_chat
        # `/whoami` must work while the bot is locked, but never responds in groups.
        if message and user and chat and chat.type == ChatType.PRIVATE:
            await message.reply_text(f"Your numeric Telegram ID is: {user.id}")

    async def profiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        cid = conversation_id(update)
        active = companion.profile_for(cid).key
        options = companion.available_profiles()
        labels = [f"• {name}{' (active)' if name == active else ''}" for name in options]
        await update.effective_message.reply_text(
            "Choose a mood:\n" + "\n".join(labels) + "\n\nUse /profile <name> to switch."
        )

    async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        if not context.args:
            await update.effective_message.reply_text("Try /profile luna — or send /profiles first.")
            return
        key = context.args[0].lower()
        try:
            person = companion.switch_profile(conversation_id(update), key)
        except (FileNotFoundError, ValueError) as error:
            await update.effective_message.reply_text(f"I couldn’t find that profile. {error}")
            return
        await update.effective_message.reply_text(
            f"New page, new vibe: {person.name}.\n\n{companion.greeting(conversation_id(update))}"
        )

    async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        companion.clear(conversation_id(update))
        await update.effective_message.reply_text("Fresh page. I cleared this saved conversation context. ✦")

    async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        if not context.args or context.args[0].lower() not in {"on", "off"}:
            state = "on" if companion.voice_is_on(conversation_id(update)) else "off"
            await update.effective_message.reply_text(f"Voice is {state}. Use /voice on or /voice off.")
            return
        enabled = context.args[0].lower() == "on"
        companion.set_voice(conversation_id(update), enabled)
        reply = f"Voice turned {'on' if enabled else 'off'} for this chat."
        if enabled and not companion.settings.voice_enabled:
            reply += " Add ElevenLabs credentials to .env before it can send audio."
        await update.effective_message.reply_text(reply)

    async def make_selfie(update: Update, context: ContextTypes.DEFAULT_TYPE, scene: str | None = None) -> None:
        if not await is_allowed(update):
            return
        assert update.effective_message is not None
        service = _image_service(companion)
        if not service:
            await update.effective_message.reply_text(
                "Selfies aren’t configured yet. The owner can add IMAGE_API_KEY to .env, "
                "then restart me."
            )
            return
        cid = conversation_id(update)
        person = companion.profile_for(cid)
        requested_scene = scene or " ".join(context.args) or "a cozy everyday moment"
        await update.effective_chat.send_action(ChatAction.UPLOAD_PHOTO)
        try:
            result = await asyncio.to_thread(
                service.generate_selfie, person.selfie_prompt(requested_scene)
            )
        except ImageError as error:
            logger.warning("Image generation failed: %s", error)
            await update.effective_message.reply_text("That selfie didn’t develop this time. Want to try another scene?")
            return
        with result.path.open("rb") as image_file:
            await update.effective_message.reply_photo(
                photo=image_file,
                caption=f"A fictional {person.name} avatar — {requested_scene} ✦",
            )

    async def selfie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await make_selfie(update, context)

    async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_allowed(update):
            return
        incoming = update.effective_message
        if not incoming or not incoming.text:
            return
        if companion.asks_for_selfie(incoming.text):
            await make_selfie(update, context, companion.selfie_scene(incoming.text))
            return
        cid = conversation_id(update)
        await update.effective_chat.send_action(ChatAction.TYPING)
        try:
            result = await asyncio.to_thread(companion.reply, cid, incoming.text)
        except ValueError as error:
            await incoming.reply_text(str(error))
            return
        await send_text(incoming, result.text)
        await maybe_send_voice(incoming, cid, result.text)

    async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.exception("Telegram update failed", exc_info=context.error)

    async def post_init(application: Application) -> None:
        await application.bot.set_my_commands(
            [
                BotCommand("start", "meet your companion"),
                BotCommand("profiles", "list personalities"),
                BotCommand("profile", "switch personality"),
                BotCommand("clear", "clear saved chat context"),
                BotCommand("voice", "toggle voice notes"),
                BotCommand("selfie", "create a fictional avatar"),
                BotCommand("whoami", "show your Telegram ID"),
            ]
        )

    application = ApplicationBuilder().token(companion.settings.telegram_bot_token).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("whoami", whoami))
    application.add_handler(CommandHandler("profiles", profiles))
    application.add_handler(CommandHandler("profile", profile))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(CommandHandler("voice", voice))
    application.add_handler(CommandHandler("selfie", selfie))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    application.add_error_handler(on_error)

    if not companion.settings.telegram_allowed_user_ids:
        print("Telegram bot started in LOCKED mode. Send /whoami to it, add that ID to .env, then restart.")
    else:
        print("Telegram companion is polling privately. Press Ctrl+C to stop.")
    application.run_polling(drop_pending_updates=drop_pending, allowed_updates=Update.ALL_TYPES)
