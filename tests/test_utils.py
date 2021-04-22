from Note.utils.algorithm import divide_and_conquer

import unittest



class Testalgorithm(unittest.TestCase):

    def test_divide_and_conquer(self):
        """
        Test Implementation of divide and conquer algorithm
        """
        
        list_ = [1,2,3,4,5,6,7,8,9,10,11]

        self.assertEqual(divide_and_conquer(list_, 6), 6)
        self.assertEqual(divide_and_conquer(list_, 5), 5)
        self.assertEqual(divide_and_conquer(list_, 11), 11)
        self.assertEqual(divide_and_conquer(list_, 1), 1)
        self.assertEqual(divide_and_conquer(list_, 3), 3)
        self.assertEqual(divide_and_conquer(list_, 2), 2)

        list_ = [1,2,3,4,5,6,7,8,9,10]
        self.assertEqual(divide_and_conquer(list_, 6), 6)
        self.assertEqual(divide_and_conquer(list_, 5), 5)
        self.assertEqual(divide_and_conquer(list_, 11), None)
        self.assertEqual(divide_and_conquer(list_, 1), 1)

