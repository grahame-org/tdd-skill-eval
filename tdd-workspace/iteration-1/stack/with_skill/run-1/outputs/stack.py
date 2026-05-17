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
