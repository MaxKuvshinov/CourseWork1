import logging
import math
import os
from datetime import datetime
from typing import Union

import pandas as pd
import requests
from src.api_config import API_KEY_CURRENCY, API_KEY_STOCKS

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
    """Функция, которая читает список операций из Excel-файла и преобразует в словарь"""
    try:
        logger.info(f"Чтение данных из файла: {operations_list}")
        df = pd.read_excel(operations_list)
    except FileNotFoundError:
        logger.error(f"Файл {operations_list} не найден.")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {operations_list}: {e}")
        return []
    new_operations_list = []
    for index, row in df.iterrows():
        operations_dict = {
            "date_operation": row["Дата операции"],
            "date_payment": row["Дата платежа"],
            "card_number": row.get("Номер карты", ""),
            "status": row["Статус"],
            "transaction_amount": row["Сумма операции"],
            "transaction_currency": row["Валюта операции"],
            "amount_payment": row["Сумма платежа"],
            "payment_currency": row["Валюта платежа"],
            "cashback": row["Кэшбэк"],
            "category": row["Категория"],
            "MCC": row["MCC"],
            "description": row["Описание"],
            "bonuses": row["Бонусы (включая кэшбэк)"],
            "rounding_investment_bank": row["Округление на инвесткопилку"],
            "rounded_transaction_amount": row["Сумма операции с округлением"],
        }
        new_operations_list.append(operations_dict)

    logger.info(f"Успешно прочитано {len(new_operations_list)} операций из файла.")
    return new_operations_list


json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/operations.xls"))
logger.info(f"Путь к файлу с операциями{json_path}")
data_transactions = read_transactions_exel(json_path)


def filter_data_range(input_data, date_string):
    """Функция, которая фильтрует данные по диапазону дат от первого дня месяца до указанной даты."""
    dt = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")
    first_day = dt.replace(day=1)

    start_range = first_day
    end_range = dt
    logger.info(f"Диапазон дат: с {start_range.strftime('%d.%m.%Y')} по {end_range.strftime('%d.%m.%Y')}")

    filtered_data = [
        item
        for item in input_data
        if "date_operation" in item and start_range <= datetime.strptime(item["date_operation"][:10], "%d.%m.%Y") <= end_range
    ]
    logger.info(f"Найдено {len(filtered_data)} операций в указанном диапазоне дат.")

    return filtered_data


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
    """Возвращает приветствие в зависимости от переданного времени в строковом формате."""
    logger.info("Вывод приветствие в зависимости от времени дня")
    date_time = get_greeting(datetime.strptime(date_and_time, "%d-%m-%Y %H:%M:%S"))
    return date_time


def get_card_data(transactions: list[dict]) -> list[dict]:
    """Функция, которая анализирует транзакции и возвращает данные о картах с общей суммой трат и кэшбэком."""

    card_data = {}

    for transaction in transactions:
        if not isinstance(transaction, dict):
            logger.error(f"Транзакция имеет неверный тип: {type(transaction)}. Ожидался dict.")
            continue

        card_number = transaction.get("card_number", "")
        if isinstance(card_number, str) and len(card_number) >= 4:
            card_number = "*" + card_number[-4:].strip()
        else:
            logger.warning(f"Некорректный номер карты: {card_number}.")
            continue

        amount = transaction.get("transaction_amount", 0)
        cashback = transaction.get("cashback", 0)

        if card_number not in card_data:
            card_data[card_number] = {"total_spent": 0, "cashback": 0}

        card_data[card_number]["total_spent"] += amount

        if isinstance(cashback, (int, float)) and not math.isnan(cashback):
            card_data[card_number]["cashback"] += cashback
        else:
            card_data[card_number]["cashback"] += amount // 100  # Примерное значение кэшбэка, если не указано явно

    result = [
        {
            "last_digits": card,
            "total_spent": round(data["total_spent"], 2),
            "cashback": round(max(data["cashback"], 0), 2),
        }
        for card, data in card_data.items()
    ]

    logger.info(f"Обработано {len(result)} карт.")
    return result


def get_top_transactions(transactions: list[dict]) -> list[dict]:
    """Функция, которая возвращает топ-5 транзакций с наибольшей суммой"""

    logger.info("Начало обработки для получения топ-5 транзакций.")
    try:
        df = pd.DataFrame(transactions)
        logger.info("Транзакции успешно преобразованы в DataFrame.")

        required_columns = ["transaction_amount", "status", "date_operation", "category", "description"]
        for column in required_columns:
            if column not in df.columns:
                logger.error(f"Отсутствует необходимый столбец: {column}")
                raise ValueError(f"Отсутствует необходимый столбец: {column}")

        df = df[df["status"] == "OK"]
        logger.info("Фильтрация транзакций со статусом 'OK' завершена.")

        sorted_df = df.sort_values(by="transaction_amount", ascending=False)
        logger.info("Транзакции отсортированы по сумме в порядке убывания.")

        top_5_transactions = sorted_df.head(5)
        result = top_5_transactions[["date_operation", "transaction_amount", "category", "description"]].to_dict(
            orient="records"
        )

        logger.info(f"Выбрано топ-5 транзакций. Количество транзакций: {len(result)}.")

        return result

    except Exception as e:
        logger.error(f"Ошибка при обработке транзакций: {e}")
        return []


def get_currency_rates(api: str, currencies: dict) -> list[dict]:
    """Функция, которая получает данные о курсе валют из указанного API для заданной валюты"""
    result = []
    try:
        for currency in currencies["user_currencies"]:
            params = {"get": "rates", "pairs": f"{currency}RUB", "key": API_KEY_CURRENCY}

            response = requests.get(api, params=params)

            if response.status_code == 200:
                response_json = response.json()

                if "data" in response_json:
                    rate = list(response_json["data"].values())
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
    """Функция, которая получает данные об акциях из указанного API"""
    result = []
    try:
        logger.info("Перебираем акции из заданного списка словарей акций")
        for stock in stocks["user_stocks"]:
            logger.info(f"Делаем запрос на сервис API для получения цен акций для {stock}")

            params = {"symbol": stock, "token": API_KEY_STOCKS}

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
