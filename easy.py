import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

def plot(data):
    data_sorted = list(reversed(data))
    dates = [item["exchangedate"] for item in data_sorted]
    rates = [item["rate"] for item in data_sorted]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker="o", color="#1f77b4", linewidth=2, label="eur / uah")
    plt.grid(True, linestyle="--", alpha=0.5) 
    plt.legend()
    plt.tight_layout()
    plt.savefig("nbu_rates.png")




today = datetime.now()
week_ago = today - timedelta(days=7)
start_date_string = week_ago.strftime("%Y%m%d")
end_date_string = today.strftime("%Y%m%d")


base_url = "https://bank.gov.ua/NBU_Exchange/exchange_site"

params = {
        "start": start_date_string,
        "end": end_date_string,
        "valcode": "eur",
        "sort": "exchangedate",
        "order": "desc",
        "json": ""
        }

if __name__ == "__main__":
    r = requests.get(base_url, params=params)
    print(r.json())
    plot(r.json())

    
