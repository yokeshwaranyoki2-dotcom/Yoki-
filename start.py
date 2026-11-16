"""/start, /help, /ping"""
import time
from telegram import Update
from telegram.ext import ContextTypes
from database.db import upsert_user

WELCOME = (
    "Vanakkam {name}! 👋 Naan YOKI — Chennai-la irukkura un friend (bot thaan, aana vibe real 😎).\n\n"
    "Anime, movies, memes, life — enna venaalum pesalam. Tamil, English, Tanglish, Hindi... "
    "nee ethula pesinaalum naan purinjikkuven.\n\n"
    "/help paaru commands-kku. Sari, first-la unna pathi sollu!"
)

HELP = (
    "YOKI commands:\n"
    "/start - Welcome\n"
    "/help - Intha list\n"
    "/ping - Bot irukka nu check\n"
    "/clear - Nan unkitta pesunathu ellam maranthuduven\n\n"
    "Groups-la: @mention pannu illa en message-ku reply pannu.\n"
    "More commands (games, gems, trivia) next stages-la varum 🎮"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await upsert_user(user.id, user.username, user.first_name)
    await update.message.reply_text(WELCOME.format(name=user.first_name or "machi"))


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_t = time.perf_counter()
    msg = await update.message.reply_text("Pong! 🏓")
    ms = int((time.perf_counter() - start_t) * 1000)
    await msg.edit_text(f"Pong! 🏓 {ms} ms")
