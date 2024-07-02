import os
import logging
import re
from typing import List, Dict
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


def find_transactions_with_phone_numbers(data: List[Dict], search_number_phone: str) -> List[Dict]:
    phone_pattern = re.compile(r"\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}")

    def contains_phone_number(transaction: Dict) -> bool:
        return bool(phone_pattern.search(transaction.get("Description", "")))

    transactions_with_phone = list(filter(contains_phone_number, data))
    return transactions_with_phone
