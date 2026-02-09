
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
