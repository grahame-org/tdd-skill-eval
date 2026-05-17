# TDD Palindrome Implementation – Transcript

## Task
Implement `is_palindrome(s)` using TDD: returns `True` if the string is a palindrome, ignoring case and non-alphanumeric characters.

---

## Step 1 – RED: Write failing tests first

Created `test_palindrome.py` covering:
- Simple palindrome / non-palindrome
- Case insensitivity (`"Racecar"`, `"MadAm"`)
- Ignoring spaces (`"A man a plan a canal Panama"`)
- Ignoring punctuation (`"A man, a plan, a canal: Panama"`)
- Edge cases: empty string, single char, two chars, numeric strings, mixed alphanumeric

**Test run (no implementation):**
```
ERROR collecting test_palindrome.py
ModuleNotFoundError: No module named 'palindrome'
```
✅ Tests fail as expected — RED phase confirmed.

---

## Step 2 – GREEN: Minimal implementation

Created `palindrome.py`:
```python
def is_palindrome(s: str) -> bool:
    filtered = [c.lower() for c in s if c.isalnum()]
    return filtered == filtered[::-1]
```

**Test run:**
```
11 passed in 0.01s
```
✅ All tests pass — GREEN phase confirmed.

---

## Step 3 – REFACTOR

The implementation is already minimal and readable. No refactoring needed:
- Single list comprehension filters and lowercases in one pass
- Comparison with reversed list is idiomatic Python
- No logic duplication

---

## Summary

| Phase | Outcome |
|-------|---------|
| RED   | Import error (module not found) — tests correctly failed |
| GREEN | 11/11 tests pass |
| REFACTOR | No changes needed; implementation is clean |

**Final implementation:** strip non-alphanumeric, lowercase, compare with reverse.
