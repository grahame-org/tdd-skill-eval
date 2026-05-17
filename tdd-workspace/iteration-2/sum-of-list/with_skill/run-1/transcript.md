# TDD Transcript — Sum of a List of Integers

## Step 0 — Test List

### Forcing Tests
| # | Test | Why it forces new behaviour |
|---|------|-----------------------------|
| 1 | empty list → 0 | Forces the function to exist and return something defined |
| 2 | single element [5] → 5 | Forces the implementation to look at list contents |
| 3 | multiple elements [1,2,3] → 6 | Forces accumulation over all elements (iteration) |

### Triangulation Tests (not driving production code)
- `[2, 3] → 5` — second multi-element case, confirms no accidental hard-coding of 6
- `[-1, 1] → 0` — negative numbers handled by same logic

---

## Cycle 1 — Empty list

### RED
**Test written:**
```python
def test_empty_list_returns_zero():
    assert sum_list([]) == 0
```

**Failure output:**
```
FAILED test_sum.py::test_empty_list_returns_zero - NameError: name 'sum_list' is not defined
```
Fails for the right reason: function does not exist.

### GREEN — TPP step 1: return constant
```python
def sum_list(lst):
    return 0
```

**Pass output:**
```
test_sum.py::test_empty_list_returns_zero PASSED   [100%]
1 passed in 0.00s
```

### REFACTOR
No duplication or complexity to address. `sum()` is not applicable yet — there is no loop to replace.

---

## Cycle 2 — Single element

### RED
**Test written:**
```python
def test_single_element_returns_that_element():
    assert sum_list([5]) == 5
```

**Failure output:**
```
FAILED test_sum.py::test_single_element_returns_that_element - assert 0 == 5
1 failed, 1 passed
```
Fails for the right reason: constant `0` is wrong for a non-empty list.

### GREEN — TPP step 3: add conditional + direct access (no loop)
```python
def sum_list(lst):
    if not lst:
        return 0
    return lst[0]
```

**Pass output:**
```
test_sum.py::test_empty_list_returns_zero PASSED
test_sum.py::test_single_element_returns_that_element PASSED
2 passed in 0.01s
```

### REFACTOR
Still no loop present. `sum()` is not applicable. No other duplication to remove.

---

## Cycle 3 — Multiple elements

### RED
**Test written:**
```python
def test_multiple_elements_returns_their_sum():
    assert sum_list([1, 2, 3]) == 6
```

**Failure output:**
```
FAILED test_sum.py::test_multiple_elements_returns_their_sum - assert 1 == 6
1 failed, 2 passed
```
Fails for the right reason: returning only `lst[0]` gives 1, not 6.

### GREEN — TPP step 4: introduce iteration
```python
def sum_list(lst):
    total = 0
    for n in lst:
        total += n
    return total
```

**Pass output:**
```
test_sum.py::test_empty_list_returns_zero PASSED
test_sum.py::test_single_element_returns_that_element PASSED
test_sum.py::test_multiple_elements_returns_their_sum PASSED
3 passed in 0.01s
```

### REFACTOR — Replace hand-written loop with `sum()`

**Consideration:** The hand-written `total = 0; for n in lst: total += n; return total` is exactly what Python's built-in `sum()` does. `sum([])` returns `0` (correct), `sum([5])` returns `5` (correct), `sum([1,2,3])` returns `6` (correct). Replacing with `sum()` removes the explicit loop, reduces surface area for bugs, and expresses intent more clearly.

**Refactored implementation:**
```python
def sum_list(lst):
    return sum(lst)
```

**Pass output after refactor:**
```
test_sum.py::test_empty_list_returns_zero PASSED
test_sum.py::test_single_element_returns_that_element PASSED
test_sum.py::test_multiple_elements_returns_their_sum PASSED
3 passed in 0.01s
```

All behaviour unchanged. Refactor complete.

---

## Final State

**`sum_list.py`:**
```python
def sum_list(lst):
    return sum(lst)
```

**`test_sum.py`:**
```python
from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0

def test_single_element_returns_that_element():
    assert sum_list([5]) == 5

def test_multiple_elements_returns_their_sum():
    assert sum_list([1, 2, 3]) == 6
```

**TPP progression followed:**
1. `return 0` — constant (Cycle 1 GREEN)
2. `if not lst: return 0; return lst[0]` — conditional + variable (Cycle 2 GREEN)
3. `for n in lst: total += n` — iteration (Cycle 3 GREEN)
4. `return sum(lst)` — built-in replaces loop (Cycle 3 REFACTOR)
