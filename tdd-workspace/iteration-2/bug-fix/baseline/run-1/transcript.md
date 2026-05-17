# TDD Bug Fix Transcript

## Bug Description

`calculate_discount` applied the 10% discount twice when both `vip=True` and
`code='SAVE10'` were supplied, resulting in a 20% total discount instead of 10%.

---

## Step 1 — Red: Write a failing test

Added to `test_discount.py`:

```python
def test_vip_with_save10_code_gets_only_10_percent_discount():
    # Bug: discount is applied twice (20% total) instead of once (10%)
    assert calculate_discount(100, vip=True, code='SAVE10') == 90.0
```

### Test output (failing)

```
FAILED test_discount.py::test_vip_with_save10_code_gets_only_10_percent_discount
AssertionError: assert 80.0 == 90.0
 +  where 80.0 = calculate_discount(100, vip=True, code='SAVE10')

1 failed, 3 passed in 0.05s
```

The test fails with `80.0` (20% discount applied) instead of the expected `90.0`
(10% discount). The bug is confirmed.

---

## Step 2 — Green: Fix the implementation

**Root cause:** The original code accumulated `discount` additively for each
condition, so both `vip` and `code == 'SAVE10'` each added 0.10, giving 0.20 total.

**Fix:** Replace additive accumulation with a single conditional — any qualifying
condition grants exactly 10% discount:

```python
# Before (buggy)
discount = 0.0
if vip:
    discount += 0.10
if code == 'SAVE10':
    discount += 0.10

# After (fixed)
if vip or code == 'SAVE10':
    discount = 0.10
else:
    discount = 0.0
```

### Test output (passing)

```
test_discount.py::test_no_discount_for_regular_customer PASSED
test_discount.py::test_vip_gets_10_percent_discount PASSED
test_discount.py::test_save10_code_gets_10_percent_discount PASSED
test_discount.py::test_vip_with_save10_code_gets_only_10_percent_discount PASSED

4 passed in 0.01s
```

---

## Summary

| Phase | Tests | Result |
|-------|-------|--------|
| Red   | 4     | 1 failed (reproducing test) |
| Green | 4     | 4 passed (after fix) |
