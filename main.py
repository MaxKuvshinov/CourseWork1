from src.views import main
from src.external_api import date
from src.utils import data_transactions
from src.services import find_transactions_with_phone_numbers
from src.reports import spending_by_category

print(main(date))
print(spending_by_category(data_transactions, "Супермаркеты", date))
search_number_phone = input("Введите номер телефона для поиска: ")
print(find_transactions_with_phone_numbers(data_transactions, search_number_phone))
