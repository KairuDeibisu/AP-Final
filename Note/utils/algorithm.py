
from typing import List
from time import sleep

def divide_and_conquer(array: List[int], key: int) -> int:

    sleep(0.1)

    length_of_array = lambda: len(array)

    center_of_array = lambda: length_of_array() // 2

    while 1 < length_of_array():



        if array[center_of_array()] == key:
            return key
        elif array[center_of_array()] > key:
            array = array[:center_of_array()]
        else:
            array = array[center_of_array():]
    
    if not length_of_array():
        return None
    
    return None if (value:=array[center_of_array()]) != key else value

