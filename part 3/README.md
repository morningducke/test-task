# Телеграм бот для отслеживания курсов валют.
https://t.me/xch_rate_bot

Команды: <br>
/rate [currency] - получить текущий курс указанной валюты [currency] по отношению к RUB <br>
/rate [base] [currency] - получить текущий курс указанной валюты [currency] по отношению к [base] <br>

Используемый API: https://www.exchangerate-api.com/. Выбран, так как показался наиболее удобным и бесплатный tier даёт много запросов в месяц. <br>
Поддержка валют: 99% мировых валют <br>

Предложения по улучшению функционала: <br>
1. Возможность получать курс валюты относительно любой другой (сделано)
2. Прикрутить БД для, например, возможности давать пользователю настраивать базовую валюты для команды /rate [currency]

