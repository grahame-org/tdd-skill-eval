import pytest
from stack import Stack


def test_new_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True


def test_push_makes_stack_non_empty():
    s = Stack()
    s.push(1)
    assert s.is_empty() is False


def test_peek_returns_top_element():
    s = Stack()
    s.push(42)
    assert s.peek() == 42


def test_peek_does_not_remove_element():
    s = Stack()
    s.push(42)
    s.peek()
    assert s.is_empty() is False


def test_pop_returns_top_element():
    s = Stack()
    s.push(7)
    assert s.pop() == 7


def test_pop_removes_element():
    s = Stack()
    s.push(7)
    s.pop()
    assert s.is_empty() is True


def test_pop_on_empty_stack_raises_index_error():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_push_multiple_pop_lifo_order():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1


def test_peek_after_multiple_pushes():
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b"
