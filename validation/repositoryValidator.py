'''
RepositoryValidator class - checks if a plane can be placed in the grid in order not to touch any other planes
'''

import unittest

class RepositoryValidator:
    @staticmethod
    def checkIfPlaneOverlaps(plane, grid):
        '''
        This function checks if a specific plane overlaps with an existing plane in the grid
        :param plane: the given plane - Plane
        :param grid: the given grid - matrix of integers
        :return: True if the plane overlaps with an existing plane
                 False otherwise
        '''
        planeCells = plane.getPlaneCellsList()
        for planeCell in planeCells:
            row = planeCell[0]
            column = planeCell[1]
            if grid[row][column] != -1:
                return True
        return False

class TestRepositoryValidator(unittest.TestCase):
    def testCheckIfPlaneOverlaps(self):
        from model.plane import Plane
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, 1, -1, -1, -1, -1, -1],
                  [-1, 1, 1, 1, -1, -1, -1, -1],
                  [-1, -1, 1, -1, -1, -1, -1, -1],
                  [1, 1, 1, 1, 1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertTrue(RepositoryValidator.checkIfPlaneOverlaps(Plane("A3", "left"), matrix))
        self.assertFalse(RepositoryValidator.checkIfPlaneOverlaps(Plane("F7", "down"), matrix))