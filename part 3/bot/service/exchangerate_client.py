import os
from aiohttp import ClientSession

from bot.schemas.error_schemas import APIError
from bot.schemas.exchange_rate_schema import CurrencyStr
from bot.schemas.string_constants import exchangerate_base_url
import bot.config as cfg

class ExchangeRateClient:
    """Клиент для общения с ExchangerRate-API"""
    
    def __init__(self, session: ClientSession) -> None:
        self._session = session
        self._api_key = cfg.EXCHANGERATE_API_KEY
        self.base_url = exchangerate_base_url
    
    async def request_rates(self, base: CurrencyStr) -> dict:
        request_string = f"{self.base_url}/{self._api_key}latest/{base}"
        async with self._session.get(request_string) as response:
            try:
                data = await response.json()
                rates = data["conversion_rates"]
            except:
                raise APIError
            return rates
            
            
             