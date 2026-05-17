import pytest
from discount import apply_discount


# Basic tests (should pass with both buggy and fixed code)
def test_no_discount():
    assert apply_discount(100.0) == 100.0


def test_vip_discount_only():
    assert apply_discount(100.0, vip=True) == 90.0


def test_save10_code_only():
    assert apply_discount(100.0, code="SAVE10") == 90.0


def test_no_vip_wrong_code():
    assert apply_discount(100.0, code="OTHER") == 100.0


# Reproducing test for the bug:
# When both vip=True and code='SAVE10' are supplied, discount should only
# be applied once (10% total → 90.0), not twice (19% total → 81.0).
def test_vip_and_save10_code_discount_not_stacked():
    result = apply_discount(100.0, vip=True, code="SAVE10")
    assert result == 90.0, (
        f"Expected 90.0 (10% off applied once), but got {result}. "
        "Bug: discount is being applied twice when both vip and code are supplied."
    )
