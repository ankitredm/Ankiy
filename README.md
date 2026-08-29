# Ankiy ✦

**A warm, playful, local-first AI companion you can make your own.**

Ankiy starts in your terminal with a local model, keeps each conversation in a small local SQLite database, and has optional bridges for Telegram, ElevenLabs voice notes, and fictional companion selfies. Personalities are just YAML files, so changing a companion should feel more like editing a character sheet than rebuilding an app.

> **Private by default:** chat runs against a local Ollama endpoint by default. Telegram, voice, and image generation are opt-in integrations. `.env`, private chats, and generated media are ignored by git.

---

## A five-minute first chat

**Prerequisite:** Python 3.11+ and [Ollama](https://ollama.com) installed on the machine.

```bash
# 1) Create an isolated Python environment and install Ankiy
python -m venv .venv
source .venv/bin/activate              # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[telegram,dev]"

# 2) Create your private config and local folders
ankiy init

# 3) Download one small local model (no API key needed)
ollama pull llama3.2

# 4) Check the setup, then meet Luna
ankiy doctor
ankiy chat
```

On Windows Command Prompt, activate with `.venv\Scripts\activate.bat`. If `ankiy` is not found, use `python -m ankiy.cli chat` from the project folder.

The first prompt supports these friendly controls:

```text
/profiles                 # see available personalities
/profile atlas            # switch companion (fresh conversation context)
/voice on                 # enable optional voice notes for this conversation
/selfie reading in a café # make an optional fictional avatar image
/clear                    # erase this conversation's saved context
/help                     # everything else
/quit
```

You can also naturally ask, for example: **“Send me a selfie at a rainy café.”** Ankiy only creates an image for explicit selfie requests, so a casual mention will not trigger an image charge.

---

## What you get

| Piece | What it does | Default |
| --- | --- | --- |
| **Companion chat** | Uses the OpenAI-compatible chat protocol; defaults to your local Ollama server. | On, local |
| **Personality profiles** | Defines voice, interests, boundaries, greeting, and image identity in `profiles/*.yaml`. | Luna, Atlas, Pip |
| **Private memory** | Stores recent conversation turns per channel/user in `data/ankiy.sqlite3`. `/clear` erases a conversation context. | On, local |
| **Telegram bridge** | Polls Telegram so you can carry the same companion in your phone. | Optional, private allow-list |
| **ElevenLabs voice** | Turns replies into an MP3 voice note after `/voice on`. | Optional |
| **Fictional selfies** | Generates a clearly fictional avatar image matching the current companion profile. | Optional |

If Ollama is offline, Ankiy responds with a clearly labelled starter-mode message instead of silently pretending an AI answer was generated. Run `ankiy doctor` to diagnose it.

---

## Make a personality yours

Profiles are intentionally plain YAML. Copy a starter and edit it:

```bash
cp profiles/luna.yaml profiles/mira.yaml
```

Then change `profiles/mira.yaml`:

```yaml
name: Mira
tagline: The gentle co-conspirator
description: A bright, cozy companion who loves small creative experiments.
traits: [warm, curious, playfully practical]
speaking_style:
  - Be vivid but never overwhelming.
  - Ask one thoughtful follow-up question when it fits.
interests: [sketchbooks, museum cafés, strange little facts]
boundaries:
  - Keep the relationship supportive and non-exclusive.
  - Never pressure the user for personal information or money.
visual_style: An original illustrated avatar with a copper bob, soft blue overalls, and a warm watercolor-and-ink aesthetic.
first_message: Hey, {owner_name}! What shall we make a little brighter today?
```

Select it with `/profile mira` in chat or Telegram. You can make it the default by setting `DEFAULT_PROFILE=mira` in `.env`.

**A note on character design:** use original visual descriptions for `visual_style`. Ankiy’s selfie prompt explicitly requests a fictional avatar and rejects real people, celebrities, logos, and watermarks. Do not use it to impersonate someone.

---

## Configure optional integrations

`ankiy init` creates `.env` from `.env.example`. Add only the pieces you want, then restart Ankiy. Never commit `.env`.

### 1. Change the owner name or chat model

```dotenv
OWNER_NAME=Sam
DEFAULT_PROFILE=luna

# Default local Ollama endpoint
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=llama3.2
```

Any OpenAI-compatible chat server can replace Ollama:

```dotenv
LLM_BASE_URL=https://your-compatible-provider.example/v1
LLM_MODEL=your-chat-model
LLM_API_KEY=your_provider_key
```

Ankiy uses `POST /chat/completions`, so it remains deliberately provider-lightweight. Keep image credentials separate from chat credentials to preserve a local-first chat setup.

### 2. Telegram — private companion on your phone

Install with the Telegram extra (included in the quick start):

```bash
pip install -e ".[telegram]"
```

1. In Telegram, open **@BotFather**, run `/newbot`, and copy the token it gives you.
2. Put it in `.env`:

   ```dotenv
   TELEGRAM_BOT_TOKEN=123456:replace-with-your-bot-token
   ```

3. Run `ankiy telegram`. It starts **locked** if you have no allow-list.
4. Open your new bot, send `/whoami`, and it will show your numeric Telegram user ID.
5. Stop the process, set that ID, and restart:

   ```dotenv
   TELEGRAM_ALLOWED_USER_IDS=123456789
   ```

```bash
ankiy telegram
```

The bot accepts only private chats and only those numeric IDs. A comma-separated allow-list supports a small trusted household:

```dotenv
TELEGRAM_ALLOWED_USER_IDS=123456789,987654321
```

It uses long polling — no public webhook, domain, or tunnel needed. Use `ankiy telegram --drop-pending` if you do not want it to process messages received while the bot was off. The implementation follows the current [`ApplicationBuilder` / `run_polling()` flow in python-telegram-bot](https://docs.python-telegram-bot.org/en/stable/telegram.ext.applicationbuilder.html).

### 3. ElevenLabs custom voice

1. In ElevenLabs, choose a voice or create a voice you are authorized to use, then copy its **Voice ID** from Voice Lab.
2. Create an API key in ElevenLabs and add both values:

   ```dotenv
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=your_voice_id
   # Optional: eleven_flash_v2_5 for lower latency, if your account supports it
   ELEVENLABS_MODEL=eleven_multilingual_v2
   ```

3. In Ankiy, send `/voice on`. The setting is remembered separately for each chat. Telegram receives a voice note; terminal chat saves `media/latest-reply.mp3`.

Ankiy calls ElevenLabs’ documented [Text-to-Speech convert endpoint](https://elevenlabs.io/docs/api-reference/text-to-speech/convert) directly, so there is no extra SDK to configure. Only clone a voice with that person’s clear permission.

### 4. Fictional companion selfies

Ankiy supports the OpenAI-compatible `POST /images/generations` pattern and asks for base64 image data (with URL response fallback). For the default OpenAI endpoint, set:

```dotenv
IMAGE_API_KEY=your_image_provider_key
IMAGE_BASE_URL=https://api.openai.com/v1
IMAGE_MODEL=gpt-image-2
IMAGE_SIZE=1024x1024
```

Then use `/selfie at a rainy café`, or ask naturally for one. Images are saved locally under `media/` and sent back in Telegram. This feature is intentionally separate from the chat model: **local chat remains key-free**, while image generation is an explicit cloud feature. See the current [OpenAI Image Generation guide](https://developers.openai.com/api/docs/guides/image-generation) for image-model access and pricing details; if your provider offers a different compatible image model, set `IMAGE_MODEL` accordingly.

---

## Day-to-day commands

```bash
ankiy chat --profile pip  # start terminal chat as a particular personality
ankiy profiles            # list profiles and their taglines
ankiy profiles --show luna
ankiy doctor              # validate profile/configuration and reachability
ankiy telegram            # start the optional Telegram bot
```

### Data and reset controls

| Location | Contains | Safe to delete? |
| --- | --- | --- |
| `.env` | Your local configuration and API keys | Only if you want to reconfigure |
| `data/ankiy.sqlite3` | Local chat context and per-chat voice toggle | Yes — resets all Ankiy conversations |
| `media/` | Generated optional selfies and terminal voice files | Yes — removes generated media |
| `profiles/` | Your personality definitions | Back these up if you customize them |

`/clear` clears the active conversation’s stored messages. Switching a profile starts that profile with a fresh chat context, which avoids one companion speaking in another companion’s voice.

---

## Project layout

```text
profiles/                 # editable companion character sheets
src/ankiy/
  cli.py                  # terminal onboarding and chat
  companion.py            # personality + memory + model orchestration
  memory.py               # local SQLite store
  telegram_bot.py         # optional private polling bridge
  voice.py                # optional ElevenLabs REST connector
  images.py               # optional compatible Images API connector
.env.example              # documented configuration template
```

### Development

```bash
pip install -e ".[telegram,dev]"
pytest
```

The integration modules use simple HTTP adapters and are deliberately small: swap providers by changing config or add a connector without changing personality or memory code.

### Troubleshooting

- **“Chat endpoint not reachable”** — run `ollama serve` if Ollama is not already running, then `ollama pull llama3.2`. Check with `ankiy doctor`.
- **Profile missing** — run `ankiy profiles`; profile filenames must end in `.yaml`, and `DEFAULT_PROFILE` must match the filename without `.yaml`.
- **Telegram remains locked** — start it once, DM `/whoami` to the bot, put that number in `TELEGRAM_ALLOWED_USER_IDS`, then restart it.
- **Voice toggle does nothing** — `/voice on` remembers the preference, but needs both ElevenLabs values and a restarted process.
- **Selfie fails** — use `ankiy doctor` to verify `IMAGE_API_KEY`, confirm image-model access with your provider, and try a shorter scene description.

---

Built to be a starter, not a cage: begin with one local conversation, then give your companion new personalities, prompts, tools, and rituals as you go.
