# -*- coding: utf-8 -*-
import json
from unittest.mock import patch

import pytest
from src.views import main


@pytest.fixture
def mock_get_response_greeting():
    with patch("src.views.get_response_greeting") as mock:
        mock.return_value = "Добрый день!"
        yield mock


@pytest.fixture
def mock_get_card_data():
    with patch("src.views.get_card_data") as mock:
        mock.return_value = [
            {"last_digits": "*7197", "total_spent": -40152.67, "cashback": 0},
            {"last_digits": "*4556", "total_spent": -5747.0, "cashback": 0},
        ]
        yield mock


@pytest.fixture
def mock_get_top_transactions():
    with patch("src.views.get_top_transactions") as mock:
        mock.return_value = [
            {
                "date_operation": "14.09.2021 14:57:42",
                "transaction_amount": 150000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "15.09.2021 15:38:43",
                "transaction_amount": 100000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "09.09.2021 16:31:58",
                "transaction_amount": 3000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "16.09.2021 23:32:16",
                "transaction_amount": 61.0,
                "category": "Бонусы",
                "description": "Вознаграждение за операции покупок",
            },
            {
                "date_operation": "03.09.2021 16:00:02",
                "transaction_amount": -1.0,
                "category": "Каршеринг",
                "description": "Ситидрайв",
            },
        ]
        yield mock


@pytest.fixture
def mock_get_currency_rates():
    with patch("src.views.get_currency_rates") as mock:
        mock.return_value = [{"currency": "USD", "rate": ["64.1824"]}, {"currency": "EUR", "rate": ["69.244"]}]
        yield mock


@pytest.fixture
def mock_get_stock_price():
    with patch("src.views.get_stock_price") as mock:
        mock.return_value = [
            {"stock": "AAPL", "price": 221.085},
            {"stock": "AMZN", "price": 197.74},
            {"stock": "GOOGL", "price": 185.98},
            {"stock": "MSFT", "price": 460.1654},
            {"stock": "TSLA", "price": 243.8858},
        ]
        yield mock


def test_main(
    mock_get_response_greeting,
    mock_get_card_data,
    mock_get_top_transactions,
    mock_get_currency_rates,
    mock_get_stock_price,
):
    date = "20-09-2021 15:30:00"
    result = main(date)

    expected_result = {
        "greeting": "Добрый день!",
        "cards": [
            {"last_digits": "*7197", "total_spent": -40152.67, "cashback": 0},
            {"last_digits": "*4556", "total_spent": -5747.0, "cashback": 0},
        ],
        "top_transactions": [
            {
                "date_operation": "14.09.2021 14:57:42",
                "transaction_amount": 150000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "15.09.2021 15:38:43",
                "transaction_amount": 100000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "09.09.2021 16:31:58",
                "transaction_amount": 3000.0,
                "category": "Пополнения",
                "description": "Перевод с карты",
            },
            {
                "date_operation": "16.09.2021 23:32:16",
                "transaction_amount": 61.0,
                "category": "Бонусы",
                "description": "Вознаграждение за операции покупок",
            },
            {
                "date_operation": "03.09.2021 16:00:02",
                "transaction_amount": -1.0,
                "category": "Каршеринг",
                "description": "Ситидрайв",
            },
        ],
        "currency_rates": [{"currency": "USD", "rate": ["64.1824"]}, {"currency": "EUR", "rate": ["69.244"]}],
        "stock_prices": [
            {"stock": "AAPL", "price": 221.085},
            {"stock": "AMZN", "price": 197.74},
            {"stock": "GOOGL", "price": 185.98},
            {"stock": "MSFT", "price": 460.1654},
            {"stock": "TSLA", "price": 243.8858},
        ],
    }

    assert json.loads(result) == expected_result
