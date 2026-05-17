# Transcript: Stack TDD Implementation

## Approach

Followed a classic Red → Green TDD cycle:

1. **Write all tests first** — covering each behaviour one at a time.
2. **Run tests** — confirmed they fail with `ModuleNotFoundError` (no `stack.py` yet).
3. **Write minimal implementation** to make all tests pass.
4. **Run tests again** — all 9 pass.

---

## Test Cases Written (and Why)

| Test | Rationale |
|------|-----------|
| `test_new_stack_is_empty` | A freshly created stack must report `is_empty() == True`. |
| `test_push_makes_stack_non_empty` | Pushing one item should flip `is_empty` to `False`. |
| `test_peek_returns_top_element` | `peek` must return the most-recently-pushed value. |
| `test_peek_does_not_remove_element` | `peek` must be non-destructive — stack stays non-empty. |
| `test_pop_returns_top_element` | `pop` must return the top value. |
| `test_pop_removes_element` | `pop` must remove the element (stack becomes empty). |
| `test_pop_on_empty_stack_raises_index_error` | Spec requires `IndexError` on underflow. |
| `test_push_multiple_pop_lifo_order` | Verifies LIFO ordering across several pushes and pops. |
| `test_peek_after_multiple_pushes` | `peek` must always reflect the *current* top, not first pushed. |

---

## Order: Tests Before Implementation

1. Created `test_stack.py` with all 9 tests.
2. Ran `pytest` → **FAIL** (ImportError – no module `stack`).
3. Created `stack.py` with `Stack` class using a list internally.
4. Ran `pytest` → **9 passed**.

---

## Final Test Run Output

```
================================================= test session starts ==================================================
platform linux -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0
rootdir: .../outputs

test_stack.py::test_new_stack_is_empty PASSED                    [ 11%]
test_stack.py::test_push_makes_stack_non_empty PASSED            [ 22%]
test_stack.py::test_peek_returns_top_element PASSED              [ 33%]
test_stack.py::test_peek_does_not_remove_element PASSED          [ 44%]
test_stack.py::test_pop_returns_top_element PASSED               [ 55%]
test_stack.py::test_pop_removes_element PASSED                   [ 66%]
test_stack.py::test_pop_on_empty_stack_raises_index_error PASSED [ 77%]
test_stack.py::test_push_multiple_pop_lifo_order PASSED          [ 88%]
test_stack.py::test_peek_after_multiple_pushes PASSED            [100%]

================================================== 9 passed in 0.01s ===================================================
```
