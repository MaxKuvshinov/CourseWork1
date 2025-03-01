# -*- coding: utf-8 -*-
import pytest


@pytest.fixture
def transactions_data():
    return [
        {
            "Date_operation": "30.08.2019 10:47:00",
            "Payment_date": "31.08.2019",
            "Card_numbers": "*4556",
            "Status": "OK",
            "amount": -100.0,
            "currency": "RUB",
            "Payment amount": -100.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "Связь",
            "MCC": 4814.0,
            "Description": "МТС",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 100.0,
        },
        {
            "Date_operation": "27.08.2019 11:28:58",
            "Payment_date": "27.08.2019",
            "Card_numbers": "*4556",
            "Status": "OK",
            "amount": 200.0,
            "currency": "RUB",
            "Payment amount": 200.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "Переводы",
            "MCC": "nan",
            "Description": "Пополнение счета",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 200.0,
        },
        {
            "Date_operation": "18.08.2019 17:54:47",
            "Payment_date": "18.08.2019",
            "Card_numbers": "*1112",
            "Status": "FAILED",
            "amount": -3000.0,
            "currency": "RUB",
            "Payment amount": -3000.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "nan",
            "MCC": "nan",
            "Description": "Перевод с карты",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 3000.0,
        },
        {
            "Date_operation": "03.01.2018 14:55:21",
            "Payment_date": "05.01.2018",
            "Card_numbers": "*7197",
            "Status": "OK",
            "amount": -21.0,
            "currency": "RUB",
            "Payment amount": -21.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "Красота",
            "MCC": 5977.0,
            "Description": "OOO Balid",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 21.0,
        },
        {
            "Date_operation": "01.01.2018 20:27:51",
            "Payment_date": "04.01.2018",
            "Card_numbers": "*7197",
            "Status": "OK",
            "amount": -316.0,
            "currency": "RUB",
            "Payment amount": -316.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "Красота",
            "MCC": 5977.0,
            "Description": "OOO Balid",
            "Bonuses": 6,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 316.0,
        },
        {
            "Date_operation": "01.01.2018 12:49:53",
            "Payment_date": "01.01.2018",
            "Card_numbers": "nan",
            "Status": "OK",
            "amount": -3000.0,
            "currency": "RUB",
            "Payment amount": -3000.0,
            "Payment currency": "RUB",
            "Cashback": "nan",
            "Category": "Переводы",
            "MCC": "nan",
            "Description": "Линзомат ТЦ Юность",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 3000.0,
        },
    ]


@pytest.fixture
def sort_search():
    return [
        {
            "Date_operation": "08.10.2021 20:15:16",
            "Payment_date": "08.10.2021",
            "Card_numbers": "*4556",
            "Status": "OK",
            "amount": -399.0,
            "currency": "RUB",
            "Payment amount": -399.0,
            "Payment currency": "RUB",
            "Cashback": 3.0,
            "Category": "Онлайн-кинотеатры",
            "MCC": 7841.0,
            "Description": "Иви",
            "Bonuses": 3,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 399.0,
        }
    ]


@pytest.fixture
def transactions():
    return [
        {
            "Date_operation": "01.10.2020 09:56:08",
            "Payment_date": "01.10.2020",
            "Card_numbers": "*4556",
            "Status": "OK",
            "amount": 50000.0,
            "currency": "RUB",
            "Payment amount": 50000.0,
            "Payment currency": "RUB",
            "Cashback": "NaN",
            "Category": "Переводы",
            "MCC": "NaN",
            "Description": "Игорь Б.",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 50000.0,
        },
        {
            "Date_operation": "30.09.2020 11:53:24",
            "Payment_date": "30.09.2020",
            "Card_numbers": "*4556",
            "Status": "OK",
            "amount": 120000.0,
            "currency": "RUB",
            "Payment amount": 120000.0,
            "Payment currency": "RUB",
            "Cashback": "NaN",
            "Category": "Переводы",
            "MCC": "NaN",
            "Description": "Игорь Б.",
            "Bonuses": 0,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 120000.0,
        },
        {
            "Date_operation": "09.07.2018 18:29:03",
            "Payment_date": "11.07.2018",
            "Card_numbers": "*7197",
            "Status": "OK",
            "amount": -60.0,
            "currency": "RUB",
            "Payment amount": -60.0,
            "Payment currency": "RUB",
            "Cashback": "NaN",
            "Category": "Duty Free",
            "MCC": 5309.0,
            "Description": "Regstaer-M Dtp",
            "Bonuses": 1,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 60.0,
        },
        {
            "Date_operation": "13.02.2019 14:25:11",
            "Payment_date": "15.02.2019",
            "Card_numbers": "*7197",
            "Status": "OK",
            "amount": -127.0,
            "currency": "RUB",
            "Payment amount": -127.0,
            "Payment currency": "RUB",
            "Cashback": "NaN",
            "Category": "Искусство",
            "MCC": 5973.0,
            "Description": "Utvar",
            "Bonuses": 2,
            "Rounding_investment_bank": 0,
            "Amount_rounding_operation": 127.0,
        },
    ]


@pytest.fixture
def currencies():
    return {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
