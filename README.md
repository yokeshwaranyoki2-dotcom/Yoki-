# YOKI – Stage 1 (core chat)

Telegram AI friend bot. Stage 1 has: /start, /help, /ping, /clear, Tanglish personality, language mirroring, per-chat memory.

## 1. Get your keys (free)
- **Telegram token:** Telegram -> @BotFather -> `/newbot` -> copy token.
- **Gemini key:** aistudio.google.com -> "Get API key".

## 2. Put the code on GitHub (phone browser)
Create a repo, then "Add file -> Upload files" for each file. Keep the folder structure
(database/, handlers/, services/, utils/). Do NOT upload a real `.env`.
Tip: in GitHub's "Create new file", typing `database/db.py` as the name creates the folder too.

## 3. Run in Termux
```
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
pip install -r requirements.txt
cp .env.example .env
nano .env        # paste your keys, save with CTRL+X, Y, Enter
python main.py
```
When you see "YOKI is starting...", open your bot in Telegram and send /start.
Stop the bot with CTRL+C. Logs are saved in `yoki.log`.

## Common problems
- `Missing in .env`: you forgot to fill TELEGRAM_TOKEN or GEMINI_API_KEY.
- Bot says "en brain hang aayiduchu": check `yoki.log` (wrong key, or model name changed).
  You can change the model in `.env` via GEMINI_MODEL.
- Termux closes when the screen sleeps: run `termux-wake-lock` or pull down the notification and tap "Acquire wakelock".
- Group chats: add the bot, then @mention it or reply to it. In BotFather you may also turn group privacy off.
