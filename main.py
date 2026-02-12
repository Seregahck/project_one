
# from src.masks import get_mask_account, get_mask_card_number
#
#
# def main() -> None:
#     card_number = "7000792289606361"
#     account_number = "73654108430135874305"
#
#     masked_card = get_mask_card_number(card_number)
#     masked_account = get_mask_account(account_number)
#
#     print(f"Card: {masked_card}")
#     print(f"Account: {masked_account}")
#
#
# if __name__ == "__main__":
#     main()

# from src.utils import load_transactions
# from src.external_api import get_transaction_amount_in_rub
#
#
# def main():
#     # Загружаем транзакции
#     transactions = load_transactions('data/operations.json')
#
#     print(f"Загружено транзакций: {len(transactions)}")
#
#     # Обрабатываем каждую транзакцию
#     for i, transaction in enumerate(transactions[:5], 1):  # Первые 5 для примера
#         try:
#             amount_rub = get_transaction_amount_in_rub(transaction)
#             currency = transaction.get('currency', 'N/A')
#             original_amount = transaction.get('amount', 'N/A')
#
#             print(f"Транзакция {i}:")
#             print(f"  Исходная сумма: {original_amount} {currency}")
#             print(f"  В рублях: {amount_rub:.2f} RUB")
#             print("-" * 30)
#
#         except Exception as e:
#             print(f"Ошибка обработки транзакции {i}: {e}")
#
#
# if __name__ == "__main__":
#     main()
import os
from typing import List, Dict
from src.operations import (
    load_json_transactions,
    filter_by_status,
    sort_transactions,
    filter_rub_transactions,
    process_bank_search,
    process_bank_operations,
    format_transaction
)


def get_user_choice(prompt: str, valid_choices: List[str]) -> str:
    """
    Получает выбор пользователя с проверкой.

    Args:
        prompt: Подсказка для пользователя
        valid_choices: Допустимые варианты

    Returns:
        Выбор пользователя
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Некорректный ввод. Допустимые варианты: {', '.join(valid_choices)}")


def get_file_choice() -> str:
    """
    Получает выбор типа файла от пользователя.

    Returns:
        Выбор пользователя
    """
    print("\n" + "="*80)
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    print("="*80)

    return get_user_choice("Ваш выбор (1-3): ", ["1", "2", "3"])


def get_status_from_user() -> str:
    """
    Получает статус операций от пользователя.

    Returns:
        Статус операций
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        print("\n" + "="*80)
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")

        status = input("Ваш выбор: ").strip().upper()

        if status in valid_statuses:
            print(f"Операции отфильтрованы по статусу '{status}'")
            return status
        else:
            print(f"Статус операции '{status}' недоступен.")


def get_sort_preferences() -> bool:
    """
    Получает предпочтения по сортировке от пользователя.

    Returns:
        True если сортировать по убыванию, False если по возрастанию
    """
    print("\n" + "="*80)
    sort_choice = get_user_choice(
        "Отсортировать операции по дате? Да/Нет: ",
        ["Да", "да", "Нет", "нет"]
    )

    if sort_choice.lower() == "да":
        direction = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (возрастанию/убыванию): ",
            ["возрастанию", "убыванию"]
        )
        return direction == "убыванию"

    return False


def main() -> None:
    """
    Основная функция программы с пользовательским интерфейсом.
    """
    # Выбор типа файла
    file_choice = get_file_choice()

    if file_choice == "1":
        print("Для обработки выбран JSON-файл.")
        filename = "data/transactions.json"
        if not os.path.exists(filename):
            print(f"Файл {filename} не найден.")
            return
        transactions = load_json_transactions(filename)
    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.")
        print("Реализация чтения CSV файлов требует дополнительных модулей.")
        return
    else:  # file_choice == "3"
        print("Для обработки выбран XLSX-файл.")
        print("Реализация чтения XLSX файлов требует дополнительных модулей.")
        return

    if not transactions:
        print("Не удалось загрузить транзакции.")
        return

    print(f"Загружено транзакций: {len(transactions)}")

    # Фильтрация по статусу
    status = get_status_from_user()
    filtered_transactions = filter_by_status(transactions, status)

    if not filtered_transactions:
        print(f"Нет транзакций со статусом '{status}'")
        return

    # Сортировка
    reverse_sort = get_sort_preferences()
    if reverse_sort is not None:
        filtered_transactions = sort_transactions(filtered_transactions, reverse_sort)

    # Фильтрация по валюте
    print("\n" + "="*80)
    rub_choice = get_user_choice(
        "Выводить только рублевые транзакции? Да/Нет: ",
        ["Да", "да", "Нет", "нет"]
    )

    if rub_choice.lower() == "да":
        filtered_transactions = filter_rub_transactions(filtered_transactions)

    # Поиск по описанию
    print("\n" + "="*80)
    search_choice = get_user_choice(
        "Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ",
        ["Да", "да", "Нет", "нет"]
    )

    if search_choice.lower() == "да":
        search_string = input("Введите слово или выражение для поиска в описании: ").strip()
        if search_string:
            filtered_transactions = process_bank_search(filtered_transactions, search_string)

    # Вывод результатов
    print("\n" + "="*80)
    print("Распечатываю итоговый список транзакций...")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(filtered_transactions)}\n")

    for transaction in filtered_transactions:
        print(format_transaction(transaction))

    # Дополнительный анализ по категориям
    print("\n" + "="*80)
    analyze_choice = get_user_choice(
        "Выполнить анализ операций по категориям? Да/Нет: ",
        ["Да", "да", "Нет", "нет"]
    )

    if analyze_choice.lower() == "да":
        # Получаем уникальные категории из отфильтрованных транзакций
        categories = list(set(
            t.get('description', '') for t in filtered_transactions
            if t.get('description')
        ))

        if categories:
            counts = process_bank_operations(filtered_transactions, categories)
            print("\nКоличество операций по категориям:")
            print("-" * 40)
            for category, count in sorted(counts.items()):
                if count > 0:
                    print(f"{category}: {count}")
        else:
            print("Нет категорий для анализа.")

    print("\n" + "="*80)
    print("Работа программы завершена. Спасибо!")


if __name__ == "__main__":
    main()