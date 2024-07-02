import os
import logging
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd


log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("reports")
logger.setLevel(logging.INFO)
log_filename = os.path.join(log_dir, "reports.log")
file_handler = logging.FileHandler(log_filename, mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


# Функция для анализа трат по категории за последние три месяца
def write_to_file(file_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(file_name, "w") as file:
                file.write(result.to_string(index=False) + "\n")
            return result

        return wrapper

    return decorator


@write_to_file(file_name="spending_report.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> pd.DataFrame:
    if date is None:
        selected_date = datetime.today().strftime("%Y-%m-%d")
    else:
        selected_date = pd.to_datetime(date, dayfirst=True)

    pd_transactions = pd.DataFrame(transactions)
    three_months_ago = selected_date - timedelta(days=90)

    filtered_transactions = pd_transactions[
        (pd_transactions["Category"] == category)
        & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) >= three_months_ago)
        & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) <= selected_date)
    ]

    spending = filtered_transactions.groupby("Date_operation")["Transaction_amount"].sum().reset_index()

    return spending
