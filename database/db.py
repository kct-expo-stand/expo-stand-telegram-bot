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

async def check_user_exists(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT COUNT(*) FROM leads WHERE user_id = ?
        """, (user_id,))
        result = await cursor.fetchone()
        return result[0] > 0

async def add_lead(user_id, username, first_name, phone, program):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO leads (user_id, username, first_name, phone, program)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, first_name, phone, program))
        await db.commit()
