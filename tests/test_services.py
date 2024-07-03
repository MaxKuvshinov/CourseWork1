# -*- coding: utf-8 -*-
import json
import unittest

from src.services import find_transactions_with_phone_numbers


class TestFindTransactionsWithPhoneNumbers(unittest.TestCase):

    def setUp(self) -> None:
        # Пример данных для тестирования
        self.data = [
            {"description": "Я МТС +7 921 11-22-33"},
            {"description": "Тинькофф Мобайл +7 995 555-55-55"},
            {"description": "МТС Mobile +7 981 333-44-55"},
        ]

    def test_find_transactions_with_phone_numbers(self) -> None:
        result = find_transactions_with_phone_numbers(self.data)
        expected_result = [
            {"description": "Тинькофф Мобайл +7 995 555-55-55"},
            {"description": "МТС Mobile +7 981 333-44-55"},
        ]
        self.assertEqual(result, json.dumps(expected_result, ensure_ascii=False, indent=4))

    def test_find_transactions_with_phone_numbers_empty(self) -> None:
        result = find_transactions_with_phone_numbers([])
        self.assertEqual(result, "[]")

    def test_find_transactions_with_phone_numbers_no_matches(self) -> None:
        data_no_matches = [
            {"description": "Без номера телефона"},
            {"description": "Неправильный формат +7 123-45-67"},
            {"description": "Еще один без номера телефона"},
        ]
        result = find_transactions_with_phone_numbers(data_no_matches)
        self.assertEqual(result, "[]")
