from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import json
import logging

# تفعيل اللوق للمتابعة
logging.basicConfig(level=logging.INFO)

# توكن البوت
API_TOKEN = "7579896789:AAFwpBpJa0NPV-STxyV5d3JOSqvryJlAupY"

# الآي دي الخاص بك كأدمن
ADMIN_ID = 7799197049

# تهيئة البوت والديسباتشر
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# إنشاء زر WebApp لفتح الصفحة داخل Telegram
def webapp_button():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "📩 أرسل رسالة",
            web_app=WebAppInfo(url="https://your-username.github.io/index.html")  # ضع رابط صفحة WebApp هنا
        )
    )
    return kb

# عند إرسال /start يظهر زر WebApp
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "مرحبًا! اضغط على الزر لإرسال رسالة للإدارة:",
        reply_markup=webapp_button()
    )

# استقبال البيانات من WebApp
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

        # إرسال الرسالة إليك مباشرة
        await bot.send_message(ADMIN_ID, text)

    except Exception as e:
        print("Error:", e)

# تشغيل البوت
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
