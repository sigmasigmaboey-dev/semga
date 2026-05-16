import os
import asyncio
import threading
import requests
from aiohttp import web
from aiogram import Bot, Dispatcher, types

# === ENVIRONMENT VARIABLES ===
TOKEN = os.getenv("TOKEN")
AI_KEY = os.getenv("AI_KEY")
PORT = int(os.getenv("PORT", "8080"))

bot = Bot(token=TOKEN)
dp = Dispatcher()


# === VENICE AI REQUEST ===
async def ask_venice(prompt: str) -> str:
    url = "https://api.venice.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "veniceai/Venice-1.1",
        "messages": [
            {"role": "system", "content": "Ты злой, мемный ИИ по имени Semga."},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, json=data, headers=headers)
    return r.json()["choices"][0]["message"]["content"]


# === TELEGRAM HANDLER ===
@dp.message()
async def semga_handler(msg: types.Message):
    text = msg.text.lower()

    if not text.startswith("semga:"):
        return

    prompt = text.replace("semga:", "").strip()
    reply = await ask_venice(prompt)
    await msg.answer(reply)


# === START TELEGRAM BOT ===
async def start_bot():
    await dp.start_polling(bot)


# === FAKE WEB SERVER FOR RENDER ===
async def handle(request):
    return web.Response(text="Bot is running on Render!")


def start_web():
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=PORT)


# === MAIN ENTRY ===
if __name__ == "__main__":
    # Run bot in separate thread
    threading.Thread(target=lambda: asyncio.run(start_bot())).start()

    # Run web server (Render requires this)
    start_web()
