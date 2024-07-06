# -*- coding: utf-8 -*-
import json
import unittest
from io import StringIO
from unittest.mock import mock_open, patch

import pandas as pd
from src.reports import spending_category


class TestSpendingCategoryFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.transactions = pd.DataFrame(
            {
                "date_operation": ["2020-01-01", "2020-02-01", "2020-03-01"],
                "category": ["Супермаркеты", "Супермаркеты", "Развлечения"],
                "transaction_amount": [150, 300, 70],
            }
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file_decorator(self, mock_open_file) -> None:
        spending_category(self.transactions, "Супермаркеты", "2020-03-31")

        mock_open_file.assert_called_with("spending_report.txt", "w")
        handle = mock_open_file()

        expected_data = [
            {"date_operation": "2020-01-01", "transaction_amount": 150},
            {"date_operation": "2020-02-01", "transaction_amount": 300},
        ]

        written_json = handle.write.call_args[0][0]
        self.assertEqual(json.loads(written_json), expected_data)

    def test_spending_category_output(self) -> None:
        result = spending_category(self.transactions, "Супермаркеты", "2020-03-31")
        expected_data = [
            {"date_operation": "2020-01-01", "transaction_amount": 150},
            {"date_operation": "2020-02-01", "transaction_amount": 300},
        ]
        self.assertEqual(json.loads(result), expected_data)

    def test_spending_category_results(self) -> None:
        result = spending_category(self.transactions, "Супермаркеты", "2020-03-31")
        result_df = pd.read_json(StringIO(result), orient="records")

        self.assertEqual(result_df.shape[0], 2)  # ожидаем две строки
        self.assertEqual(result_df.iloc[0]["date_operation"], "2020-01-01")
        self.assertEqual(result_df.iloc[0]["transaction_amount"], 150)
        self.assertEqual(result_df.iloc[1]["date_operation"], "2020-02-01")
        self.assertEqual(result_df.iloc[1]["transaction_amount"], 300)
