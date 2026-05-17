from palindrome import is_palindrome

def test_empty_string_is_palindrome():
    assert is_palindrome("") is True

def test_single_character_is_palindrome():
    assert is_palindrome("a") is True

def test_simple_palindrome_is_palindrome():
    assert is_palindrome("aba") is True

def test_simple_non_palindrome_is_not_palindrome():
    assert is_palindrome("abc") is False

def test_mixed_case_palindrome_is_palindrome():
    assert is_palindrome("Aba") is True

def test_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
