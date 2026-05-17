# TDD FizzBuzz Transcript

## Step 0 — Test List

Before writing any code, the following test cases were identified, ordered from simplest to most complex:

1. Returns the number as a string for 1 (trivial non-multiple)
2. Returns the number as a string for 2 (second non-multiple, forces generalisation from constant)
3. Returns 'Fizz' for 3 (first multiple of 3)
4. Returns 'Buzz' for 5 (first multiple of 5)
5. Returns 'Fizz' for 6 (another multiple of 3 — triangulation)
6. Returns 'Buzz' for 10 (another multiple of 5 — triangulation)
7. Returns 'FizzBuzz' for 15 (multiple of both 3 and 5)
8. Returns 'FizzBuzz' for 30 (another multiple of both — triangulation)

---

## Cycle 1 — Returns number as string for 1

### RED

**Test written:**
```python
def test_returns_number_as_string_for_1():
    assert fizzbuzz(1) == "1"
```

**Run output (FAIL — module not found):**
```
ERROR test_fizzbuzz.py
ModuleNotFoundError: No module named 'fizzbuzz'
```
Test fails as expected — no production code exists yet.

### GREEN

**Minimum code — return a constant:**
```python
def fizzbuzz(n):
    return "1"
```

**Run output:**
```
test_fizzbuzz.py::test_returns_number_as_string_for_1 PASSED
1 passed in 0.01s
```
Returning the constant `"1"` is sufficient to pass this single test.

### REFACTOR
No duplication or clarity issues at this stage. Nothing to refactor.

---

## Cycle 2 — Returns number as string for 2

### RED

**Test written:**
```python
def test_returns_number_as_string_for_2():
    assert fizzbuzz(2) == "2"
```

**Run output (FAIL):**
```
FAILED test_fizzbuzz.py::test_returns_number_as_string_for_2
AssertionError: assert '1' == '2'
1 failed, 1 passed
```
Fails as expected — the constant `"1"` doesn't satisfy `fizzbuzz(2)`.

### GREEN

**Minimum code — use a variable (str conversion):**
```python
def fizzbuzz(n):
    return str(n)
```

Moving up the transformation ladder from "return constant" to "use a variable" — `str(n)` generalises over any number.

**Run output:**
```
test_fizzbuzz.py::test_returns_number_as_string_for_1 PASSED
test_fizzbuzz.py::test_returns_number_as_string_for_2 PASSED
2 passed in 0.01s
```

### REFACTOR
Nothing to refactor yet.

---

## Cycle 3 — Returns 'Fizz' for 3

### RED

**Test written:**
```python
def test_returns_fizz_for_3():
    assert fizzbuzz(3) == "Fizz"
```

**Run output (FAIL):**
```
FAILED test_fizzbuzz.py::test_returns_fizz_for_3
AssertionError: assert '3' == 'Fizz'
1 failed, 2 passed
```

### GREEN

**Minimum code — add a conditional:**
```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)
```

Moving up the ladder to "add a conditional".

**Run output:**
```
test_fizzbuzz.py::test_returns_number_as_string_for_1 PASSED
test_fizzbuzz.py::test_returns_number_as_string_for_2 PASSED
test_fizzbuzz.py::test_returns_fizz_for_3 PASSED
3 passed in 0.01s
```

### REFACTOR
No duplication. Nothing to refactor.

---

## Cycle 4 — Returns 'Buzz' for 5

### RED

**Test written:**
```python
def test_returns_buzz_for_5():
    assert fizzbuzz(5) == "Buzz"
```

**Run output (FAIL):**
```
FAILED test_fizzbuzz.py::test_returns_buzz_for_5
AssertionError: assert '5' == 'Buzz'
1 failed, 3 passed
```

### GREEN

**Minimum code — add another conditional:**
```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

**Run output:**
```
test_fizzbuzz.py::test_returns_number_as_string_for_1 PASSED
test_fizzbuzz.py::test_returns_number_as_string_for_2 PASSED
test_fizzbuzz.py::test_returns_fizz_for_3 PASSED
test_fizzbuzz.py::test_returns_buzz_for_5 PASSED
4 passed in 0.01s
```

### REFACTOR
No duplication. Nothing to refactor.

---

## Cycles 5 & 6 — Triangulation for Fizz (6) and Buzz (10)

These tests were written to verify the general modulo logic works for more than just the first example of each case (triangulation):

```python
def test_returns_fizz_for_6():
    assert fizzbuzz(6) == "Fizz"

def test_returns_buzz_for_10():
    assert fizzbuzz(10) == "Buzz"
```

Both passed immediately with the existing implementation — no code changes needed.

**Run output:**
```
6 passed in 0.01s
```

---

## Cycle 7 — Returns 'FizzBuzz' for 15

### RED

**Test written:**
```python
def test_returns_fizzbuzz_for_15():
    assert fizzbuzz(15) == "FizzBuzz"
```

**Run output (FAIL):**
```
FAILED test_fizzbuzz.py::test_returns_fizzbuzz_for_15
AssertionError: assert 'Fizz' == 'FizzBuzz'
1 failed, 6 passed
```
15 hits the `n % 3 == 0` branch first and returns `"Fizz"` instead of `"FizzBuzz"`.

### GREEN

**Minimum code — add FizzBuzz check before Fizz/Buzz:**
```python
def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

The combined condition must be checked first.

**Run output:**
```
7 passed in 0.01s
```

### REFACTOR
No structural duplication. Nothing to refactor yet.

---

## Cycle 8 — Triangulation: FizzBuzz for 30

**Test written:**
```python
def test_returns_fizzbuzz_for_30():
    assert fizzbuzz(30) == "FizzBuzz"
```

Passed immediately — no code changes needed.

**Run output:**
```
8 passed in 0.02s
```

---

## Final Refactor

With all tests green and the test list exhausted, a clarity improvement was made:

`n % 3 == 0 and n % 5 == 0` is equivalent to `n % 15 == 0`, which is more concise and expresses the intent directly.

**Before:**
```python
if n % 3 == 0 and n % 5 == 0:
    return "FizzBuzz"
```

**After:**
```python
if n % 15 == 0:
    return "FizzBuzz"
```

**Run output after refactor:**
```
test_fizzbuzz.py::test_returns_number_as_string_for_1 PASSED
test_fizzbuzz.py::test_returns_number_as_string_for_2 PASSED
test_fizzbuzz.py::test_returns_fizz_for_3 PASSED
test_fizzbuzz.py::test_returns_buzz_for_5 PASSED
test_fizzbuzz.py::test_returns_fizz_for_6 PASSED
test_fizzbuzz.py::test_returns_buzz_for_10 PASSED
test_fizzbuzz.py::test_returns_fizzbuzz_for_15 PASSED
test_fizzbuzz.py::test_returns_fizzbuzz_for_30 PASSED
8 passed in 0.01s
```

All tests pass. Test list is empty.

---

## Final Files

### fizzbuzz.py
```python
def fizzbuzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

### test_fizzbuzz.py
```python
# TODO Test List:
# 1. Returns the number as a string for 1 (trivial, non-multiple)
# 2. Returns the number as a string for 2
# 3. Returns 'Fizz' for 3 (multiple of 3)
# 4. Returns 'Buzz' for 5 (multiple of 5)
# 5. Returns 'Fizz' for 6 (another multiple of 3)
# 6. Returns 'Buzz' for 10 (another multiple of 5)
# 7. Returns 'FizzBuzz' for 15 (multiple of both 3 and 5)
# 8. Returns 'FizzBuzz' for 30 (another multiple of both)

import pytest
from fizzbuzz import fizzbuzz

def test_returns_number_as_string_for_1():
    assert fizzbuzz(1) == "1"

def test_returns_number_as_string_for_2():
    assert fizzbuzz(2) == "2"

def test_returns_fizz_for_3():
    assert fizzbuzz(3) == "Fizz"

def test_returns_buzz_for_5():
    assert fizzbuzz(5) == "Buzz"

def test_returns_fizz_for_6():
    assert fizzbuzz(6) == "Fizz"

def test_returns_buzz_for_10():
    assert fizzbuzz(10) == "Buzz"

def test_returns_fizzbuzz_for_15():
    assert fizzbuzz(15) == "FizzBuzz"

def test_returns_fizzbuzz_for_30():
    assert fizzbuzz(30) == "FizzBuzz"
```
