# Обработчик банковских операций

## Модуль для фильтрации и сортировки банковских транзакций. Модуль содержит две основные функции: filter_by_state для фильтрации операций по статусу и sort_by_date для сортировки операций по дате.

## Установка:
1. Клонируйте репозиторий:
```
 [GitHub] https://github.com/Seregahck/project_one.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование:

from processing import filter_by_state, sort_by_date

# Тестовые данные
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

## Описание тестируемых функций
# 1. get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты в формате "XXXX XX** **** XXXX"

Тесты:

test_get_mask_card_number_valid - валидные номера карт

test_get_mask_card_number_invalid - невалидные номера

test_get_mask_card_number_with_spaces - номера с пробелами

# 2. get_mask_account(account_number: str) -> str
Маскирует номер банковского счета в формате "**XXXX"

Тесты:

test_get_mask_account_valid - валидные номера счетов

test_get_mask_account_invalid - невалидные номера

test_get_mask_account_with_spaces - номера с пробелами

# 3. mask_account_card(text: str) -> str
Определяет тип номера (карта или счет) и маскирует его

Тесты:

test_mask_account_card_card - строки с номерами карт

test_mask_account_card_account - строки с номерами счетов

test_mask_account_card_edge_cases - крайние случаи

# 4. get_date(date_str: str) -> str
Преобразует дату из формата ISO в формат "DD.MM.YYYY"

Тесты:

test_get_date_valid - валидные даты

test_get_date_invalid - невалидные даты

# 5. filter_by_state(transactions: List[Dict], state: str = "EXECUTED") -> List[Dict]
Фильтрует список транзакций по статусу

Тесты:

test_filter_by_state_basic - базовый тест фильтрации

test_filter_by_state_default - тест значения по умолчанию

test_filter_by_state_all_executed - все транзакции EXECUTED

test_filter_by_state_pending - фильтрация PENDING

test_filter_by_state_empty - пустой список

test_filter_by_state_single - одна транзакция

test_filter_by_state_parametrized - параметризованный тест

# 6. sort_by_date(transactions: List[Dict], reverse: bool = True) -> List[Dict]
Сортирует транзакции по дате

Тесты:

test_sort_by_date_descending - сортировка по убыванию

test_sort_by_date_ascending - сортировка по возрастанию

test_sort_by_date_chronological - хронологический порядок

test_sort_by_date_same_date - одинаковые даты

test_sort_by_date_empty - пустой список

test_sort_by_date_single - одна транзакция

test_sort_by_date_parametrized - параметризованный тест

Фикстуры
В файле tests/conftest.py определены фикстуры для тестов:

Для тестов маскирования:
valid_card_numbers - валидные номера карт

invalid_card_numbers - невалидные номера карт

valid_account_numbers - валидные номера счетов

invalid_account_numbers - невалидные номера счетов

card_strings - строки с картами

account_strings - строки со счетами

Для тестов дат:
valid_dates - валидные даты

invalid_dates - невалидные даты

Для тестов транзакций:
sample_transactions - образец транзакций

executed_transactions - только EXECUTED

pending_transactions - только PENDING

empty_transactions - пустой список

single_transaction - одна транзакция

dated_transactions - транзакции с датами

chronological_transactions - хронологический порядок

same_date_transactions - одинаковые даты