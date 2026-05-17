from fizzbuzz import fizzbuzz


def test_returns_number_as_string_for_1():
    assert fizzbuzz(1) == "1"


def test_returns_fizz_for_multiple_of_3():
    assert fizzbuzz(3) == "Fizz"


def test_returns_buzz_for_multiple_of_5():
    assert fizzbuzz(5) == "Buzz"


def test_returns_fizzbuzz_for_multiple_of_3_and_5():
    assert fizzbuzz(15) == "FizzBuzz"


def test_returns_fizz_for_another_multiple_of_3():
    assert fizzbuzz(9) == "Fizz"


def test_returns_buzz_for_another_multiple_of_5():
    assert fizzbuzz(10) == "Buzz"


def test_returns_fizzbuzz_for_30():
    assert fizzbuzz(30) == "FizzBuzz"


def test_returns_number_as_string_for_non_multiple():
    assert fizzbuzz(7) == "7"
