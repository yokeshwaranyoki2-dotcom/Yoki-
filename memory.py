"""Per-chat conversation memory. Private chat id == user id; each group has its own."""
import aiosqlite
import config


async def add_message(chat_id: int, user_id: int | None, role: str, content: str) -> None:
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT INTO conversations (chat_id, user_id, role, content) VALUES (?, ?, ?, ?)",
            (chat_id, user_id, role, content),
        )
        # Keep only the newest MEMORY_LIMIT messages for this chat
        await db.execute(
            """DELETE FROM conversations WHERE chat_id = ? AND id NOT IN (
                 SELECT id FROM conversations WHERE chat_id = ? ORDER BY id DESC LIMIT ?)""",
            (chat_id, chat_id, config.MEMORY_LIMIT),
        )
        await db.commit()


async def get_history(chat_id: int) -> list[tuple[str, str]]:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute(
            "SELECT role, content FROM conversations WHERE chat_id = ? ORDER BY id DESC LIMIT ?",
            (chat_id, config.MEMORY_LIMIT),
        )
        rows = await cur.fetchall()
    rows.reverse()
    while rows and rows[0][0] != "user":  # Gemini wants history to start with a user turn
        rows.pop(0)
    return [(r, c) for r, c in rows]


async def clear(chat_id: int) -> int:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("DELETE FROM conversations WHERE chat_id = ?", (chat_id,))
        await db.commit()
        return cur.rowcount
