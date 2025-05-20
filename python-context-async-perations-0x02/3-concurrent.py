#!/usr/bin/python3

import asyncio
import aiosqlite

async def get_db_connection():
    return await aiosqlite.connect("users.db")

async def async_fetch_users():
    db = await get_db_connection()
    async with db:
        print("Fetching all users...")
        await db.execute("SELECT * FROM users") 
        await asyncio.sleep(1) 
        print("Fetched all users")
        return "All users fetched"

async def async_fetch_older_users():
    db = await get_db_connection()
    async with db:
        print("Fetching users older than 40...")
        await db.execute("SELECT * FROM users WHERE age > 40") # Placeholder query
        await asyncio.sleep(1.5) 
        print("Fetched users older than 40")
        return "Older users fetched"

async def fetch_concurrently():
    results = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("\nResults Summary:")
    print(results)

asyncio.run(fetch_concurrently())