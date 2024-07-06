# -*- coding: utf-8 -*-
import json
import logging
import os

from dotenv import load_dotenv

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("api_config")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "api_config.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


load_dotenv()

logger.info("URL Api для валют и акций")
url_currency = "https://currate.ru/api/"
url_stocks = "https://finnhub.io/api/v1/quote"

logger.info("Путь к файлу с настройками")
json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../user_settings.json"))
with open(json_path, "r") as file:
    data_json = json.load(file)

logger.info("Заданная дата")
date = "20-09-2021 15:30:00"

load_dotenv()

API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")
