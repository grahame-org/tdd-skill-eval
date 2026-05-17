import pytest
from palindrome import is_palindrome


def test_simple_palindrome():
    assert is_palindrome("racecar") is True


def test_simple_non_palindrome():
    assert is_palindrome("hello") is False


def test_case_insensitive():
    assert is_palindrome("Racecar") is True


def test_with_spaces():
    assert is_palindrome("A man a plan a canal Panama") is True


def test_with_punctuation():
    assert is_palindrome("Was it a car or a cat I saw?") is True


def test_empty_string():
    assert is_palindrome("") is True


def test_single_character():
    assert is_palindrome("a") is True


def test_two_same_characters():
    assert is_palindrome("aa") is True


def test_two_different_characters():
    assert is_palindrome("ab") is False


def test_numbers():
    assert is_palindrome("12321") is True


def test_mixed_alphanumeric():
    assert is_palindrome("A1B2B1A") is True


def test_non_palindrome_with_punctuation():
    assert is_palindrome("Hello, World!") is False
