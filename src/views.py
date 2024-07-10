import json
import logging
import os

from src.api_config import data_json, url_currency, url_stocks
from src.utils import (
    data_transactions,
    filter_data_range,
    get_card_data,
    get_currency_rates,
    get_response_greeting,
    get_stock_price,
    get_top_transactions,
)

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("views")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "views.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main(date: str) -> str:
    """Функция, которая вызывает остальные функции для главной страницы, преобразовывая в необходимый словарь"""
    logger.info("Приветствие")
    greeting = get_response_greeting(date)
    logger.info("Список транзакций")
    transactions = get_card_data(filter_data_range(data_transactions, date))
    logger.info("Топ-5 транзакций")
    top_transactions = get_top_transactions(filter_data_range(data_transactions, date))
    logger.info("Актуальный курс валют")
    course = get_currency_rates(url_currency, data_json)
    logger.info("Актуальная стоимость акций")
    stock_prices = get_stock_price(url_stocks, data_json)

    logger.info("Преобразование к корректному словарю")
    response = {
        "greeting": greeting,
        "cards": transactions,
        "top_transactions": top_transactions,
        "currency_rates": course,
        "stock_prices": stock_prices,
    }

    logger.info("Вывод полученного результата")
    return json.dumps(response, ensure_ascii=False, indent=4)
