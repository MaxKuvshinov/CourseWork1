# -*- coding: utf-8 -*-
import datetime
import os
from unittest.mock import Mock, patch
import requests

import pandas as pd
import pytest
from dotenv import load_dotenv
from src.utils import read_transactions_exel, filter_data_range, get_greeting,get_response_greeting,get_card_data, get_top_transactions, get_currency_rates, get_stock_price

load_dotenv()

API_KEY_CURRENCY = os.getenv("API_KEY_CURRENCY")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")


@patch("pandas.read_excel")
def test_read_transactions_exel(mock_read_excel):
    file_name = "test.xlsx"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    data = {
        "Дата операции": ["08.03.2018 20:35:03", "08.03.2018 20:12:02"],
        "Дата платежа": ["10.03.2018", "10.03.2018"],
        "Номер карты": ["*7197", "*7197"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-899.00, -1194.00],
        "Валюта операции": ["RUB", "RUB"],
        "Кэшбэк": [3, 0],
        "Категория": ["Одежда и обувь", "Одежда и обувь"],
        "Описание": ["OOO Sedmaya Avenyu", "Kontsept Klub"],
        "Сумма платежа": [0, 0],
        "Валюта платежа": ["RUB", "RUB"],
        "MCC": [0, 0],
        "Бонусы (включая кэшбэк)": [0, 0],
        "Округление на инвесткопилку": [0, 0],
        "Сумма операции с округлением": [0, 0],
    }
    df = pd.DataFrame(data)
    mock_read_excel.return_value = df
    result = read_transactions_exel(file_path)
    assert len(result) == 2
    assert result[0] == {
        "date_operation": "08.03.2018 20:35:03",
        "date_payment": "10.03.2018",
        "card_number": "*7197",
        "status": "OK",
        "transaction_amount": -899.00,
        "transaction_currency": "RUB",
        "amount_payment": 0,
        "payment_currency": "RUB",
        "cashback": 3,
        "category": "Одежда и обувь",
        "MCC": 0,
        "description": "OOO Sedmaya Avenyu",
        "bonuses": 0,
        "rounding_investment_bank": 0,
        "rounded_transaction_amount": 0,
    }
    assert result[1] == {
        "date_operation": "08.03.2018 20:12:02",
        "date_payment": "10.03.2018",
        "card_number": "*7197",
        "status": "OK",
        "transaction_amount": -1194.00,
        "transaction_currency": "RUB",
        "amount_payment": 0,
        "payment_currency": "RUB",
        "cashback": 0,
        "category": "Одежда и обувь",
        "MCC": 0,
        "description": "Kontsept Klub",
        "bonuses": 0,
        "rounding_investment_bank": 0,
        "rounded_transaction_amount": 0,
    }


@pytest.mark.parametrize(
    "date, expected",
    [
        (datetime.datetime(2021, 12, 31, 11, 0, 0), "Доброе утро!"),
        (datetime.datetime(2021, 12, 31, 15, 0, 0), "Добрый день!"),
        (datetime.datetime(2021, 12, 31, 20, 0, 0), "Добрый вечер!"),
        (datetime.datetime(2021, 12, 31, 23, 0, 0), "Доброй ночи!"),
    ],
)
def test_get_greeting(date, expected):
    assert get_greeting(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("31-12-2021 10:44:00", "Доброе утро!"),
        ("31-12-2021 16:44:00", "Добрый день!"),
        ("31-12-2021 19:44:00", "Добрый вечер!"),
        ("31-12-2021 23:44:00", "Доброй ночи!"),
    ],
)
def test_get_response_greeting(date, expected):
    assert get_response_greeting(date) == expected


def test_filter_data_range(transactions):
    result_empty = filter_data_range(transactions, "01-10-2021 09:56:08")
    assert result_empty == []


def test_get_card_data():
    transactions = [
        {
            "date_operation": "08.10.2021 20:15:16",
            "date_payment": "08.10.2021",
            "card_number": "*4556",
            "status": "OK",
            "transaction_amount": -399.0,
            "transaction_currency": "RUB",
            "amount_payment": -399.0,
            "payment_currency": "RUB",
            "cashback": 3.0,
            "category": "Онлайн-кинотеатры",
            "MCC": 7841.0,
            "description": "Иви",
            "bonuses": 3,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 399.0,
        },
        {
            "date_operation": "18.08.2019 17:54:47",
            "date_payment": "18.08.2019",
            "card_number": "*1112",
            "status": "FAILED",
            "transaction_amount": -3000.0,
            "transaction_currency": "RUB",
            "amount_payment": -3000.0,
            "payment_currency": "RUB",
            "cashback": "nan",
            "category": "nan",
            "MCC": "nan",
            "description": "Перевод с карты",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 3000.0,
        },
    ]

    result = get_card_data(transactions)
    assert result == [
        {"last_digits": "*4556", "total_spent": -399.0, "cashback": 3.0},
        {"last_digits": "*1112", "total_spent": -3000.0, "cashback": 0},
    ]

    transactions = [
        {
            "card_number": "*4556",
            "transaction_amount": 100000.0,
            "cashback": 0,
        },
        {
            "card_number": "*4556",
            "transaction_amount": 70000.0,
            "cashback": 0,
        },
        {
            "card_number": "*7197",
            "transaction_amount": -187.0,
            "cashback": 0,
        },
    ]

    result = get_card_data(transactions)
    assert result == [
        {"last_digits": "*4556", "total_spent": 170000.0, "cashback": 0},
        {"last_digits": "*7197", "total_spent": -187.0, "cashback": 0},
    ]


def test_get_top_transactions():
    transactions = [
        {
            "date_operation": "08.10.2021 20:15:16",
            "date_payment": "08.10.2021",
            "card_number": "*4556",
            "status": "OK",
            "transaction_amount": 1000.0,
            "transaction_currency": "RUB",
            "amount_payment": 1000.0,
            "payment_currency": "RUB",
            "cashback": 0,
            "category": "Онлайн-кинотеатры",
            "MCC": 7841.0,
            "description": "Иви",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 1000.0,
        },
        {
            "date_operation": "18.08.2019 17:54:47",
            "date_payment": "18.08.2019",
            "card_number": "*1112",
            "status": "OK",
            "transaction_amount": 2000.0,
            "transaction_currency": "RUB",
            "amount_payment": 2000.0,
            "payment_currency": "RUB",
            "cashback": 0,
            "category": "Онлайн-магазины",
            "MCC": 7997.0,
            "description": "Алиэкспресс",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 2000.0,
        },
        {
            "date_operation": "15.07.2020 10:30:00",
            "date_payment": "15.07.2020",
            "card_number": "*4556",
            "status": "OK",
            "transaction_amount": 3000.0,
            "transaction_currency": "RUB",
            "amount_payment": 3000.0,
            "payment_currency": "RUB",
            "cashback": 0,
            "category": "Рестораны",
            "MCC": 5812.0,
            "description": "Макдональдс",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 3000.0,
        },
        {
            "date_operation": "20.05.2022 12:00:00",
            "date_payment": "20.05.2022",
            "card_number": "*1112",
            "status": "OK",
            "transaction_amount": 4000.0,
            "transaction_currency": "RUB",
            "amount_payment": 4000.0,
            "payment_currency": "RUB",
            "cashback": 0,
            "category": "Онлайн-магазины",
            "MCC": 7997.0,
            "description": "Алиэкспресс",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 4000.0,
        },
        {
            "date_operation": "25.03.2023 14:00:00",
            "date_payment": "25.03.2023",
            "card_number": "*4556",
            "status": "OK",
            "transaction_amount": 5000.0,
            "transaction_currency": "RUB",
            "amount_payment": 5000.0,
            "payment_currency": "RUB",
            "cashback": 0,
            "category": "Рестораны",
            "MCC": 5812.0,
            "description": "Макдональдс",
            "bonuses": 0,
            "rounding_investment_bank": 0,
            "rounded_transaction_amount": 5000.0,
        },
    ]

    expected_result = [
        {
            "date_operation": "25.03.2023 14:00:00",
            "transaction_amount": 5000.0,
            "category": "Рестораны",
            "description": "Макдональдс",
        },
        {
            "date_operation": "20.05.2022 12:00:00",
            "transaction_amount": 4000.0,
            "category": "Онлайн-магазины",
            "description": "Алиэкспресс",
        },
        {
            "date_operation": "15.07.2020 10:30:00",
            "transaction_amount": 3000.0,
            "category": "Рестораны",
            "description": "Макдональдс",
        },
        {
            "date_operation": "18.08.2019 17:54:47",
            "transaction_amount": 2000.0,
            "category": "Онлайн-магазины",
            "description": "Алиэкспресс",
        },
        {
            "date_operation": "08.10.2021 20:15:16",
            "transaction_amount": 1000.0,
            "category": "Онлайн-кинотеатры",
            "description": "Иви",
        },
    ]

    result = get_top_transactions(transactions)
    assert result == expected_result


@pytest.fixture
def mock_get():
    with patch("requests.get") as mock:
        yield mock


def test_get_currency_rates_success(mock_get):
    api = "https://api.example.com"
    currencies = {"user_currencies": ["USD", "EUR", "GBP"]}

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"USD": 1.0, "EUR": 2.0, "GBP": 3.0}}
    mock_get.return_value = mock_response

    result = get_currency_rates(api, currencies)

    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert isinstance(item, dict)
        assert "currency" in item
        assert "rate" in item


@patch("requests.get")
def test_get_currency_rates_error(mock_get):
    api = "https://api.example.com"
    currencies = {"user_currencies": ["USD", "EUR"]}

    import requests

    mock_get.side_effect = requests.exceptions.RequestException

    result = get_currency_rates(api, currencies)
    assert result == []


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get


# Test case for successful retrieval of stock prices
def test_get_stock_price_success(mock_requests_get):
    api = "https://api.example.com/stocks"
    stocks = {"user_stocks": ["AAPL", "GOOGL", "MSFT"]}


    mock_response_aapl = Mock()
    mock_response_aapl.status_code = 200
    mock_response_aapl.json.return_value = {"c": 150.0}

    mock_response_googl = Mock()
    mock_response_googl.status_code = 200
    mock_response_googl.json.return_value = {"c": 2500.0}

    mock_response_msft = Mock()
    mock_response_msft.status_code = 200
    mock_response_msft.json.return_value = {"c": 300.0}

    mock_requests_get.side_effect = [mock_response_aapl, mock_response_googl, mock_response_msft]

    result = get_stock_price(api, stocks)

    assert isinstance(result, list)
    assert len(result) == 3

    expected_result = [
        {"stock": "AAPL", "price": 150.0},
        {"stock": "GOOGL", "price": 2500.0},
        {"stock": "MSFT", "price": 300.0}
    ]

    assert result == expected_result


@patch("requests.get")
def test_get_stock_price_error(mock_get):
    api = "https://api.example.com"
    currencies = {"user_stocks": ["AAPL", "AMZN", "GOOGL"]}

    import requests

    mock_get.side_effect = requests.exceptions.RequestException

    result = get_stock_price(api, currencies)
    assert result == []
