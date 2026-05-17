def is_palindrome(s):
    normalized = "".join(c for c in s.lower() if c.isalnum())
    return normalized == normalized[::-1]
