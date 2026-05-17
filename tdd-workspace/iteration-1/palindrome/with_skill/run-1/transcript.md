# TDD Transcript: Palindrome Function

## Step 0 — Test List

Before writing any code, the following test cases were identified to cover all required behaviours:

1. **Empty string** — `""` → `True` (trivially a palindrome)
2. **Single character** — `"a"` → `True` (single char reads same forwards/backwards)
3. **Simple palindrome** — `"racecar"` → `True`
4. **Simple non-palindrome** — `"hello"` → `False`
5. **Mixed-case palindrome** — `"Racecar"` → `True` (case is ignored)
6. **Palindrome with spaces** — `"a man a plan a canal panama"` → `True` (non-alphanumeric ignored)
7. **Palindrome with punctuation** — `"A man, a plan, a canal: Panama"` → `True` (punctuation ignored)

---

## RED 1 — Empty string

**Test added:**
```python
def test_empty_string():
    assert is_palindrome("") == True
```

**`palindrome.py` state:** empty (no `is_palindrome` defined)

**Test output:**
```
collected 0 items / 1 error

ERROR collecting test_palindrome.py
ImportError: cannot import name 'is_palindrome' from 'palindrome'

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
1 error in 0.10s
```

✅ RED confirmed — ImportError, test cannot even run.

---

## GREEN 1 — Empty string

**`palindrome.py`:**
```python
def is_palindrome(s):
    return True
```
*Minimum code: stub that always returns True.*

**Test output:**
```
test_palindrome.py::test_empty_string PASSED     [100%]

1 passed in 0.01s
```

✅ GREEN — 1/1 tests passing.

---

## RED 2 — Single character

**Test added:**
```python
def test_single_character():
    assert is_palindrome("a") == True
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED          [ 50%]
test_palindrome.py::test_single_character PASSED      [100%]

2 passed in 0.01s
```

📝 Note: This test passes immediately — a single character is a palindrome and the stub returns `True`. No code change required; we proceed to the next test that will force a real failure.

---

## RED 3 — Simple non-palindrome

**Test added:**
```python
def test_simple_non_palindrome():
    assert is_palindrome("hello") == False
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED               [ 33%]
test_palindrome.py::test_single_character PASSED           [ 66%]
test_palindrome.py::test_simple_non_palindrome FAILED      [100%]

FAILURES
AssertionError: assert True == False
  where True = is_palindrome('hello')

1 failed, 2 passed in 0.05s
```

✅ RED confirmed — stub returns `True` for everything; `"hello"` should be `False`.

---

## GREEN 3 — Simple non-palindrome

**`palindrome.py`:**
```python
def is_palindrome(s):
    return s == s[::-1]
```
*Reverse comparison: the simplest real check.*

**Test output:**
```
test_palindrome.py::test_empty_string PASSED               [ 33%]
test_palindrome.py::test_single_character PASSED           [ 66%]
test_palindrome.py::test_simple_non_palindrome PASSED      [100%]

3 passed in 0.01s
```

✅ GREEN — 3/3 tests passing.

---

## RED 4 — Simple palindrome "racecar"

**Test added:**
```python
def test_simple_palindrome():
    assert is_palindrome("racecar") == True
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED          [ 25%]
test_palindrome.py::test_single_character PASSED      [ 50%]
test_palindrome.py::test_simple_non_palindrome PASSED [ 75%]
test_palindrome.py::test_simple_palindrome PASSED     [100%]

4 passed in 0.01s
```

📝 Note: Passes immediately — `"racecar" == "racecar"[::-1]` is `True`. Current implementation already handles this case; we proceed to the next forcing test.

---

## RED 5 — Mixed-case palindrome

**Test added:**
```python
def test_mixed_case_palindrome():
    assert is_palindrome("Racecar") == True
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED               [ 20%]
test_palindrome.py::test_single_character PASSED           [ 40%]
test_palindrome.py::test_simple_non_palindrome PASSED      [ 60%]
test_palindrome.py::test_simple_palindrome PASSED          [ 80%]
test_palindrome.py::test_mixed_case_palindrome FAILED      [100%]

FAILURES
AssertionError: assert False == True
  where False = is_palindrome('Racecar')

1 failed, 4 passed in 0.06s
```

✅ RED confirmed — `"Racecar" != "racecaR"` (case-sensitive reverse fails).

---

## GREEN 5 — Mixed-case palindrome

**`palindrome.py`:**
```python
def is_palindrome(s):
    normalized = s.lower()
    return normalized == normalized[::-1]
```
*Lowercase the string before comparing.*

**Test output:**
```
test_palindrome.py::test_empty_string PASSED               [ 20%]
test_palindrome.py::test_single_character PASSED           [ 40%]
test_palindrome.py::test_simple_non_palindrome PASSED      [ 60%]
test_palindrome.py::test_simple_palindrome PASSED          [ 80%]
test_palindrome.py::test_mixed_case_palindrome PASSED      [100%]

5 passed in 0.01s
```

✅ GREEN — 5/5 tests passing.

---

## RED 6 — Palindrome with spaces

**Test added:**
```python
def test_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama") == True
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED                 [ 16%]
test_palindrome.py::test_single_character PASSED             [ 33%]
test_palindrome.py::test_simple_non_palindrome PASSED        [ 50%]
test_palindrome.py::test_simple_palindrome PASSED            [ 66%]
test_palindrome.py::test_mixed_case_palindrome PASSED        [ 83%]
test_palindrome.py::test_palindrome_with_spaces FAILED       [100%]

FAILURES
AssertionError: assert False == True
  where False = is_palindrome('a man a plan a canal panama')

1 failed, 5 passed in 0.06s
```

✅ RED confirmed — spaces break the reversal comparison.

---

## GREEN 6 — Palindrome with spaces

**`palindrome.py`:**
```python
def is_palindrome(s):
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    return normalized == normalized[::-1]
```
*Filter to alphanumeric only, then lowercase before comparing.*

**Test output:**
```
test_palindrome.py::test_empty_string PASSED                 [ 16%]
test_palindrome.py::test_single_character PASSED             [ 33%]
test_palindrome.py::test_simple_non_palindrome PASSED        [ 50%]
test_palindrome.py::test_simple_palindrome PASSED            [ 66%]
test_palindrome.py::test_mixed_case_palindrome PASSED        [ 83%]
test_palindrome.py::test_palindrome_with_spaces PASSED       [100%]

6 passed in 0.01s
```

✅ GREEN — 6/6 tests passing.

---

## RED 7 — Palindrome with punctuation

**Test added:**
```python
def test_palindrome_with_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") == True
```

**Test output:**
```
test_palindrome.py::test_empty_string PASSED                   [ 14%]
test_palindrome.py::test_single_character PASSED               [ 28%]
test_palindrome.py::test_simple_non_palindrome PASSED          [ 42%]
test_palindrome.py::test_simple_palindrome PASSED              [ 57%]
test_palindrome.py::test_mixed_case_palindrome PASSED          [ 71%]
test_palindrome.py::test_palindrome_with_spaces PASSED         [ 85%]
test_palindrome.py::test_palindrome_with_punctuation PASSED    [100%]

7 passed in 0.01s
```

📝 Note: Passes immediately — the `c.isalnum()` filter introduced in GREEN 6 strips both spaces and punctuation. No code change needed.

✅ GREEN — 7/7 tests passing.

---

## REFACTOR

After reviewing the final implementation:

```python
def is_palindrome(s):
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    return normalized == normalized[::-1]
```

**Assessment:** No refactoring required.
- The function is concise (2 lines) and clearly expresses intent.
- No duplication exists — normalization (filter + lowercase) and comparison are each done once.
- Variable name `normalized` accurately describes what the value represents.
- The generator expression `c.lower() for c in s if c.isalnum()` combines both transformations in a single pass — efficient and readable.

---

## Final State

### `palindrome.py`
```python
def is_palindrome(s):
    normalized = ''.join(c.lower() for c in s if c.isalnum())
    return normalized == normalized[::-1]
```

### `test_palindrome.py`
```python
from palindrome import is_palindrome

def test_empty_string():
    assert is_palindrome("") == True

def test_single_character():
    assert is_palindrome("a") == True

def test_simple_non_palindrome():
    assert is_palindrome("hello") == False

def test_simple_palindrome():
    assert is_palindrome("racecar") == True

def test_mixed_case_palindrome():
    assert is_palindrome("Racecar") == True

def test_palindrome_with_spaces():
    assert is_palindrome("a man a plan a canal panama") == True

def test_palindrome_with_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") == True
```

### Final test run
```
7 passed in 0.01s
```

---

## TDD Cycle Summary

| # | Test | RED | GREEN | Code Change |
|---|------|-----|-------|-------------|
| 1 | empty string | ImportError | ✅ | Stub: `return True` |
| 2 | single character | Pass immediately | ✅ | No change needed |
| 3 | simple non-palindrome | `True == False` fail | ✅ | `s == s[::-1]` |
| 4 | simple palindrome "racecar" | Pass immediately | ✅ | No change needed |
| 5 | mixed-case "Racecar" | `False == True` fail | ✅ | Added `.lower()` |
| 6 | spaces in palindrome | `False == True` fail | ✅ | Added `isalnum()` filter |
| 7 | punctuation in palindrome | Pass immediately | ✅ | No change needed |
