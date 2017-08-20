import unittest
from binary_search import binary_search

class TestBinarySearch(unittest.TestCase):

    def test_binary_search(self):
        filter_val = ['Subaru', 'Chevrolet', 'Toyota', 'Dodge']
        filter_val = sorted(filter_val)

        answer = binary_search(filter_val, 'Chevrolet')
        self.assertTrue(answer)
        