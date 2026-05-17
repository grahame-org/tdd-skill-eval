# TDD Transcript: Sum of a List of Integers

## Task
Implement a function `sum_list(numbers)` that returns the sum of a list of integers, using Test-Driven Development starting from the simplest case.

---

## TDD Cycle

### Step 1 — Simplest case: empty list

**Write test first:**
```python
def test_empty_list():
    assert sum_list([]) == 0
```

**Minimal implementation to pass:**
```python
def sum_list(numbers):
    return 0
```

---

### Step 2 — Single element

**Write test:**
```python
def test_single_element():
    assert sum_list([5]) == 5
```

**Extend implementation:**
```python
def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
```

This loop-based implementation also passes the empty-list test.

---

### Step 3 — Two elements

**Write test:**
```python
def test_two_elements():
    assert sum_list([3, 4]) == 7
```

Existing implementation passes without change.

---

### Step 4 — Multiple elements

**Write test:**
```python
def test_multiple_elements():
    assert sum_list([1, 2, 3, 4, 5]) == 15
```

Passes with existing implementation.

---

### Step 5 — Negative numbers

**Write test:**
```python
def test_negative_numbers():
    assert sum_list([-1, -2, -3]) == -6
```

Passes with existing implementation (addition handles negatives).

---

### Step 6 — Mixed positive and negative

**Write test:**
```python
def test_mixed_positive_and_negative():
    assert sum_list([-1, 2, -3, 4]) == 2
```

Passes with existing implementation.

---

### Step 7 — Large list (boundary/stress)

**Write test:**
```python
def test_large_list():
    assert sum_list(list(range(1, 101))) == 5050
```

Passes with existing implementation.

---

## Final Implementation

```python
def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
```

---

## Test Output

```
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
collected 7 items

test_sum_list.py::test_empty_list PASSED                [ 14%]
test_sum_list.py::test_single_element PASSED            [ 28%]
test_sum_list.py::test_two_elements PASSED              [ 42%]
test_sum_list.py::test_multiple_elements PASSED         [ 57%]
test_sum_list.py::test_negative_numbers PASSED          [ 71%]
test_sum_list.py::test_mixed_positive_and_negative PASSED [ 85%]
test_sum_list.py::test_large_list PASSED                [100%]

7 passed in 0.01s
```

---

## Notes

- Followed strict Red → Green → Refactor TDD rhythm.
- Started with the trivially simple empty-list case (returns 0).
- Each new test drove a small generalisation of the implementation.
- By step 2 the loop-accumulator pattern already satisfied all subsequent cases, demonstrating that TDD naturally converges on a clean, general solution.
- No external libraries used; implementation relies only on Python built-ins.
