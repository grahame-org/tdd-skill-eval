# FizzBuzz TDD Transcript

## Test List

Before writing any code I identified the cases to cover:

1. A plain number (not divisible by 3 or 5) → return that number as a string
2. A multiple of 3 → return "Fizz"
3. A multiple of 5 → return "Buzz"
4. A multiple of both 3 and 5 → return "FizzBuzz"

Additional confirming tests:
- Another multiple of 3 (9)
- Another multiple of 5 (10)
- Another multiple of both (30)
- Another plain number (7)

---

## Cycle 1 — Plain number returns string

### Test written

```python
def test_returns_number_as_string_for_1():
    assert fizzbuzz(1) == "1"
```

### Implementation (stub)

```python
def fizzbuzz(n):
    pass
```

### Test output (RED)

```
FAILED test_fizzbuzz.py::test_returns_number_as_string_for_1
AssertionError: assert None == '1'
```

### Implementation (green)

```python
def fizzbuzz(n):
    return str(n)
```

### Test output (GREEN)

```
1 passed in 0.00s
```

---

## Cycle 2 — Multiples of 3 return "Fizz"

### Test written

```python
def test_returns_fizz_for_multiple_of_3():
    assert fizzbuzz(3) == "Fizz"
```

### Test output (RED)

```
FAILED test_fizzbuzz.py::test_returns_fizz_for_multiple_of_3
AssertionError: assert '3' == 'Fizz'
```

### Implementation (green)

```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)
```

### Test output (GREEN)

```
2 passed in 0.01s
```

---

## Cycle 3 — Multiples of 5 return "Buzz"

### Test written

```python
def test_returns_buzz_for_multiple_of_5():
    assert fizzbuzz(5) == "Buzz"
```

### Test output (RED)

```
FAILED test_fizzbuzz.py::test_returns_buzz_for_multiple_of_5
AssertionError: assert '5' == 'Buzz'
```

### Implementation (green)

```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

### Test output (GREEN)

```
3 passed in 0.01s
```

---

## Cycle 4 — Multiples of both 3 and 5 return "FizzBuzz"

### Test written

```python
def test_returns_fizzbuzz_for_multiple_of_3_and_5():
    assert fizzbuzz(15) == "FizzBuzz"
```

### Test output (RED)

```
FAILED test_fizzbuzz.py::test_returns_fizzbuzz_for_multiple_of_3_and_5
AssertionError: assert 'Fizz' == 'FizzBuzz'
```

The bug: the `n % 3 == 0` branch fires before we check for multiples of both.

### Implementation (green)

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

### Test output (GREEN)

```
4 passed in 0.01s
```

---

## Confirming tests added (no new failures expected)

Added:
- `test_returns_fizz_for_another_multiple_of_3` → fizzbuzz(9) == "Fizz"
- `test_returns_buzz_for_another_multiple_of_5` → fizzbuzz(10) == "Buzz"
- `test_returns_fizzbuzz_for_30` → fizzbuzz(30) == "FizzBuzz"
- `test_returns_number_as_string_for_non_multiple` → fizzbuzz(7) == "7"

### Final test output

```
platform linux -- Python 3.12.13, pytest-9.0.3

test_fizzbuzz.py::test_returns_number_as_string_for_1                   PASSED
test_fizzbuzz.py::test_returns_fizz_for_multiple_of_3                   PASSED
test_fizzbuzz.py::test_returns_buzz_for_multiple_of_5                   PASSED
test_fizzbuzz.py::test_returns_fizzbuzz_for_multiple_of_3_and_5         PASSED
test_fizzbuzz.py::test_returns_fizz_for_another_multiple_of_3           PASSED
test_fizzbuzz.py::test_returns_buzz_for_another_multiple_of_5           PASSED
test_fizzbuzz.py::test_returns_fizzbuzz_for_30                          PASSED
test_fizzbuzz.py::test_returns_number_as_string_for_non_multiple        PASSED

8 passed in 0.01s
```

---

## Final Implementation

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

## Observations

- TDD forced the FizzBuzz case to be discovered explicitly — the naive ordering (check 3 first) produced a failing test for 15, making the bug visible immediately.
- Each cycle was: write one failing test → write minimal code → green → add next test.
