# TDD Transcript — Palindrome Implementation

## Step 0 — Forcing Tests List

The following forcing tests were identified **before writing any code**. Triangulation tests are NOT listed here — they are added only after their corresponding forcing test passes.

1. Empty string `""` → is palindrome (constant True / trivial)
2. Single character `"a"` → is palindrome
3. Simple palindrome `"aba"` → forces actual comparison logic (via preceding non-palindrome test)
4. Simple non-palindrome `"abc"` → forces the comparison to distinguish True from False
5. Mixed-case palindrome `"Aba"` → forces case folding
6. Palindrome with spaces and punctuation `"A man, a plan, a canal: Panama"` → forces stripping non-alphanumeric characters

---

## Cycle 1 — Empty string

### RED

**Test added:**
```python
def test_empty_string_is_palindrome():
    assert is_palindrome("") is True
```

**`palindrome.py` (before GREEN):** empty file — `is_palindrome` not yet defined.

**Failure output:**
```
ERROR collecting test_palindrome.py
ImportError: cannot import name 'is_palindrome' from 'palindrome'
1 error during collection
```

### GREEN

**Minimum code:**
```python
def is_palindrome(s):
    return True
```

**TPP transformation:** *no code* → constant (`return True`)

**Pass output:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [100%]
1 passed in 0.00s
```

### REFACTOR

No duplication or clarity issues. Nothing to refactor.

---

## Cycle 2 — Single character

### RED

**Test added:**
```python
def test_single_character_is_palindrome():
    assert is_palindrome("a") is True
```

**Run result:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [ 50%]
test_palindrome.py::test_single_character_is_palindrome PASSED [100%]
2 passed in 0.01s
```

**⚠ Test passed immediately without a code change.**  
The specific line that satisfies it: `return True` in `palindrome.py`. A constant `True` is vacuously correct for any "is palindrome" assertion on a trivially-true case.

### GREEN / REFACTOR

No code change needed or made.

---

## Cycle 3 — Simple palindrome "aba"

### RED

**Test added:**
```python
def test_simple_palindrome_is_palindrome():
    assert is_palindrome("aba") is True
```

**Run result:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [ 33%]
test_palindrome.py::test_single_character_is_palindrome PASSED [ 66%]
test_palindrome.py::test_simple_palindrome_is_palindrome PASSED [100%]
3 passed in 0.01s
```

**⚠ Test passed immediately without a code change.**  
The specific line that satisfies it: `return True` in `palindrome.py`. The constant still covers every True-returning case.

### GREEN / REFACTOR

No code change needed or made.

---

## Cycle 4 — Simple non-palindrome "abc"

### RED

**Test added:**
```python
def test_simple_non_palindrome_is_not_palindrome():
    assert is_palindrome("abc") is False
```

**Failure output:**
```
FAILED test_palindrome.py::test_simple_non_palindrome_is_not_palindrome
AssertionError: assert True is False
 +  where True = is_palindrome('abc')
1 failed, 3 passed in 0.04s
```

### GREEN

**Minimum code** — `return True` can no longer satisfy both `"aba"` → True and `"abc"` → False. The simplest transformation that handles both is a string-reversal comparison (TPP: *constant → comparison*):

```python
def is_palindrome(s):
    return s == s[::-1]
```

**Pass output:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [ 25%]
test_palindrome.py::test_single_character_is_palindrome PASSED [ 50%]
test_palindrome.py::test_simple_palindrome_is_palindrome PASSED [ 75%]
test_palindrome.py::test_simple_non_palindrome_is_not_palindrome PASSED [100%]
4 passed in 0.01s
```

### REFACTOR

No duplication. Nothing to refactor.

---

## Cycle 5 — Mixed-case palindrome "Aba"

### RED

**Test added:**
```python
def test_mixed_case_palindrome_is_palindrome():
    assert is_palindrome("Aba") is True
```

**Failure output:**
```
FAILED test_palindrome.py::test_mixed_case_palindrome_is_palindrome
AssertionError: assert False is True
 +  where False = is_palindrome('Aba')
1 failed, 4 passed in 0.05s
```

`"Aba" != "abA"` so the raw reversal fails. Case folding is now required.

### GREEN

**Minimum code** — introduce `.lower()` before comparing (TPP: *comparison → case-folding*):

```python
def is_palindrome(s):
    normalized = s.lower()
    return normalized == normalized[::-1]
```

**Pass output:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [ 20%]
test_palindrome.py::test_single_character_is_palindrome PASSED [ 40%]
test_palindrome.py::test_simple_palindrome_is_palindrome PASSED [ 60%]
test_palindrome.py::test_simple_non_palindrome_is_not_palindrome PASSED [ 80%]
test_palindrome.py::test_mixed_case_palindrome_is_palindrome PASSED [100%]
5 passed in 0.01s
```

### REFACTOR

No duplication. Nothing to refactor.

---

## Cycle 6 — Palindrome with spaces and punctuation

### Note on test case selection

The instructions reference "A man a plan" as the forcing test. However, `"A man a plan"` stripped of non-alphanumerics is `"amanaplan"`, which reversed is `"nalpanama"` — **not** a palindrome. The canonical phrase is `"A man, a plan, a canal: Panama"` → stripped: `"amanaplanacanalpanama"` which **is** a palindrome and correctly exercises both space and punctuation stripping. The test uses the full canonical phrase.

### RED

**Test added:**
```python
def test_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
```

**Failure output (with cycle-5 implementation — lowercase only, no stripping):**
```
FAILED test_palindrome.py::test_palindrome_with_spaces_and_punctuation
AssertionError: assert False is True
 +  where False = is_palindrome('A man, a plan, a canal: Panama')
1 failed, 5 passed in 0.04s
```

Commas, spaces, and colon disrupt the comparison; non-alphanumeric stripping is now required.

### GREEN

**Minimum code** — filter non-alphanumeric characters (TPP: *case-folding → stripping*):

```python
def is_palindrome(s):
    normalized = "".join(c for c in s.lower() if c.isalnum())
    return normalized == normalized[::-1]
```

**Pass output:**
```
test_palindrome.py::test_empty_string_is_palindrome PASSED    [ 16%]
test_palindrome.py::test_single_character_is_palindrome PASSED [ 33%]
test_palindrome.py::test_simple_palindrome_is_palindrome PASSED [ 50%]
test_palindrome.py::test_simple_non_palindrome_is_not_palindrome PASSED [ 66%]
test_palindrome.py::test_mixed_case_palindrome_is_palindrome PASSED [ 83%]
test_palindrome.py::test_palindrome_with_spaces_and_punctuation PASSED [100%]
6 passed in 0.01s
```

### REFACTOR

The `normalized` variable name is clear. The generator expression is idiomatic Python. No duplication. Nothing to refactor.

---

## Final Implementation

```python
def is_palindrome(s):
    normalized = "".join(c for c in s.lower() if c.isalnum())
    return normalized == normalized[::-1]
```

## TPP Transformation Path

| Cycle | Forcing Test | Transformation |
|-------|-------------|----------------|
| 1 | `""` → True | *no code* → constant (`return True`) |
| 2 | `"a"` → True | passes with constant (no change) |
| 3 | `"aba"` → True | passes with constant (no change) |
| 4 | `"abc"` → False | constant → comparison (`s == s[::-1]`) |
| 5 | `"Aba"` → True | comparison → case-folding (`.lower()`) |
| 6 | `"A man, a plan, a canal: Panama"` → True | case-folding → stripping (`.isalnum()` filter) |
