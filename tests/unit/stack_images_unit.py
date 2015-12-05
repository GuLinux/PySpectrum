import unittest
from stack_images_dialog import MedianStacker
import numpy as np
from numpy.testing import * 

class TestSpectrum(unittest.TestCase):
    def setUp(self):
        self.single_matrix_data = [
            {'data': np.array([1,2,3,4,5,6]).reshape(2,3), 'offset': {'x': 0, 'y': 0} }
            ]
        self.two_matrices_data = [self.single_matrix_data[0],
            {'data': np.array([3,4,5,6,7,8]).reshape(2,3), 'offset': {'x': 2, 'y': -3} }
        ]
        self.three_matrices_data = [self.single_matrix_data[0], self.two_matrices_data[1],
            {'data': np.array([4,5,6,7,8,9]).reshape(2,3), 'offset': {'x': -4, 'y': 7} }
        ]
        
    def test_final_shape(self):
        stacker = MedianStacker(self.single_matrix_data)
        self.assertEqual(stacker.final_shape()['shape'], (2,3))
        self.assertEqual(stacker.final_shape()['zero'], (0,0))
        stacker = MedianStacker(self.two_matrices_data)
        self.assertEqual(stacker.final_shape()['shape'], (5,5))
        self.assertEqual(stacker.final_shape()['zero'], (3,0))
        stacker = MedianStacker(self.three_matrices_data)
        self.assertEqual(stacker.final_shape()['shape'], (12,9))
        self.assertEqual(stacker.final_shape()['zero'], (3,4))
        
    def test_data_reposition(self):
        stacker = MedianStacker([])
        input = self.three_matrices_data[0]
        data = input['data']
        assert_array_equal(stacker.data_reposition(input, {'zero': (0,0), 'shape': (2,3)}), data)
        
        expected = np.zeros(3*3).reshape(3,3)
        expected[1:3,0:3]=data
        assert_array_equal(stacker.data_reposition(input, {'zero': (1,0), 'shape': (3,3)}), expected)
        
        expected = np.zeros(3*4).reshape(3,4)
        expected[1:3,1:4]=data
        assert_array_equal(stacker.data_reposition(input, {'zero': (1,1), 'shape': (3,4)}), expected)
        
        input = self.three_matrices_data[1]
        data = input['data']
        expected = np.zeros(4*6).reshape(4,6)
        expected[0:2,2:5]=data
        assert_array_equal(stacker.data_reposition(input, {'zero': (3,0), 'shape': (4,6)}), expected)
        
        input = self.three_matrices_data[2]
        data = input['data']
        expected = np.zeros(12*9).reshape(12,9)
        expected[10:12,0:3]=data
        actual = stacker.data_reposition(input, {'zero': (3,4), 'shape': (12,9)})
        assert_array_equal(actual, expected)
        
    def test_median_single(self):
        stacker = MedianStacker(self.single_matrix_data)
        assert_array_equal(stacker.median(), self.single_matrix_data[0]['data'])
        
    def test_median(self):
        stacker = MedianStacker([self.two_matrices_data[0], self.two_matrices_data[0], self.two_matrices_data[1]])
        expected = np.zeros(25).reshape(5,5)
        expected[3:5,0:3] = np.arange(1,7).reshape(2,3)
        assert_array_equal(stacker.median(), expected)
        
        stacker = MedianStacker([self.two_matrices_data[0], self.two_matrices_data[1], self.two_matrices_data[1]])
        expected = np.zeros(25).reshape(5,5)
        expected[0:2,2:5] = np.arange(3,9).reshape(2,3)
        assert_array_equal(stacker.median(), expected)

if __name__ == '__main__':
    unittest.main()