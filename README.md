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