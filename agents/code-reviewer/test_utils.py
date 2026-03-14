import pytest
from utils import calculate_average, get_user, merge_lists

def test_average_empty():
    assert calculate_average([]) == 0

def test_average_normal():
    assert calculate_average([1, 2, 3]) == 2.0

def test_get_user_missing_name():
    users = [{"id": 1}]
    result = get_user(users, 1)
    assert result is None

def test_merge_lists_no_mutation():
    result1 = merge_lists([1, 2])
    result2 = merge_lists([3, 4])
    assert result2 == [3, 4]
