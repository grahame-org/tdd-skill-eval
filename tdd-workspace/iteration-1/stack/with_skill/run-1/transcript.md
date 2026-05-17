# TDD Transcript: Stack Implementation

## Step 0 — Test List

Before writing any code, the following test cases were planned (simplest to most complex):

```
# [x] is_empty on a new stack returns True
# [x] is_empty returns False after push
# [x] push then pop returns the pushed value
# [x] pop on empty stack raises IndexError
# [x] peek returns top element without removing it
# [x] peek after push leaves element on stack (is_empty still False)
# [x] push multiple items, pop returns LIFO order
```

Ordering rationale: start with the degenerate case (empty stack), then add state (push), then verify retrieval (pop), then guard behavior (error), then the non-destructive read (peek), then LIFO correctness with multiple items.

---

## Cycle 1: `is_empty` on new stack returns True

### RED 1

**Test written:**
```python
from stack import Stack

def test_new_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True
```

**Test output (FAIL — no `stack` module):**
```
ERROR test_stack.py - ModuleNotFoundError: No module named 'stack'
```
✅ Confirmed RED.

### GREEN 1

**Minimum implementation:**
```python
class Stack:
    def is_empty(self):
        return True
```
Returned a constant — the simplest transformation on the ladder.

**Test output:**
```
test_stack.py::test_new_stack_is_empty PASSED
1 passed in 0.01s
```
✅ GREEN.

### REFACTOR 1
No refactor needed — code is at its simplest possible form.

---

## Cycle 2: `is_empty` returns False after push

### RED 2

**Test written:**
```python
def test_is_not_empty_after_push():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False
```

**Test output (FAIL):**
```
FAILED test_stack.py::test_is_not_empty_after_push - AttributeError: 'Stack' object has no attribute 'push'
1 failed, 1 passed
```
✅ Confirmed RED.

### GREEN 2

**Minimum implementation** (introduced a collection and real state):
```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def is_empty(self):
        return len(self._items) == 0
```
The constant `return True` was no longer sufficient once `push` existed. Introduced `_items` list and length check.

**Test output:**
```
test_stack.py::test_new_stack_is_empty PASSED
test_stack.py::test_is_not_empty_after_push PASSED
2 passed in 0.01s
```
✅ GREEN.

### REFACTOR 2
No refactor needed.

---

## Cycle 3: push then pop returns the pushed value

### RED 3

**Test written:**
```python
def test_pop_returns_pushed_value():
    s = Stack()
    s.push(42)
    assert s.pop() == 42
```

**Test output (FAIL):**
```
FAILED test_stack.py::test_pop_returns_pushed_value - AttributeError: 'Stack' object has no attribute 'pop'
1 failed, 2 passed
```
✅ Confirmed RED.

### GREEN 3

**Minimum implementation** (add `pop` delegating to list):
```python
def pop(self):
    return self._items.pop()
```

**Test output:**
```
test_stack.py::test_new_stack_is_empty PASSED
test_stack.py::test_is_not_empty_after_push PASSED
test_stack.py::test_pop_returns_pushed_value PASSED
3 passed in 0.01s
```
✅ GREEN.

### REFACTOR 3
No refactor needed.

---

## Cycle 4: pop on empty stack raises IndexError

### RED 4

**Test written:**
```python
def test_pop_empty_stack_raises():
    s = Stack()
    import pytest
    with pytest.raises(IndexError):
        s.pop()
```

**Test output:**
```
test_stack.py::test_pop_empty_stack_raises PASSED
4 passed in 0.01s
```

> **Note:** This test passed immediately (no RED phase). Python's `list.pop()` already raises `IndexError` on an empty list, so the current implementation already satisfies this requirement. The test still has value as regression protection and behavioral documentation.

### GREEN 4
Implementation already correct — no new code needed.

### REFACTOR 4
No refactor needed.

---

## Cycle 5: peek returns top element without removing it

### RED 5

**Test written:**
```python
def test_peek_returns_top_without_removing():
    s = Stack()
    s.push(7)
    assert s.peek() == 7
```

**Test output (FAIL):**
```
FAILED test_stack.py::test_peek_returns_top_without_removing - AttributeError: 'Stack' object has no attribute 'peek'
1 failed, 4 passed
```
✅ Confirmed RED.

### GREEN 5

**Minimum implementation:**
```python
def peek(self):
    return self._items[-1]
```

**Test output:**
```
test_stack.py::test_new_stack_is_empty PASSED
test_stack.py::test_is_not_empty_after_push PASSED
test_stack.py::test_pop_returns_pushed_value PASSED
test_stack.py::test_pop_empty_stack_raises PASSED
test_stack.py::test_peek_returns_top_without_removing PASSED
5 passed in 0.01s
```
✅ GREEN.

### REFACTOR 5
No refactor needed.

---

## Cycle 6: peek leaves element on stack

### RED 6

**Test written:**
```python
def test_peek_does_not_remove_element():
    s = Stack()
    s.push(7)
    s.peek()
    assert s.is_empty() is False
```

**Test output:**
```
6 passed in 0.01s
```

> **Note:** This test also passed immediately. `self._items[-1]` does not modify the list, so the element remains. Test confirms correct non-destructive behavior.

### GREEN 6
Implementation already correct — no new code needed.

### REFACTOR 6
No refactor needed.

---

## Cycle 7: push multiple items, pop returns LIFO order

### RED 7

**Test written:**
```python
def test_lifo_order():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
```

**Test output:**
```
7 passed in 0.02s
```

> **Note:** This test also passed immediately. Python's `list.pop()` removes from the end (LIFO), which is exactly the Stack behavior. The test confirms this fundamental property.

### GREEN 7
Implementation already correct.

### REFACTOR 7

**Refactor applied:** Moved `import pytest` from inside `test_pop_empty_stack_raises` to the top of the file — standard Python import convention.

**Before:**
```python
def test_pop_empty_stack_raises():
    s = Stack()
    import pytest
    with pytest.raises(IndexError):
        s.pop()
```

**After:**
```python
import pytest  # moved to top of file

def test_pop_empty_stack_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()
```

**Test output after refactor:**
```
7 passed in 0.01s
```
✅ All tests still pass.

---

## Final Test Run

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.13, pytest-9.0.3
collected 7 items

test_stack.py::test_new_stack_is_empty PASSED                [ 14%]
test_stack.py::test_is_not_empty_after_push PASSED           [ 28%]
test_stack.py::test_pop_returns_pushed_value PASSED          [ 42%]
test_stack.py::test_pop_empty_stack_raises PASSED            [ 57%]
test_stack.py::test_peek_returns_top_without_removing PASSED [ 71%]
test_stack.py::test_peek_does_not_remove_element PASSED      [ 85%]
test_stack.py::test_lifo_order PASSED                        [100%]

================================================== 7 passed in 0.01s ===================================================
```

---

## Final Implementation

### `stack.py`
```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def peek(self):
        return self._items[-1]

    def pop(self):
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0
```

### `test_stack.py`
```python
# Test list (TODO):
# [x] is_empty on a new stack returns True
# [x] is_empty returns False after push
# [x] push then pop returns the pushed value
# [x] pop on empty stack raises IndexError
# [x] peek returns top element without removing it
# [x] peek after push leaves element on stack (is_empty still False)
# [x] push multiple items, pop returns LIFO order

from stack import Stack
import pytest


def test_new_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True


def test_is_not_empty_after_push():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False


def test_pop_returns_pushed_value():
    s = Stack()
    s.push(42)
    assert s.pop() == 42


def test_pop_empty_stack_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_peek_returns_top_without_removing():
    s = Stack()
    s.push(7)
    assert s.peek() == 7


def test_peek_does_not_remove_element():
    s = Stack()
    s.push(7)
    s.peek()
    assert s.is_empty() is False


def test_lifo_order():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
```
