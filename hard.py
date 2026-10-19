"""
#[Hard] На основі Telegram Bot API та прикладу 
#(https://gitlab.com/Athamaxy/telegram-bot-tutorial/-/blob/main/TutorialBot.py) 
#створити бота, що підтримує команди menu, whisper, scream
"""

"""
У цьому вирішенні будемо використовувати більш сучасну бібліотеку aiogram,
принципіально алгоритм дій не змінится

"""

import aiogram
import aiohttp
import matplotlib.pyplot as plt
import requests
import asyncio
import logging
import os
import io
from dotenv import load_dotenv
from datetime import datetime, timedelta

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H.%M.%S"
        )


logger = logging.getLogger(__name__)

def plot(data) -> io.BytesIO:
    data_sorted = list(reversed(data))
    dates = [item["exchangedate"] for item in data_sorted]
    rates = [item["rate"] for item in data_sorted]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, rates, marker="o", color="#1f77b4", linewidth=2, label="usd / uah")
    ax.grid(True, linestyle="--", alpha=0.5) 
    ax.legend()
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    fig.savefig("nbu_rates.png")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)

    return buf


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") 

if not BOT_TOKEN:
    logger.error("BOT_TOKEN non existent")

bot = aiogram.Bot(token=BOT_TOKEN)
dp = aiogram.Dispatcher()

async def bot_commands(bot: aiogram.Bot):
    commands = [
            aiogram.types.BotCommand(command="whisper", description="Що напишеш те і виведу маленькими"),
            aiogram.types.BotCommand(command="scream", description="Що напишеш те і виведу ВЕЛИКИМИ"),
            aiogram.types.BotCommand(command="nbu_usd", description="Курс долара НБУ за минулий тиждень")
        ]
    await bot.set_my_commands(commands)


@dp.message(aiogram.filters.CommandStart())
async def handle_start(message: aiogram.types.Message):
    await message.answer("Pick what to do...", reply_markup=reply_kb)


@dp.message(aiogram.filters.Command("scream"))
async def handle_scream(message: aiogram.types.Message, command: iogram.filters.CommandObject):
    if not command.args:
        await message.answer("Введи щось після /scream , типу /scream чудік")
        return
    if command.args == "чудік":
        await message.answer("САМ ЧУДІК!")
        return
    result = command.args.upper()
    await message.answer(result)


@dp.message(aiogram.filters.Command("whisper"))
async def handle_scream(message: aiogram.types.Message, command: iogram.filters.CommandObject):
    if not command.args:
        await message.answer("Введи щось після /whisper , типу /whisper ПРИВІТ")
        return
    result = command.args.lower()
    await message.answer(result)

@dp.message(aiogram.filters.Command("nbu_usd"))
async def handle_scream(message: aiogram.types.Message, command: iogram.filters.CommandObject):
        await message.answer("Дата трансфер від НБУ")
        today = datetime.now()
        month_ag=today-timedelta(days=30)

        params={
            "start": month_ag.strftime("%Y%m%d"),
            "finish": today.strftime("%Y%m%d"),
            "valcode": "usd",
            "sort": "exchangedate",
            "order": "asc",
            "json": ""
        }
        base_url = "https://bank.gov.ua/NBU_Exchange/exchange_site"

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as resp:
                data = await resp.json()
        if not data:
            await message.answer("NBU data transfer failed")
            return

        img_buff = plot(data)

        png = aiogram.types.BufferedInputFile(
                file=img_buff.getvalue(),
                filename="nbu_usd.png"
        )
        await message.answer_photo(photo=png, caption="Курс НБУ за місяць")



        return

async def main():
    logger.info("bot polling....")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot_commands(bot)
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    asyncio.run(main())



