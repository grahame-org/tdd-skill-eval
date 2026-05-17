import pytest
from sum_list import sum_list


def test_empty_list():
    assert sum_list([]) == 0


def test_single_element():
    assert sum_list([5]) == 5


def test_two_elements():
    assert sum_list([1, 2]) == 3


def test_multiple_elements():
    assert sum_list([1, 2, 3, 4, 5]) == 15


def test_negative_numbers():
    assert sum_list([-1, -2, -3]) == -6


def test_mixed_positive_and_negative():
    assert sum_list([10, -3, 5]) == 12


def test_zeros():
    assert sum_list([0, 0, 0]) == 0
