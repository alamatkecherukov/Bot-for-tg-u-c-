import aiosqlite

DB_NAME = "bot_database.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                teacher_msg_id INTEGER PRIMARY KEY,
                student_id INTEGER
            )
        """)
        await db.commit()

async def save_message(teacher_msg_id: int, student_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO messages (teacher_msg_id, student_id) VALUES (?, ?)",
            (teacher_msg_id, student_id)
        )
        await db.commit()

async def get_student_id(teacher_msg_id: int) -> int | None:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT student_id FROM messages WHERE teacher_msg_id = ?",
            (teacher_msg_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None
