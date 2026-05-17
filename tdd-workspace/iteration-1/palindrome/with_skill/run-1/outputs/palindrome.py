def is_palindrome(s):
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    return normalized == normalized[::-1]
