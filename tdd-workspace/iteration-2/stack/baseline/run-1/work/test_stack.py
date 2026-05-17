import pytest
from stack import Stack


class TestStackIsEmpty:
    def test_new_stack_is_empty(self):
        s = Stack()
        assert s.is_empty() is True

    def test_stack_not_empty_after_push(self):
        s = Stack()
        s.push(1)
        assert s.is_empty() is False

    def test_stack_empty_after_push_and_pop(self):
        s = Stack()
        s.push(1)
        s.pop()
        assert s.is_empty() is True


class TestStackPush:
    def test_push_single_item(self):
        s = Stack()
        s.push(42)
        assert s.peek() == 42

    def test_push_multiple_items(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        assert s.peek() == 3

    def test_push_returns_none(self):
        s = Stack()
        result = s.push(10)
        assert result is None


class TestStackPop:
    def test_pop_returns_top_item(self):
        s = Stack()
        s.push(7)
        assert s.pop() == 7

    def test_pop_removes_top_item(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.pop()
        assert s.peek() == 1

    def test_pop_lifo_order(self):
        s = Stack()
        s.push("a")
        s.push("b")
        s.push("c")
        assert s.pop() == "c"
        assert s.pop() == "b"
        assert s.pop() == "a"

    def test_pop_empty_stack_raises_index_error(self):
        s = Stack()
        with pytest.raises(IndexError):
            s.pop()

    def test_pop_until_empty_then_raises(self):
        s = Stack()
        s.push(1)
        s.pop()
        with pytest.raises(IndexError):
            s.pop()


class TestStackPeek:
    def test_peek_returns_top_without_removing(self):
        s = Stack()
        s.push(99)
        assert s.peek() == 99
        assert s.is_empty() is False

    def test_peek_does_not_change_size(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.peek()
        s.peek()
        assert s.pop() == 2
        assert s.pop() == 1
