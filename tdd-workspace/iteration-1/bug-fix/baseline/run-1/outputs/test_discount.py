import pytest
from discount import apply_discount


def test_no_discount():
    assert apply_discount(100) == 100.0


def test_vip_discount():
    assert apply_discount(100, vip=True) == 90.0


def test_code_discount():
    assert apply_discount(100, code="SAVE10") == 90.0


def test_vip_and_code_only_one_discount():
    # Bug reproduction: both vip=True and code='SAVE10' should apply only one 10% discount
    result = apply_discount(100, vip=True, code="SAVE10")
    assert result == 90.0, f"Expected 90.0 but got {result} (double discount bug)"


def test_unrecognised_code():
    assert apply_discount(100, code="OTHER") == 100.0
