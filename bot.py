import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types

TOKEN = os.getenv("BOT_TOKEN")
AI_KEY = os.getenv("AI_KEY")

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message()
async def semga_handler(msg: types.Message):
    text = msg.text.lower()

    if not text.startswith("semga"):
        return

    prompt = msg.text[len("semga"):].strip()
    if prompt == "":
        prompt = "поприветствуй пользователя"

    answer = await asyncio.to_thread(ask_venice, prompt)
    await msg.reply(answer)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
