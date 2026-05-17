# TDD Transcript: Stack Implementation

## Task
Implement a `Stack` class in Python with `push`, `pop`, `peek`, and `is_empty` methods using Test-Driven Development. `pop` on an empty stack must raise `IndexError`.

---

## Cycle 1 — RED (Write failing tests)

Written `test_stack.py` with 13 tests covering all four methods before any implementation exists.

```
$ python -m pytest test_stack.py -v
ERROR collecting test_stack.py
  ModuleNotFoundError: No module named 'stack'
```

Tests fail at collection — `stack` module doesn't exist yet. ✅ RED confirmed.

---

## Cycle 2 — GREEN (Minimal implementation)

Created `stack.py`:

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0
```

```
$ python -m pytest test_stack.py -v
13 passed in 0.01s
```

All 13 tests pass. ✅ GREEN confirmed.

---

## Cycle 3 — REFACTOR

Implementation is already clean and minimal:
- Internal state uses a `list` (Python's built-in dynamic array)
- `push`/`pop`/`peek` delegate to list operations — O(1) amortised
- `is_empty` is a pure predicate with no side effects
- No refactoring needed.

---

## Test Coverage Summary

| Class             | Test                                     | Result |
|-------------------|------------------------------------------|--------|
| TestStackIsEmpty  | test_new_stack_is_empty                  | PASSED |
| TestStackIsEmpty  | test_stack_not_empty_after_push          | PASSED |
| TestStackIsEmpty  | test_stack_empty_after_push_and_pop      | PASSED |
| TestStackPush     | test_push_single_item                    | PASSED |
| TestStackPush     | test_push_multiple_items                 | PASSED |
| TestStackPush     | test_push_returns_none                   | PASSED |
| TestStackPop      | test_pop_returns_top_item                | PASSED |
| TestStackPop      | test_pop_removes_top_item                | PASSED |
| TestStackPop      | test_pop_lifo_order                      | PASSED |
| TestStackPop      | test_pop_empty_stack_raises_index_error  | PASSED |
| TestStackPop      | test_pop_until_empty_then_raises         | PASSED |
| TestStackPeek     | test_peek_returns_top_without_removing   | PASSED |
| TestStackPeek     | test_peek_does_not_change_size           | PASSED |

**13 / 13 passed**
