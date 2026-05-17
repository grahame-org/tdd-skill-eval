import pytest
from fizzbuzz import fizzbuzz


def test_returns_number_as_string():
    assert fizzbuzz(1) == "1"


def test_returns_fizz_for_multiple_of_3():
    assert fizzbuzz(3) == "Fizz"


def test_returns_buzz_for_multiple_of_5():
    assert fizzbuzz(5) == "Buzz"


def test_returns_fizzbuzz_for_multiple_of_15():
    assert fizzbuzz(15) == "FizzBuzz"


def test_returns_fizz_for_6():
    assert fizzbuzz(6) == "Fizz"


def test_returns_buzz_for_10():
    assert fizzbuzz(10) == "Buzz"


def test_returns_fizzbuzz_for_30():
    assert fizzbuzz(30) == "FizzBuzz"


def test_returns_number_as_string_for_2():
    assert fizzbuzz(2) == "2"


def test_returns_number_as_string_for_7():
    assert fizzbuzz(7) == "7"
