import requests
from datetime import date, timedelta


def yyyymmdd(d: date) -> str:
    return d.strftime("%Y%m%d")


def fetch_nbu_rates_last_week(valcode: str = "usd"):
    end = date.today()
    start = end - timedelta(days=7)

    params = {
        "start": yyyymmdd(start),
        "end": yyyymmdd(end),
        "sort": "exchangedate",
        "order": "desc",
        "json": ""
    }

    if valcode:
        params["valcode"] = valcode

    url = "https://bank.gov.ua/NBU_Exchange/exchange_site"
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()

    data = r.json()
    return data


if __name__ == "__main__":
    rates = fetch_nbu_rates_last_week("usd")

    for item in rates:
        print(f"{item['exchangedate']} {item['cc']}: {item['rate']}")
