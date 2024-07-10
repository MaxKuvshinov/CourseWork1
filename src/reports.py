import logging
import os
from datetime import datetime, timedelta
from typing import Callable, Any, Optional
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


def write_to_file(file_name: str) -> Callable[[Callable[..., str]], Callable[..., str]]:
    """Декоратор для записи результата функции в файл."""

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        def wrapper(*args: Any, **kwargs: Any) -> str:
            logger.info(f"Вызов функции {func.__name__}")
            result = func(*args, **kwargs)
            try:
                with open(file_name, "w") as file:
                    file.write(result + "\n")
                logger.info(f"Результат функции {func.__name__} записан в файл {file_name}")
            except Exception as e:
                logger.error(f"Ошибка при записи результата в файл {file_name}: {e}")
            return result

        return wrapper

    return decorator


@write_to_file(file_name="spending_report.txt")
def spending_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """Функция для анализа трат по категории за последние три месяца."""
    if date is None:
        selected_date = datetime.today().strftime("%Y-%m-%d")
    else:
        selected_date = pd.to_datetime(date, dayfirst=True).strftime("%Y-%m-%d")

    pd_transactions = pd.DataFrame(transactions)
    three_months_ago = (pd.to_datetime(selected_date) - timedelta(days=90)).strftime("%Y-%m-%d")
    logger.info(f"Анализ транзакций за период с {three_months_ago} по {selected_date}")
    filtered_transactions = pd_transactions[
        (pd_transactions["category"] == category)
        & (pd.to_datetime(pd_transactions["date_operation"], dayfirst=True).between(three_months_ago, selected_date))
    ]

    spending = filtered_transactions.groupby("date_operation")["transaction_amount"].sum().reset_index()
    logger.info("Результаты преобразованы в JSON-строку.")

    return spending.to_json(orient="records", indent=4)
