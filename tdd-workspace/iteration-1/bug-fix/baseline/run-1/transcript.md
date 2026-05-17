# Bug Fix Transcript

## Task
Fix a double-discount bug in `apply_discount`: when both `vip=True` and `code='SAVE10'` are supplied, a 10% discount was applied twice, returning 81.0 instead of the expected 90.0.

## Steps

### 1. Created buggy `discount.py`
The original implementation used two independent `if` statements, so both conditions could trigger separately:

```python
def apply_discount(price: float, vip: bool = False, code: str = "") -> float:
    if vip:
        price = price * 0.9
    if code == "SAVE10":
        price = price * 0.9  # Bug: applies again even when vip already applied it
    return round(price, 2)
```

### 2. Wrote `test_discount.py` (TDD – test first)
Added `test_vip_and_code_only_one_discount` to reproduce the bug before fixing it:

```python
def test_vip_and_code_only_one_discount():
    result = apply_discount(100, vip=True, code="SAVE10")
    assert result == 90.0, f"Expected 90.0 but got {result} (double discount bug)"
```

Running tests confirmed the failure:
```
FAILED test_discount.py::test_vip_and_code_only_one_discount
AssertionError: Expected 90.0 but got 81.0 (double discount bug)
```

### 3. Fixed the bug
Merged the two conditions with `or` so the discount is applied at most once:

```python
def apply_discount(price: float, vip: bool = False, code: str = "") -> float:
    if vip or code == "SAVE10":
        price = price * 0.9
    return round(price, 2)
```

### 4. Verified all tests pass
```
5 passed in 0.01s
```

## Result
- `apply_discount(100, vip=True, code='SAVE10')` now correctly returns `90.0`.
- All existing behaviour (no discount, vip-only, code-only, unrecognised code) is preserved.
