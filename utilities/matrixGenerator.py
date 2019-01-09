'''
MatrixGenerator class - generates matrixes of different values
'''

from copy import deepcopy
import unittest

class MatrixGenerator:
    @staticmethod
    def generateMatrix(rowCounter, columnCounter, fillingElement = 0):
        '''
        This function generates a matrix with 'rowCounter' rows, 'columnCounter' columns and fills it with
        'fillingElement'
        :param rowCounter: the number of rows of matrix - integer
        :param columnCounter: the number of columns of matrix - integer
        :param fillingElement: the element which the matrix needs to be filled with - any type
        :return: matrix: the generated matrix
        '''
        matrix = []
        elementaryRow = [fillingElement] * columnCounter
        for i in range(rowCounter):
            matrix += [deepcopy(elementaryRow)]
        return matrix

class TestMatrixGenerator(unittest.TestCase):
    def testGenerateMatrix(self):
        matrix = MatrixGenerator.generateMatrix(2, 3, 5)
        self.assertEqual(matrix, [[5, 5, 5], [5, 5, 5]])
        matrix = MatrixGenerator.generateMatrix(3, 4)
        self.assertEqual(matrix, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        matrix = MatrixGenerator.generateMatrix(5, 2, -1)
        self.assertEqual(matrix, [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]])