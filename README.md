# ������  "���������� ��� ������� ����������"

## ��������:
���������� ����� ������������ JSON-������ ��� ���-�������, 
����������� Excel-������, � ����� ������������� ������ �������.

## ������ views.py:
��������� ����� ������� � ������� �������, ����������� �� ���� ������ � ����� � �������� � ������� 
YYYY-MM-DD HH:MM:SS � ������������ JSON-����� �� ���������� �������:

1. ����������� � �������"???", ��� ??? � ������� ���� / ������� ����� / ������� ����� / ������� ���� � ����������� �� �������� �������.
2. �� ������ �����:
- ��������� 4 ����� �����;
- ����� ����� ��������;
- ������ (1 ����� �� ������ 100 ������).
3. ���-5 ���������� �� ����� �������.
4. ���� �����.
5. ��������� ����� �� S&P500.
- `main`

## ������ utils.py:

�������� ����� ������� ��� ������ "�������" ��������.
- `read_transactions_exel`
- `filter_data_range`
- `get_greeting`
- `get_response_greeting`
- `get_card_data`
- `get_top_transactions`
- `get_currency_rates`
- `get_stock_price`

## ������ reports.py:
���������� ����� �� �������� ��������� �� ��������� ��� ������ (�� ���������� ����).
- `spending_category`

## ������ services.py:

�������� �������, ������� ���������� JSON �� ����� ������������, ����������� � �������� ��������� ������.
- `find_transactions_with_phone_numbers`
- `contains_phone_number`

## ���������:
1. ���������� �����������.
```
git@github.com:MaxKuvshinov/CourseWork1.git
```
2. ���������� ����������� (��� ��������� ������������ ������������ Poetry):
```
poetry install
```
3. ����������� ����������� ���������:
```
poetry shell
```

## ������������:
��� ����������� �������� � ���������� ���� ����� ��������� ��������� ����� � �������������� pytest. 
����-����� ����� ��������� ��������� ���������� �� ������������ �� ������.

## ��������� ������������ ��� ������������:
���������, ��� �� ���������� � �������������� ����������� ��������� Poetry. ����� ���������� ����������� ��� ������������:
```
poetry add --group dev pytest
```

## ������ ������:
��� ������� ������ ��������� ��������� ������� � �������� �������� �������:
���������, ��� �� ���������� � �������������� ����������� ��������� Poetry. ����� ���������� ����������� ��� ������������:
```
pytest
```
## ��������� ������:
� ������� ����� ����� tests, ���������� ����� ��� ��������� �����������.

## �������� �������:
```
Name                     Stmts   Miss  Cover
--------------------------------------------
src\__init__.py              0      0   100%
src\api_config.py           26      0   100%
src\reports.py              39      3    92%
src\services.py             22      0   100%
src\utils.py               141     19    87%
src\views.py                29      0   100%
tests\__init__.py            0      0   100%
tests\conftest.py           13      3    77%
tests\test_reports.py       29      0   100%
tests\test_services.py      18      0   100%
tests\test_utils.py         99      0   100%
tests\test_views.py         34      0   100%
--------------------------------------------
TOTAL                      450     25    94%
```

## ��������: �������� ������

## ��������:
 ���� ������ ������������ �� [�������� MIT](https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F_MIT).