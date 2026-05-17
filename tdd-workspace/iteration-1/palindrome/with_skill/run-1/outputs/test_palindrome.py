# test_palindrome.py - TDD tests for palindrome function
from palindrome import is_palindrome

# TEST 1 (RED): empty string should return True
def test_empty_string():
    assert is_palindrome("") == True

# TEST 2 (RED): single character should return True
def test_single_character():
    assert is_palindrome("a") == True

# TEST 3 (RED): simple non-palindrome should return False
def test_simple_non_palindrome():
    assert is_palindrome("hello") == False

# TEST 4 (RED): simple palindrome "racecar" should return True
def test_simple_palindrome():
    assert is_palindrome("racecar") == True

# TEST 5 (RED): mixed-case palindrome "Racecar" should return True
def test_mixed_case_palindrome():
    assert is_palindrome("Racecar") == True

# TEST 6 (RED): palindrome with spaces should return True
def test_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama") == True

# TEST 7 (RED): palindrome with punctuation should return True
def test_palindrome_with_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") == True
