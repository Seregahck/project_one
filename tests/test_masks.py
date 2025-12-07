import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"


def test_get_mask_card_number_with_spaces() -> None:
    assert get_mask_card_number("7000 7922 8960 6361") == "7000 79** **** 6361"


def test_get_mask_card_number_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("1234")
    with pytest.raises(ValueError):
        get_mask_card_number("12345678901234567890")
    with pytest.raises(ValueError):
        get_mask_card_number("1234abcd56789012")


def test_get_mask_account() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"
    assert get_mask_account("1234567890") == "**7890"


def test_get_mask_account_with_spaces() -> None:
    assert get_mask_account("7365 4108 4301 3587 4305") == "**4305"


def test_get_mask_account_invalid() -> None:
    with pytest.raises(ValueError):
        get_mask_account("123")
    with pytest.raises(ValueError):
        get_mask_account("12ab34")
