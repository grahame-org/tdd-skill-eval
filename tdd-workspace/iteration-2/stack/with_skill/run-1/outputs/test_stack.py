from stack import Stack
import pytest


# Cycle 1 — is_empty on a new stack
def test_new_stack_is_empty():
    stack = Stack()
    assert stack.is_empty() is True


# Cycle 2 — not empty after push
def test_not_empty_after_push():
    stack = Stack()
    stack.push(1)
    assert stack.is_empty() is False


# Cycle 3 — pop returns the pushed value
def test_pop_returns_pushed_value():
    stack = Stack()
    stack.push(42)
    assert stack.pop() == 42


# Cycle 4 — pop removes the element (stack empty after popping last item)
def test_pop_empties_stack():
    stack = Stack()
    stack.push(1)
    stack.pop()
    assert stack.is_empty() is True


# Cycle 5 — pop on empty stack raises IndexError
def test_pop_raises_index_error_on_empty_stack():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()


# Cycle 6 — peek returns the top value
def test_peek_returns_top_value():
    stack = Stack()
    stack.push(7)
    assert stack.peek() == 7


# Cycle 7 — peek does not remove the element
def test_peek_does_not_remove_element():
    stack = Stack()
    stack.push(1)
    stack.peek()
    assert stack.is_empty() is False


# Triangulation A — LIFO order: pop returns last pushed
def test_pop_lifo_order():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2


# Triangulation B — peek returns last pushed after multiple pushes
def test_peek_returns_last_pushed():
    stack = Stack()
    stack.push(10)
    stack.push(20)
    assert stack.peek() == 20
