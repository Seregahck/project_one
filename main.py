from src.masks import get_mask_account, get_mask_card_number


def main() -> None:
    card_number = "7000792289606361"
    account_number = "73654108430135874305"

    masked_card = get_mask_card_number(card_number)
    masked_account = get_mask_account(account_number)

    print(f"Card: {masked_card}")
    print(f"Account: {masked_account}")


if __name__ == "__main__":
    main()
