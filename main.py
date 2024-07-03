from src.views import main
from src.utils import data_transactions
from src.services import find_transactions_with_phone_numbers
from src.reports import spending_category
from src.api_config import date


print(main(date))
print(spending_category(data_transactions, "Супермаркеты", date))
print(find_transactions_with_phone_numbers(data_transactions))
