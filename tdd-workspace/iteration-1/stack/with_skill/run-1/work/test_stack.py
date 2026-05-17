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
