# FizzBuzz TDD Implementation Transcript

## Approach

I used a classic Red-Green-Refactor TDD cycle:
1. Write a failing test
2. Write the minimal implementation to make it pass
3. Refactor if needed, keeping tests green

## Test Cases Written

Tests were written before the implementation, covering all four behaviours:

| Test | Reason |
|------|--------|
| `test_returns_number_as_string` (n=1) | Base case — non-divisible number returns string of that number |
| `test_returns_fizz_for_multiple_of_3` (n=3) | Smallest multiple of 3 |
| `test_returns_buzz_for_multiple_of_5` (n=5) | Smallest multiple of 5 |
| `test_returns_fizzbuzz_for_multiple_of_15` (n=15) | Smallest common multiple — must return "FizzBuzz" |
| `test_returns_fizz_for_6` | Second multiple of 3, confirms rule isn't just for n=3 |
| `test_returns_buzz_for_10` | Second multiple of 5, confirms rule isn't just for n=5 |
| `test_returns_fizzbuzz_for_30` | Second multiple of 15, confirms FizzBuzz rule generalises |
| `test_returns_number_as_string_for_2` | Another plain number |
| `test_returns_number_as_string_for_7` | Another plain number |

## Order of Writing

1. **Tests first** — all tests written in `test_fizzbuzz.py` before any implementation
2. **Implementation second** — `fizzbuzz.py` written to satisfy all tests

The implementation checks `n % 15 == 0` first to avoid the FizzBuzz case being masked by the Fizz or Buzz checks, then checks each divisor independently, and falls back to `str(n)`.

## Final Test Run Output

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
collected 9 items

test_fizzbuzz.py::test_returns_number_as_string PASSED                                                           [ 11%]
test_fizzbuzz.py::test_returns_fizz_for_multiple_of_3 PASSED                                                     [ 22%]
test_fizzbuzz.py::test_returns_buzz_for_multiple_of_5 PASSED                                                     [ 33%]
test_fizzbuzz.py::test_returns_fizzbuzz_for_multiple_of_15 PASSED                                                [ 44%]
test_fizzbuzz.py::test_returns_fizz_for_6 PASSED                                                                 [ 55%]
test_fizzbuzz.py::test_returns_buzz_for_10 PASSED                                                                [ 66%]
test_fizzbuzz.py::test_returns_fizzbuzz_for_30 PASSED                                                            [ 77%]
test_fizzbuzz.py::test_returns_number_as_string_for_2 PASSED                                                     [ 88%]
test_fizzbuzz.py::test_returns_number_as_string_for_7 PASSED                                                     [100%]

================================================== 9 passed in 0.02s ===================================================
```
