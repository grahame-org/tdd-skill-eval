# TDD Bug-Fix Transcript

## Task

Bug: `calculate_discount` applies a 10% discount twice when both `vip=True` and `code='SAVE10'` are supplied.

---

## Baseline — 3 existing tests passing

```
$ python -m pytest test_discount.py -v

test_discount.py::test_no_discount_for_regular_customer PASSED
test_discount.py::test_vip_gets_10_percent_discount PASSED
test_discount.py::test_save10_code_gets_10_percent_discount PASSED

3 passed in 0.01s
```

---

## Step 1 — RED: Write the failing reproducing test

Added to `test_discount.py`:

```python
def test_vip_and_save10_discount_applied_once():
    # vip=True + code='SAVE10' should give only 10% off (not 20%)
    assert calculate_discount(100, vip=True, code='SAVE10') == 90.0
```

```
$ python -m pytest test_discount.py -v

test_discount.py::test_no_discount_for_regular_customer PASSED
test_discount.py::test_vip_gets_10_percent_discount PASSED
test_discount.py::test_save10_code_gets_10_percent_discount PASSED
test_discount.py::test_vip_and_save10_discount_applied_once FAILED

FAILED test_discount.py::test_vip_and_save10_discount_applied_once
  AssertionError: assert 80.0 == 90.0
   +  where 80.0 = calculate_discount(100, vip=True, code='SAVE10')

1 failed, 3 passed in 0.04s
```

✅ Bug confirmed — double discount produces 80.0 instead of expected 90.0.

---

## Step 2 — GREEN: Minimal fix

Changed the two independent `if` blocks into `if / elif` so that `SAVE10` only applies when the customer is **not** already a VIP:

```python
# Before (buggy)
if vip:
    discount += 0.10

if code == 'SAVE10':
    discount += 0.10

# After (fixed)
if vip:
    discount += 0.10
elif code == 'SAVE10':
    discount += 0.10
```

```
$ python -m pytest test_discount.py -v

test_discount.py::test_no_discount_for_regular_customer PASSED
test_discount.py::test_vip_gets_10_percent_discount PASSED
test_discount.py::test_save10_code_gets_10_percent_discount PASSED
test_discount.py::test_vip_and_save10_discount_applied_once PASSED

4 passed in 0.01s
```

✅ All 4 tests green.

---

## Step 3 — REFACTOR

No refactoring required. The fix is minimal and the code is already clear.
