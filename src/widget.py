from datetime import datetime


def mask_account_card(info_string: str) -> str:
    """
    Маскирует номер карты или счета в строке.
    """
    parts = info_string.split()

    if not parts:
        return ""

    account_type = " ".join(parts[:-1])
    number = parts[-1]

    if account_type.lower() == "счет":
        if len(number) >= 4:
            masked_number = "**" + number[-4:]
        else:
            masked_number = number
        return f"{account_type} {masked_number}"
    else:
        if len(number) == 16 and number.isdigit():
            masked_number = f"{number[:4]} {number[4:6]}** **** {number[-4:]}"
        else:
            masked_number = number
        return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.
    """
    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))

        return dt.strftime("%d.%m.%Y")
    except (ValueError, AttributeError):
        return ""
