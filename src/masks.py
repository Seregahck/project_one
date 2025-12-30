def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты в формате XXXX XX** **** XXXX"""
    cleaned_number = card_number.replace(" ", "")
    if not cleaned_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен состоять из 16 цифр.")
    part1 = cleaned_number[:4]
    part2 = cleaned_number[4:6]
    part3 = "**"
    part4 = "****"
    part5 = cleaned_number[-4:]
    return f"{part1} {part2}{part3} {part4} {part5}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета в формате **XXXX"""
    cleaned_number = account_number.replace(" ", "")
    if not cleaned_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")
    if len(cleaned_number) < 4:
        raise ValueError("Номер счета должен быть длиной не менее 4 цифр")
    return f"**{cleaned_number[-4:]}"

