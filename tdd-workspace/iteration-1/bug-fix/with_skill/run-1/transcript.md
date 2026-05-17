# TDD Bug Fix Transcript — Discount Double-Application Bug

## Task

Fix a bug where `apply_discount(price, vip=True, code='SAVE10')` applies a 10% discount twice (returning 81.0) instead of once (expected 90.0).

---

## Step 0 — Build the Test List

Before writing any code, I identified the test cases needed to prove the requirement:

1. **No discount** — `apply_discount(100.0)` → `100.0` (baseline)
2. **VIP only** — `apply_discount(100.0, vip=True)` → `90.0` (10% off)
3. **SAVE10 code only** — `apply_discount(100.0, code='SAVE10')` → `90.0` (10% off)
4. **Wrong code, no VIP** — `apply_discount(100.0, code='OTHER')` → `100.0` (no discount)
5. **Both VIP + SAVE10** — `apply_discount(100.0, vip=True, code='SAVE10')` → `90.0` (**the bug**: currently returns 81.0)

---

## Step 1 — RED: Write the Buggy Implementation and Failing Test

### Buggy `discount.py`

```python
def apply_discount(price: float, vip: bool = False, code: str = "") -> float:
    """Apply discount to a price. VIP gets 10% off. Code 'SAVE10' gets 10% off."""
    if vip:
        price = price * 0.9
    if code == "SAVE10":
        price = price * 0.9  # Bug: this applies again even when vip=True already applied it
    return round(price, 2)
```

### `test_discount.py` with reproducing test

```python
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
```

### Test run — CONFIRMS FAILURE

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
collected 5 items

test_discount.py::test_no_discount PASSED                                                                        [ 20%]
test_discount.py::test_vip_discount_only PASSED                                                                  [ 40%]
test_discount.py::test_save10_code_only PASSED                                                                   [ 60%]
test_discount.py::test_no_vip_wrong_code PASSED                                                                  [ 80%]
test_discount.py::test_vip_and_save10_code_discount_not_stacked FAILED                                           [100%]

======================================================= FAILURES =======================================================
____________________________________ test_vip_and_save10_code_discount_not_stacked _____________________________________

    def test_vip_and_save10_code_discount_not_stacked():
        result = apply_discount(100.0, vip=True, code="SAVE10")
>       assert result == 90.0, (
            f"Expected 90.0 (10% off applied once), but got {result}. "
            "Bug: discount is being applied twice when both vip and code are supplied."
        )
E       AssertionError: Expected 90.0 (10% off applied once), but got 81.0. Bug: discount is being applied twice when both vip and code are supplied.
E       assert 81.0 == 90.0

test_discount.py:27: AssertionError
=============================================== short test summary info ================================================
FAILED test_discount.py::test_vip_and_save10_code_discount_not_stacked - AssertionError: Expected 90.0 (10% off applied once), but got 81.0.
============================================= 1 failed, 4 passed in 0.06s ==============================================
```

**The reproducing test fails as expected.** The buggy code applies the 0.9 multiplier twice: once for `vip=True` and once for `code='SAVE10'`, yielding `100 * 0.9 * 0.9 = 81.0` instead of `90.0`.

---

## Step 2 — GREEN: Apply the Minimal Fix

The fix combines both conditions with `or` so the discount is applied at most once, regardless of which condition(s) trigger it.

### Fixed `discount.py`

```python
def apply_discount(price: float, vip: bool = False, code: str = "") -> float:
    """Apply discount to a price. VIP gets 10% off. Code 'SAVE10' gets 10% off.
    If both are supplied, the discount is only applied once."""
    if vip or code == "SAVE10":
        price = price * 0.9
    return round(price, 2)
```

**Change made:** Replaced two separate `if` blocks with a single `if vip or code == "SAVE10"` condition. This ensures the 10% discount is applied at most once.

### Test run after fix — ALL PASS

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
collected 5 items

test_discount.py::test_no_discount PASSED                                                                        [ 20%]
test_discount.py::test_vip_discount_only PASSED                                                                  [ 40%]
test_discount.py::test_save10_code_only PASSED                                                                   [ 60%]
test_discount.py::test_no_vip_wrong_code PASSED                                                                  [ 80%]
test_discount.py::test_vip_and_save10_code_discount_not_stacked PASSED                                           [100%]

================================================== 5 passed in 0.01s ===================================================
```

✅ All 5 tests pass.

---

## Step 3 — REFACTOR

No refactoring needed. The fix is clean and minimal — a single `if/or` condition is clearer and more correct than two sequential `if` blocks that each apply a discount independently.

---

## Summary

| Step | Action | Result |
|------|--------|--------|
| Step 0 | Built test list of 5 cases | Identified the stacking bug case |
| Step 1 (RED) | Wrote `test_vip_and_save10_code_discount_not_stacked` | **FAILED** — got 81.0, expected 90.0 |
| Step 2 (GREEN) | Changed two `if` blocks to `if vip or code == "SAVE10"` | **All 5 tests PASS** |
| Step 3 (REFACTOR) | No changes needed | — |
