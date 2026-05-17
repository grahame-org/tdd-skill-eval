# TDD Transcript — Sum of a List of Integers

## Step 0 — Build the Test List

Before writing any code, the test cases were listed from simplest to most complex:

1. **Empty list** → should return `0`
2. **Single element** → should return that element
3. **Multiple elements** → should return the sum of all elements

---

## Cycle 1: Empty List

### Step 1 — RED: Write the first failing test

**test_sum_list.py**
```python
from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0
```

**Test run output:**
```
================================================= test session starts ==================================================
collecting ... collected 0 items / 1 error

ERROR collecting test_sum_list.py
ImportError: No module named 'sum_list'
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
=================================================== 1 error in 0.11s ===================================================
```

✅ Test is failing (module does not exist) — RED confirmed.

### Step 2 — GREEN: Write the minimum code (return constant 0)

**sum_list.py** — Transformation: *return a constant*
```python
def sum_list(lst):
    return 0
```

**Test run output:**
```
================================================= test session starts ==================================================
collected 1 item

test_sum_list.py::test_empty_list_returns_zero PASSED                                                            [100%]

================================================== 1 passed in 0.01s ===================================================
```

✅ GREEN — implementation is deliberately just `return 0`.

### Step 3 — REFACTOR

No refactoring needed at this stage.

---

## Cycle 2: Single Element

### Step 1 — RED: Write the next failing test

**test_sum_list.py** (updated)
```python
from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0

def test_single_element_returns_that_element():
    assert sum_list([5]) == 5
```

**Test run output:**
```
================================================= test session starts ==================================================
collected 2 items

test_sum_list.py::test_empty_list_returns_zero PASSED                                                            [ 50%]
test_sum_list.py::test_single_element_returns_that_element FAILED                                                [100%]

FAILURES
assert 0 == 5
 +  where 0 = sum_list([5])

============================================= 1 failed, 1 passed in 0.05s =============================================
```

✅ RED confirmed — `return 0` cannot pass the single-element test.

### Step 2 — GREEN: Use a variable (return lst[0])

**sum_list.py** — Transformation: *use a variable*
```python
def sum_list(lst):
    if not lst:
        return 0
    return lst[0]
```

**Test run output:**
```
================================================= test session starts ==================================================
collected 2 items

test_sum_list.py::test_empty_list_returns_zero PASSED                                                            [ 50%]
test_sum_list.py::test_single_element_returns_that_element PASSED                                                [100%]

================================================== 2 passed in 0.01s ===================================================
```

✅ GREEN — both tests pass.

### Step 3 — REFACTOR

No refactoring needed.

---

## Cycle 3: Multiple Elements

### Step 1 — RED: Write the next failing test

**test_sum_list.py** (updated)
```python
from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0

def test_single_element_returns_that_element():
    assert sum_list([5]) == 5

def test_multiple_elements_returns_sum():
    assert sum_list([1, 2, 3]) == 6
```

**Test run output:**
```
================================================= test session starts ==================================================
collected 3 items

test_sum_list.py::test_empty_list_returns_zero PASSED                                                            [ 33%]
test_sum_list.py::test_single_element_returns_that_element PASSED                                                [ 66%]
test_sum_list.py::test_multiple_elements_returns_sum FAILED                                                      [100%]

FAILURES
assert 1 == 6
 +  where 1 = sum_list([1, 2, 3])

============================================= 1 failed, 2 passed in 0.06s =============================================
```

✅ RED confirmed — `return lst[0]` returns only the first element.

### Step 2 — GREEN: Introduce iteration

**sum_list.py** — Transformation: *add iteration*
```python
def sum_list(lst):
    total = 0
    for n in lst:
        total += n
    return total
```

**Test run output:**
```
================================================= test session starts ==================================================
collected 3 items

test_sum_list.py::test_empty_list_returns_zero PASSED                                                            [ 33%]
test_sum_list.py::test_single_element_returns_that_element PASSED                                                [ 66%]
test_sum_list.py::test_multiple_elements_returns_sum PASSED                                                      [100%]

================================================== 3 passed in 0.01s ===================================================
```

✅ GREEN — all 3 tests pass.

### Step 3 — REFACTOR

The loop-based implementation is already clean and readable. The explicit `total = 0` accumulator correctly handles the empty-list case (loop body never executes), eliminating the need for the `if not lst` guard. No further refactoring required.

---

## Summary of Transformation Steps

| Cycle | Failing test              | Implementation                            | Transformation           |
|-------|---------------------------|-------------------------------------------|--------------------------|
| 1     | `sum_list([]) == 0`       | `return 0`                                | Return a constant        |
| 2     | `sum_list([5]) == 5`      | `if not lst: return 0; return lst[0]`     | Use a variable           |
| 3     | `sum_list([1,2,3]) == 6`  | accumulator loop                          | Add iteration            |

## Final Files

**sum_list.py**
```python
def sum_list(lst):
    total = 0
    for n in lst:
        total += n
    return total
```

**test_sum_list.py**
```python
from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0

def test_single_element_returns_that_element():
    assert sum_list([5]) == 5

def test_multiple_elements_returns_sum():
    assert sum_list([1, 2, 3]) == 6
```
