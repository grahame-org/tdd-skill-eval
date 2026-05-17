# Transcript: TDD Implementation of `sum_list`

## Approach

Used TDD starting from the simplest case, building up to more complex scenarios.

## Steps

### 1. Empty list (simplest case)
Wrote the first test: `sum_list([]) == 0`. Implemented `sum_list` to return 0 for an empty list using an accumulator loop.

### 2. Single element
Added `test_single_element`: `sum_list([5]) == 5`. The loop already handles this.

### 3. Two elements
Added `test_two_elements`: `sum_list([1, 2]) == 3`. Confirmed accumulation works.

### 4. Multiple elements
Added `test_multiple_elements`: `sum_list([1, 2, 3, 4, 5]) == 15`.

### 5. Negative numbers
Added `test_negative_numbers`: `sum_list([-1, -2, -3]) == -6`.

### 6. Mixed positive and negative
Added `test_mixed_positive_and_negative`: `sum_list([10, -3, 5]) == 12`.

### 7. Zeros
Added `test_zeros`: `sum_list([0, 0, 0]) == 0`.

## Result

All 7 tests passed. Final implementation:

```python
def sum_list(numbers):
    total = 0
    for n in numbers:
        total += n
    return total
```
