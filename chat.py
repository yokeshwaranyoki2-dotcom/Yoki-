"""Normal text chat + /clear."""
import logging
import time
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
import config
from database.db import upsert_user
from services import ai, memory

log = logging.getLogger(__name__)
_last_msg: dict[int, float] = {}  # user_id -> time of last accepted message


def _is_group(update: Update) -> bool:
    return update.effective_chat.type in ("group", "supergroup")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message
    if not msg or not msg.text:
        return
    user = update.effective_user
    chat_id = update.effective_chat.id
    text = msg.text.strip()

    # In groups only answer when mentioned or replied to
    if _is_group(update):
        bot_name = (context.bot.username or "").lower()
        mentioned = bool(bot_name) and f"@{bot_name}" in text.lower()
        replied = bool(
            msg.reply_to_message
            and msg.reply_to_message.from_user
            and msg.reply_to_message.from_user.id == context.bot.id
        )
        if not (mentioned or replied):
            return
        if mentioned:
            text = text.replace(f"@{context.bot.username}", "").strip() or "hi"
        text = f"[{user.first_name or 'User'}]: {text}"  # so YOKI knows who is talking in a group

    # Rate limit
    now = time.monotonic()
    if now - _last_msg.get(user.id, 0) < config.COOLDOWN_SECONDS:
        return
    _last_msg[user.id] = now

    if len(text) > config.MAX_INPUT_CHARS:
        await msg.reply_text("Machi, romba perusa irukku 😅 Konjam short-ah sollu!")
        return

    await upsert_user(user.id, user.username, user.first_name)
    await context.bot.send_chat_action(chat_id, ChatAction.TYPING)

    history = await memory.get_history(chat_id)
    reply = await ai.generate_reply(history, text)

    await memory.add_message(chat_id, user.id, "user", text)
    await memory.add_message(chat_id, None, "model", reply)

    for i in range(0, len(reply), 4000):  # Telegram limit is 4096 chars
        await msg.reply_text(reply[i : i + 4000])


async def clear_memory(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _is_group(update):
        member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if member.status not in ("administrator", "creator"):
            await update.message.reply_text("Group memory-a admins mattum thaan clear panna mudiyum 🙅")
            return
    await memory.clear(update.effective_chat.id)
    await update.message.reply_text("Done! Ellathaiyum maranthuten 🧹 Fresh start!")
