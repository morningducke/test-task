
import asyncio
import logging
import re
import sys
import os
import bot.config as cfg

from aiohttp import ClientSession
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from pydantic import ValidationError

from bot.service.exchange_rates import get_exchange_rate
from bot.service.exchangerate_client import ExchangeRateClient
from bot.schemas.error_schemas import APIError
from bot.schemas.string_constants import start_string, fallback_string, commands_info_string

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Ответ на команду /start"""
    await message.answer(start_string)

@dp.message(Command("rate"))
async def command_rate_handler(message: Message, command: CommandObject) -> None:
    """Ответ на команду /rate.
       Принимается две версии: /rate [currency] - возвращает курс относительно рубля
                               /rate [base] [currency] возвращает курс [currency] относительно [base]"""
       
    if command.args is None:
        await message.answer("Ошибка: не передана валюта для сравнения")
        return
    
    try:
        currencies = command.args.split()
        currencies = list(map(str.upper, currencies)) # перевод в заглавные буквы всех аргументов
        
        if len(currencies) == 1:
            rate = await get_exchange_rate(base="RUB", query=currencies[0], client=exchangerate_client)
        elif len(currencies) == 2:
            rate = await get_exchange_rate(base=currencies[0], query=currencies[1], client=exchangerate_client)
        else:
            await message.answer("Ошибка: больше чем два аргумента. Пример: /rate RUB USD")
            return
        
    except ValidationError:
        await message.answer(f"Ошибка: название валюты должно состоять из трех букв латинского алфавита. Пример: /rate USD")
        return
    except APIError:
        await message.answer(f"Ошибка: что-то не так с API провайдером...")
        return
    except ValueError:
        await message.answer(f"Введенной валюты не существует.")
        return
    
    await message.answer(f"1 {rate.base_currency} = {rate.rate} {rate.query_currency}") 

@dp.message(Command("help"))
async def command_rate_handler(message: Message) -> None:
    """Выводит список команд"""
    await message.answer(commands_info_string)
        
    
@dp.message(Command(re.compile(r"^.+$")))
async def command_fallback(message: Message) -> None:
    """Fallback для неиизвестных команд. Функция всегда должна находиться последней."""
    await message.answer(fallback_string)

 
async def main() -> None:
    bot = Bot(token=cfg.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    async with ClientSession() as session:
        global exchangerate_client # для повторного использования сессии
        exchangerate_client = ExchangeRateClient(session=session)
        await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())