from aiogram import Router, F, Dispatcher, Bot, types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from bot_code.database import db
from aiogram.fsm.storage.memory import MemoryStorage
import google.generativeai as genai
import asyncio
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

router = Router(name='base')

max_daily_requests = 5

class LanguageStates(StatesGroup):
    choosing_language = State()

class SpeakingStates(StatesGroup):
    chatting = State()

welcome_text = {
    "uz": "🎉 Assalomu alaykum!",
    "ru": "🎉 Здравствуйте!",
    "en": "🎉 Welcome!"
}

language_button = ["🇺🇿 Uzbek", "🇷🇺 Russian", "🇬🇧 English"]
language_code = {
    "🇺🇿 Uzbek": "uz",
    "🇷🇺 Russian": "ru",
    "🇬🇧 English": "en"
}


question_topic= {
    "uz": "📌 Qaysi mavzu bo‘yicha savolingiz bor?",
    "ru": "📌 По какому предмету у вас есть вопрос?",
    "en": "📌 What topic is your question about?"
}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await db.add_user(
        user_id=message.from_user.id,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        username=message.from_user.username
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=lang)] for lang in language_button],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("🌐 Iltimos, tilni tanlang / Пожалуйста, выберите язык / Please select a language:", reply_markup=keyboard)
    await state.set_state(LanguageStates.choosing_language)


@router.message(LanguageStates.choosing_language, F.text.in_(language_code.keys()))
async def language_chosen(message: Message, state: FSMContext):
    lang_code = language_code[message.text]
    await state.update_data(language=lang_code)

    await db.update_user_language(message.from_user.id, lang_code)

    await message.answer(welcome_text[lang_code], reply_markup=ReplyKeyboardRemove())
    await message.answer(question_topic[lang_code])
    await state.set_state(SpeakingStates.chatting)



@router.message(SpeakingStates.chatting)
async def gemini_chat(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    question = message.text.strip()

    lang_data = await state.get_data()
    lang = lang_data.get("language", "uz")

    today = datetime.now().date()
    request_count = await db.get_user_request_count(user_id, today)

    if request_count >= max_daily_requests:
        msg = {
            "uz": "❌ Kunlik limit tugadi (3 ta so‘rov). Ertaga qayta urinib ko‘ring.",
            "ru": "❌ Дневной лимит исчерпан (3 запроса). Попробуйте завтра.",
            "en": "❌ Daily limit reached (3 requests). Try again tomorrow."
        }
        await message.answer(msg[lang])
        return

    try:
        response = await asyncio.to_thread(model.generate_content, question)
        answer = response.text
    except Exception as e:
        await message.answer("❌ Gemini bilan aloqa uzildi. Keyinroq urinib ko‘ring.")
        return

    await message.answer(answer)

    await db.insert_question(
        user_id=user_id,
        username=username,
        question=question,
        answer=answer,
        lang=lang,
        created_at=datetime.now()
    )


