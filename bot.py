from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

import json

API_TOKEN = "7579896789:AAFwpBpJa0NPV-STxyV5d3JOSqvryJlAupY"
ADMIN_ID = 7799197049

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# هذا هو زر WebApp
kb = InlineKeyboardMarkup()
kb.add(
    InlineKeyboardButton(
        "📩 أرسل رسالة", 
        web_app=WebAppInfo(url="https://your-username.github.io/index.html")  # ضع رابط GitHub Pages
    )
)

# عندما يرسل المستخدم /start أو أي رسالة
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "مرحبًا! اضغط على الزر لإرسال رسالة للإدارة:", 
        reply_markup=kb
    )

# معالج البيانات القادمة من WebApp
@dp.message_handler(content_types=types.ContentTypes.WEB_APP_DATA)
async def webapp_handler(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        user = data.get("user", {})

        full_name = f"{user.get('first_name','')} {user.get('last_name','')}".strip()
        username = user.get("username") or "لا يوجد"

        text = (
            f"📩 رسالة جديدة من WebApp\n\n"
            f"👤 المستخدم: {full_name} (@{username})\n"
            f"🆔 ID: {user.get('id','؟')}\n\n"
            f"✉️ الرسالة:\n{data.get('message','')}"
        )

        await bot.send_message(ADMIN_ID, text)
        await message.answer("✅ تم استلام رسالتك، شكراً لك!")

    except Exception as e:
        await message.answer(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
