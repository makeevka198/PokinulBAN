from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus
import asyncio

TOKEN = "8581310157:AAE_PWKwEcBbRMFBPggxq-edTE76QAIQs9Y"
CHANNEL_ID = -1002874954438  # ID канала, куда будут попадать нарушители

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.left_chat_member)
async def on_user_left(message: Message):
    user = message.left_chat_member

    # 1. Баним в группе
    try:
        await bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=user.id
        )
        print(f"User {user.id} was banned in group")
    except Exception as e:
        print("Ban error:", e)

    # 2. Отправляем в канал уведомление
    try:
        await bot.send_message(
            CHANNEL_ID,
            f"Пользователь @{user.username} (ID: {user.id}) покинул группу и был забанен."
        )
    except Exception as e:
        print("Channel post error:", e)

    # 3. Блокируем в канале (опционально)
    try:
        await bot.ban_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user.id
        )
        print(f"User {user.id} blocked in channel")
    except Exception as e:
        print("Channel ban error:", e)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
