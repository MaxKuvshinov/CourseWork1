import logging
import os
from datetime import datetime
import math
import requests
from main import API_KEY_CURRENCY, API_KEY_STOCKS
from typing import Union,Any

import pandas as pd

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("utils")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "utils.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_transactions_exel(operations_list: str) -> list[dict]:
    df = pd.read_excel(operations_list)
    new_operations_list = []
    for index, row in df.iterrows():
        operations_dict = {
            "Date_operation": row["Дата операции"],
            "Date_payment": row["Дата платежа"],
            "Card_number": row.get("Номер карты", ""),
            "Status": row["Статус"],
            "Transaction_amount": row["Сумма операции"],
            "Transaction_currency": row["Валюта операции"],
            "Amount_payment": row["Сумма платежа"],
            "Payment_currency": row["Валюта платежа"],
            "Cashback": row["Кэшбэк"],
            "Category": row["Категория"],
            "MCC": row["MCC"],
            "Description": row["Описание"],
            "Bonuses": row["Бонусы (включая кэшбэк)"],
            "Rounding_investment_bank": row["Округление на инвесткопилку"],
            "Rounded_transaction_amount": row["Сумма операции с округлением"],
        }
        new_operations_list.append(operations_dict)

    return new_operations_list


json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/operations.xls"))
data_transactions = json_path


def get_greeting(time: datetime) -> str:
    """Приветствие в зависимости от времени дня"""
    hour = time.hour
    logger.info("Проверка времени для корректного приветствия")
    if 6 <= hour < 12:
        return "Доброе утро!"
    elif 12 <= hour < 18:
        return "Добрый день!"
    elif 18 <= hour < 22:
        return "Добрый вечер!"
    else:
        return "Доброй ночи!"


def get_response_greeting(date_and_time: str) -> str:
    logger.info("Вывод приветствие в зависимости от времени дня")
    date_time = get_greeting(datetime.strptime(date_and_time, "%d-%m-%Y %H:%M:%S"))
    return date_time


def get_card_data(transactions: list[dict]) -> list[dict]:
    card_data = {}

    for transaction in transactions:
        if not isinstance(transaction, dict):
            logger.error(f"Транзакция имеет неверный тип: {type(transaction)}. Ожидался dict.")
            continue

        card_number = transaction.get("Card_number", "")
        if isinstance(card_number, str) and len(card_number) >= 4:
            card_number = card_number[-4:]
        else:
            continue

        amount = transaction["Transaction_amount"]
        if card_number not in card_data:
            card_data[card_number] = {
                "total_spent": 0,
                "cashback": 0
            }
        card_data[card_number]["total_spent"] += amount
        cashback = transaction["Cashback"]

        if isinstance(cashback, (int, float)) and not math.isnan(cashback):
            card_data[card_number]["cashback"] += cashback
        else:
            card_data[card_number]["cashback"] += amount // 100

    result = [{"last_digits": card,
               "total_spent": round(data["total_spent"], 2),
               "cashback": round(max(data["cashback"], 0), 2)}
              for card, data in card_data.items()]

    return result


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    df = pd.DataFrame(transactions)
    required_columns = ["Transaction_amount", "Status", "Date_operation", "Category", "Description"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Такой столбец отсутствует")
    df = df[df["Status"] == "OK"]
    sorted_df = df.sort_values(by="Transaction_amount", ascending=False)
    top_5_transactions = sorted_df.head(5)
    result = top_5_transactions[["Date_operation", "Transaction_amount", "Category", "Description"]].to_dict(orient="records")

    return result


def get_currency_rates(api: str, currencies: dict) -> list[dict]:
    """Функция, которая получает данные о курсе валют из указанного API для заданной валюты"""
    result = []
    try:
        for currency in currencies["user_currencies"]:
            params = {
                "get": "rates",
                "pairs": f"{currency}RUB",
                "key": API_KEY_CURRENCY
            }

            response = requests.get(api, params=params)

            if response.status_code == 200:
                response_json = response.json()

                if "data" in response_json:
                    rate = list(response_json["data"].values())[0]
                    result.append({"currency": currency, "rate": rate})
                    logger.info(f"Получены данные для {currency}: курс {rate}")
                else:
                    logger.error(f"Не удалось получить данные для {currency}: JSON не содержит ожидаемых данных")
            else:
                logger.error(f"Ошибка при запросе к API для {currency}: {response.status_code}")

        logger.info("Выводим результат")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return []


def get_stock_price(api: str, stocks: dict) -> Union[list[dict]]:
    result = []
    try:
        logger.info("Перебираем акции из заданного списка словарей акций")
        for stock in stocks["user_stocks"]:
            logger.info(f"Делаем запрос на сервис API для получения цен акций для {stock}")

            params = {
                "symbol": stock,
                "token": API_KEY_STOCKS
            }

            response = requests.get(api, params=params)

            if response.status_code == 200:
                response_json = response.json()

                if "c" in response_json:
                    price = response_json["c"]
                    result.append({"stock": stock, "price": price})

                else:
                    logger.error(f"Не удалось получить данные для {stock}:")
            else:
                logger.error(f"Ошибка при запросе к API для {stock}: {response.status_code}")

        logger.info("Выводим результат")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при запросе к API: {e}")
        return []
