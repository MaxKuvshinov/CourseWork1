import pytest
from src.utils import get_stock_price, read_transactions_exel, get_currency_rates, filter_data_range, get_greeting, get_card_data, get_top_transactions
import os
import unittest
from unittest.mock import patch
import pandas as pd

from datetime import datetime


@pytest.fixture
def sample_transactions():
    data = {
        "date_operation": ["01.04.2023", "01.05.2023", "01.06.2023", "01.07.2023"],
        "category": ["Food", "Food", "Food", "Shopping"],
        "transaction_amount": [100.0, 200.0, 150.0, 300.0],
        "status": ["OK", "OK", "OK", "FAILED"],
        "description": ["Grocery", "Restaurant", "Cafe", "Clothes"]
    }
    return pd.DataFrame(data)


@patch("pandas.read_excel")
def test_read_transactions_exel(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame({
        "Дата операции": ["01.04.2023"],
        "Дата платежа": ["02.04.2023"],
        "Номер карты": ["1234"],
        "Статус": ["OK"],
        "Сумма операции": [100.0],
        "Валюта операции": ["RUB"],
        "Сумма платежа": [100.0],
        "Валюта платежа": ["RUB"],
        "Кэшбэк": [1.0],
        "Категория": ["Food"],
        "MCC": [5411],
        "Описание": ["Grocery"],
        "Бонусы (включая кэшбэк)": [1.0],
        "Округление на инвесткопилку": [0.0],
        "Сумма операции с округлением": [100.0]
    })

    result = read_transactions_exel("dummy_path")
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["date_operation"] == "01.04.2023"


def test_filter_data_range(sample_transactions):
    input_data = sample_transactions.to_dict(orient='records')
    filtered_data = filter_data_range(input_data, "01-07-2020 23:59:59")

    assert len(filtered_data) == 4
    assert filtered_data[0]["date_operation"] == "01.04.2020"


@pytest.mark.parametrize("hour,expected_greeting", [
    (7, "Доброе утро!"),
    (13, "Добрый день!"),
    (19, "Добрый вечер!"),
    (23, "Доброй ночи!")
])
def test_get_greeting(hour, expected_greeting):
    with patch("my_module.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2023, 7, 1, hour)
        assert get_greeting(mock_datetime.now()) == expected_greeting


def test_get_card_data(sample_transactions):
    input_data = sample_transactions.to_dict(orient='records')
    card_data = get_card_data(input_data)

    assert isinstance(card_data, list)
    assert len(card_data) > 0
    assert "last_digits" in card_data[0]
    assert "total_spent" in card_data[0]
    assert "cashback" in card_data[0]


def test_get_top_transactions(sample_transactions):
    input_data = sample_transactions.to_dict(orient='records')
    top_transactions = get_top_transactions(input_data)

    assert isinstance(top_transactions, list)
    assert len(top_transactions) == 3
    assert top_transactions[0]["transaction_amount"] == 200.0


@patch("requests.get")
def test_get_currency_rates(mock_get):
    mock_response = {
        "data": {"USDRUB": 74.5}
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api_url = "http://fakeapi.com"
    currencies = {"user_currencies": ["USD"]}
    rates = get_currency_rates(api_url, currencies)

    assert isinstance(rates, list)
    assert len(rates) == 1
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 74.5


@patch("requests.get")
def test_get_stock_price(mock_get):
    mock_response = {
        "c": 150.0
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    api_url = "http://fakeapi.com"
    stocks = {"user_stocks": ["AAPL"]}
    prices = get_stock_price(api_url, stocks)

    assert isinstance(prices, list)
    assert len(prices) == 1
    assert prices[0]["stock"] == "AAPL"
    assert prices[0]["price"] == 150.0


