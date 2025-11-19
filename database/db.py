import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                phone TEXT,
                program TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def add_lead(user_id, username, first_name, phone, program):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO leads (user_id, username, first_name, phone, program)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, first_name, phone, program))
        await db.commit()
