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
