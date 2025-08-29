import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from datetime import datetime, timedelta

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

subscriptions = {}
admin_id = 8452935714

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if user_id not in subscriptions or subscriptions[user_id] < datetime.now():
        await message.answer("❌ Sizda obuna yo'q yoki muddati tugagan. Iltimos, obuna sotib oling.")
    else:
        await message.answer("""✅ Xush kelibsiz! Bot menyusi:

📊 /expenses - Harajatlarni kiritish
🗓 /plans - Rejalarni kiritish
⏰ /reminders - Eslatmalar qo'shish""")

@dp.message_handler(commands=["addsub"])
async def add_subscription(message: types.Message):
    if message.from_user.id != admin_id:
        await message.answer("❌ Sizda ruxsat yo'q.")
        return

    try:
        _, user_id, days = message.text.split()
        user_id = int(user_id)
        days = int(days)
        subscriptions[user_id] = datetime.now() + timedelta(days=days)
        await message.answer(f"✅ Foydalanuvchi {user_id} uchun {days} kunlik obuna qo'shildi.")
        await bot.send_message(user_id, f"🎉 Sizga {days} kunlik obuna berildi!")
    except Exception:
        await message.answer("❌ Xato format. Foydalanish: /addsub USER_ID KUN")

@dp.message_handler(commands=["expenses"])
async def expenses(message: types.Message):
    user_id = message.from_user.id
    if user_id not in subscriptions or subscriptions[user_id] < datetime.now():
        await message.answer("❌ Obunangiz muddati tugagan.")
        return
    await message.answer("💰 Harajatlaringizni shu yerga yozing:")

@dp.message_handler(commands=["plans"])
async def plans(message: types.Message):
    user_id = message.from_user.id
    if user_id not in subscriptions or subscriptions[user_id] < datetime.now():
        await message.answer("❌ Obunangiz muddati tugagan.")
        return
    await message.answer("📝 Kelajakdagi rejalarni kiriting:")

@dp.message_handler(commands=["reminders"])
async def reminders(message: types.Message):
    user_id = message.from_user.id
    if user_id not in subscriptions or subscriptions[user_id] < datetime.now():
        await message.answer("❌ Obunangiz muddati tugagan.")
        return
    await message.answer("⏰ Qaysi vaqtga eslatma qo'shmoqchisiz?")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
