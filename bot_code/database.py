import asyncpg
import logging
import asyncio
from typing import Optional
import os
import aiohttp
from datetime import datetime, timezone
from datetime import date


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._pool = None  # Pool bo‘yicha bitta instansiya
            cls._instance._is_connected = False
        return cls._instance


    async def connect(self, user, password, db, host, port):
        """PostgreSQL bilan ulanishni o‘rnatish"""
        self._pool = await asyncpg.create_pool(
            user=user,
            password=password,
            database=db,
            host=host,
            port=port
        )

    async def is_connected(self) -> bool:
        if self._pool is None:
            return False
        try:
            async with self._pool.acquire() as connection:
                await connection.fetch("SELECT 1")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    async def fetch(self, query, *args):
        async with self._pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute(self, query, *args):
        """SQL so'rovini bajarish (ma'lumot o'zgartirish)"""
        async with self._pool.acquire() as connection:
            return await connection.execute(query, *args)



    async def add_user(self, user_id: int, first_name: str, last_name: str, username: Optional[str] = None):
        """Bazaga yangi user qo‘shish yoki yangilash"""
        created_at = datetime.utcnow()

        async with self._pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO apps_user (user_id, first_name, last_name, username, created_at)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (user_id) DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    username = EXCLUDED.username
            """, user_id, first_name, last_name, username, created_at)


    async def update_user_language(self, user_id: int, language: str):
        await self.execute("""
            UPDATE apps_user SET language = $1 WHERE user_id = $2
        """, language, user_id)

    async def insert_question(self, user_id, username, question, answer, lang, created_at):
        await self._pool.execute('''
            INSERT INTO apps_question (user_id, username, question, answer, language, created_at)
            VALUES ($1, $2, $3, $4, $5, $6)
        ''', user_id, username, question, answer, lang, created_at)


    async def count_today_questions(self, user_id, today: date) -> int:
        return await self._pool.fetchval('''
            SELECT COUNT(*) FROM apps_question
            WHERE user_id = $1 AND created_at::date = $2
        ''', user_id, today)

    async def get_user_request_count(self, user_id: int, today: date) -> int:
        return await self._pool.fetchval('''
            SELECT COUNT(*) FROM apps_question
            WHERE user_id = $1 AND created_at::date = $2
        ''', user_id, today)

    async def get_user_questions(self, user_id):
        return await self._pool.fetch('''
            SELECT question, answer, created_at FROM apps_question
            WHERE user_id = $1 ORDER BY created_at DESC
        ''', user_id)



DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1@localhost:5432/chat_bot")
db = Database()