import pytest
from palindrome import is_palindrome


# RED: basic palindrome
def test_simple_palindrome():
    assert is_palindrome("racecar") is True


def test_simple_non_palindrome():
    assert is_palindrome("hello") is False


# RED: case insensitive
def test_case_insensitive():
    assert is_palindrome("Racecar") is True
    assert is_palindrome("MadAm") is True


# RED: ignore non-alphanumeric
def test_ignore_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_ignore_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("Was it a car or a cat I saw?") is True


# RED: edge cases
def test_empty_string():
    assert is_palindrome("") is True


def test_single_character():
    assert is_palindrome("a") is True


def test_two_same_chars():
    assert is_palindrome("aa") is True


def test_two_different_chars():
    assert is_palindrome("ab") is False


def test_numbers():
    assert is_palindrome("12321") is True
    assert is_palindrome("12345") is False


def test_mixed_alphanum():
    assert is_palindrome("A1B2B1A") is True  # alphanum only: a1b2b1a
