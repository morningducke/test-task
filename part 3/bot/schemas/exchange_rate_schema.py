from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

# валюта - 3 заглавных буквы латинского алфавита
CurrencyStr = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}$")]

class ExchangeRate(BaseModel):
    """Модель, несущая информацию о курсе валют"""
    base_currency: CurrencyStr
    query_currency: CurrencyStr
    rate: float = Field(gt=0.) # не должно вызывать проблем со сравнением float в силу максимальной разницы между валютами


