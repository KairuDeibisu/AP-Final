
from Note.utils.algorithm import divide_and_conquer

from typing import List
from timeit import timeit


def divide_and_conquer(array: List[int], key: int) -> int:

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


if __name__ == "__main__":
    data_set = [*range(100000)]
    run_1 = timeit(lambda: divide_and_conquer(data_set, 250), number=10000)
    run_2 = timeit(lambda: divide_and_conquer(data_set, 2500), number=10000)
    run_3 = timeit(lambda: divide_and_conquer(data_set, 50000), number=10000)
    average = (run_1 + run_2 + run_3) / 3

    print(f"Run 1 took: {run_1:.2f}")
    print(f"Run 2 took: {run_2:.2f}")
    print(f"Run 3 took: {run_3:.2f}")
    print(f"Average of all runs: {average:.2f}")
