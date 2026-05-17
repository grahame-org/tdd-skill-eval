from sum_list import sum_list

def test_empty_list_returns_zero():
    assert sum_list([]) == 0

def test_single_element_returns_that_element():
    assert sum_list([5]) == 5

def test_multiple_elements_returns_their_sum():
    assert sum_list([1, 2, 3]) == 6
