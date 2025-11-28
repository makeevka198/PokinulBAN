from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
from aiohttp import web

TOKEN = "8581310157:AAE_PWKwEcBbRMFBPggxq-edTE76QAIQs9Y"
CHANNEL_ID = -1002874954438

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я бот для контроля покинувших группу пользователей.")

@dp.message(F.left_chat_member)
async def on_user_left(message: Message):
    user = message.left_chat_member
    try:
        await bot.ban_chat_member(message.chat.id, user.id)
    except Exception as e:
        print("Ошибка бана в группе:", e)

    try:
        await bot.send_message(
            CHANNEL_ID,
            f"Пользователь @{user.username} (ID: {user.id}) покинул группу и был забанен."
        )
    except Exception as e:
        print("Ошибка отправки в канал:", e)

    try:
        await bot.ban_chat_member(CHANNEL_ID, user.id)
    except Exception as e:
        print("Ошибка бана в канале:", e)

async def main():
    app = web.Application()
    dp.workflow_data["bot"] = bot

    # Указываем порт
    PORT = 8080  

    async def handle(request):
        update = await request.json()
        await dp.feed_raw_update(bot, update)
        return web.Response()

    app.router.add_post(f"/{TOKEN}", handle)

    await bot.set_webhook(f"https://your-domain.com/{TOKEN}")

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    print(f"Webhook запущен на порту {PORT}")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
