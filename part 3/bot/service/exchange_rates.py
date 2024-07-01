from bot.service.exchangerate_client import ExchangeRateClient
from bot.schemas.exchange_rate_schema import CurrencyStr, ExchangeRate
from pydantic import validate_call

@validate_call(config=dict(arbitrary_types_allowed=True))
async def get_exchange_rate(base: CurrencyStr, query: CurrencyStr, client: ExchangeRateClient) -> ExchangeRate:
    """Получает курс относительно базовой валюты

    Args:
        base (CurrencyStr): строка-идентификатор базовый валюты (пример: RUB)
        query (CurrencyStr): строка-идентификатор валюты для сравнения с базовой
        client (ExchangeRateClient): клиент, отправлюящий запросы к Exchange-Rate-API

    Raises:
        ValueError: возникает в случае ввода несуществующей валюты

    Returns:
        ExchangeRate: структура, содержащая строку базовой валюты, валюты для сравнения и курс (float)
    """
    
    rates = await client.request_rates(base)
    if query not in rates:
        raise ValueError
    rate = rates[query]
    return ExchangeRate(base_currency=base, query_currency=query, rate=rate)