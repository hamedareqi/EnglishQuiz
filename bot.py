from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import json

# ضع توكن البوت هنا
API_TOKEN = "7579896789:AAFwpBpJa0NPV-STxyV5d3JOSqvryJlAupY"
# ضع الآي دي الخاص بك لتصلك الرسائل
ADMIN_ID = 7799197049

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# معالج الرسائل القادمة من WebApp
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

        # إرسال الرسالة إليك
        await bot.send_message(ADMIN_ID, text)
        # رد للمستخدم أن الرسالة وصلت
        await message.answer("✅ تم استلام رسالتك، شكراً لك!")

    except Exception as e:
        await message.answer(f"❌ حدث خطأ: {str(e)}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
