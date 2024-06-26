import logging
import os
from src.utils import read_transactions_exel, get_card_data, get_greeting, get_response_greeting, get_currency_rates, get_top_transactions, get_stock_price, data_transactions
from main import date_time_obj, data_json, url_stocks, url_currency
import json

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "views.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main():
    greeting = get_greeting(date_time_obj)
    transactions = get_card_data(data_transactions)
    top_transactions = get_top_transactions(data_transactions)
    course = get_currency_rates(url_currency, data_json)
    stock_prices = get_stock_price(url_stocks, date_time_obj)

    response = {
        "greeting": greeting,
        "cards": transactions,
        "top_transactions": top_transactions,
        "currency_rates": course,
        "stock_prices": stock_prices,
    }

    logger.info("Выводим результат")
    return json.dumps(response, ensure_ascii=False)


if __name__ == "__main__":
    main()