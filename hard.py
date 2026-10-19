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
import asyncio
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H.%M.%S"
        )


logger = logging.getLogger(__name__)

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



""""
reply_kb = aiogram.types.ReplyKeyboardMarkup(
        keyboard=[
            [aiogram.types.KeyboardButton(text="/scream")],
            [aiogram.types.KeyboardButton(text="/whisper")]
        ],
        resize_keyboard = True,
        one_time_keyboard = True
        )
"""


@dp.message(aiogram.filters.CommandStart())
async def handle_start(message: aiogram.types.Message):
    await message.answer("Pick what to do...", reply_markup=reply_kb)


async def main():
    logger.info("bot polling....")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot_commands(bot)
    await dp.start_polling(bot)
    
    

if __name__ == "__main__":
    asyncio.run(main())



