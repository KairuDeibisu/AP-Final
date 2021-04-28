

from typing import List


def divide_and_conquer(array: List[int], key: int) -> int:
    """
    Find element in list.

    Args:
        array: A list of integers.
        key: The value to find.

    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 6)
    6
    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 11)
    11
    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 1)
    1
    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 11)
    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
    5
    >>> divide_and_conquer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1)
    1

    """

    def center_of_array(): return len(array) // 2

    while 1 < len(array):

        if array[center_of_array()] == key:
            return key

        if array[center_of_array()] > key:
            array = array[:center_of_array()]
        else:
            array = array[center_of_array():]

    if not len(array):
        return None

    return None if (value := array[center_of_array()]) != key else value
