from ORM.models import Currency


def convert_currency(val, from_currency, to_currency):
    exchange_rate = {
        Currency.USD: 1,
        Currency.EUR: 1.22,
        Currency.UAH: 0.036,
        Currency.PLN: 0.27,
        Currency.RUB: 0.014
    }

    return int(val * exchange_rate[from_currency] / exchange_rate[to_currency])
