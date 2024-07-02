import json
import os
from dotenv import load_dotenv


load_dotenv()

url_currency = "https://currate.ru/api/"
url_stocks = "https://finnhub.io/api/v1/quote"


json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../user_settings.json"))
with open(json_path, "r") as file:
    data_json = json.load(file)


date = "19-11-2021 15:30:00"


load_dotenv()

API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")
