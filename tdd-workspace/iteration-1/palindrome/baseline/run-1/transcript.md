# Palindrome TDD – Transcript

## Approach

Used TDD: wrote tests first, verified they failed (import error), then implemented the function.

## Step 1 – Write tests (`test_palindrome.py`)

Wrote 12 tests covering:
- Simple palindrome / non-palindrome
- Case insensitivity (`"Racecar"`)
- Spaces (`"A man a plan a canal Panama"`)
- Punctuation (`"Was it a car or a cat I saw?"`)
- Empty string, single char, two chars
- Numeric palindrome (`"12321"`)
- Mixed alphanumeric (`"A1B2B1A"`)
- Non-palindrome with punctuation

## Step 2 – Red phase

Running `pytest` before any implementation produced:

```
ModuleNotFoundError: No module named 'palindrome'
```

Tests correctly failed.

## Step 3 – Implement (`palindrome.py`)

```python
def is_palindrome(s: str) -> bool:
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
```

Strategy: strip non-alphanumeric chars, lowercase, compare to its reverse.

## Step 4 – Green phase

```
12 passed in 0.01s
```

All tests passed on the first implementation attempt.
