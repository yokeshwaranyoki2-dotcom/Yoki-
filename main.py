"""YOKI - entry point. Run with:  python main.py"""
import logging
from logging.handlers import RotatingFileHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import config
from database.db import init_db
from handlers import chat, start


def setup_logging() -> None:
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=fmt,
        handlers=[logging.StreamHandler(), RotatingFileHandler("yoki.log", maxBytes=1_000_000, backupCount=2)],
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)  # httpx logs URLs; keep tokens out of logs


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.getLogger("yoki").error("Unhandled error", exc_info=context.error)


async def post_init(app: Application) -> None:
    await init_db()


def main() -> None:
    config.validate()
    setup_logging()
    app = Application.builder().token(config.TELEGRAM_TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("help", start.help_cmd))
    app.add_handler(CommandHandler("ping", start.ping))
    app.add_handler(CommandHandler("clear", chat.clear_memory))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat.handle_text))
    app.add_error_handler(on_error)

    logging.getLogger("yoki").info("YOKI is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
