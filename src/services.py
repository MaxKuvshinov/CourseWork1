import logging
import os
import re
from typing import Dict, List
import json

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("services")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "services.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def find_transactions_with_phone_numbers(data: List[Dict]) -> str:
    """Функция, которая находит транзакции содержащие номер телефона"""

    logger.info("Регулярное выражение для поиска номеров телефонов")
    phone_pattern = re.compile(r"\+7[\s\(\)-]*\d{3}[\s\(\)-]*\d{3}[\s\(\)-]*\d{2}[\s\(\)-]*\d{2}")

    def contains_phone_number(transaction: Dict) -> bool:
        """Функция, которая проверяет, содержит ли описание транзакции номер телефона"""
        return bool(phone_pattern.search(transaction.get("description", "")))

    transactions_with_phone = [
        transaction for transaction in data
        if contains_phone_number(transaction)
    ]

    logger.info(f"Найдено {len(transactions_with_phone)} транзакций с номерами телефонов.")

    return json.dumps(transactions_with_phone, ensure_ascii=False, indent=4)
