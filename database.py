import aiosqlite

DB = "data.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            username TEXT,
            silver INTEGER DEFAULT 0
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS promo(
            code TEXT PRIMARY KEY,
            reward INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            text TEXT,
            status TEXT DEFAULT 'new'
        )
        """)

        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users(id, username) VALUES(?,?)",
            (user_id, username)
        )
        await db.commit()


async def add_silver(user_id, amount):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE users SET silver=silver+? WHERE id=?",
            (amount, user_id)
        )
        await db.commit()


async def get_silver(user_id):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT silver FROM users WHERE id=?",
            (user_id,)
        )
        result = await cur.fetchone()
        return result[0] if result else 0
