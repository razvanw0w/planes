'''
Repository class - the storage support of a player's moves
'''

from utilities.matrixGenerator import MatrixGenerator
from validation.repositoryValidator import RepositoryValidator
import unittest

class Repository:
    def __init__(self):
        self.__planesGrid = MatrixGenerator.generateMatrix(8, 8, -1)
        self.__shotsGrid = MatrixGenerator.generateMatrix(8, 8, -1)

    def initializeNewGame(self):
        '''
        This function resets the matrices
        :return: nothing
        '''
        self.__planesGrid = MatrixGenerator.generateMatrix(8, 8, -1)
        self.__shotsGrid = MatrixGenerator.generateMatrix(8, 8, -1)

    def getPlanesGrid(self):
        '''
        This function returns the matrix of the planes
        :return: planesGrid - the matrix of planes
        '''
        return self.__planesGrid[:]

    def getShotsGrid(self):
        '''
        This function returns the matrix of shots
        :return: shotsGrid - the matrix of shots
        '''
        return self.__shotsGrid[:]

    def addPlane(self, plane):
        '''
        This function should add a plane into the storage
        :param plane: a given plane - Plane
        :return: nothing
        '''
        if RepositoryValidator.checkIfPlaneOverlaps(plane, self.__planesGrid) is True:
            raise ValueError("Plane cannot be placed in the grid (overlaps with an existing plane)")
        planeCells = plane.getPlaneCellsList()
        for planeCell in planeCells:
            row = planeCell[0]
            column = planeCell[1]
            self.__planesGrid[row][column] = 1

    def hitCell(self, row, column):
        '''
        This function treats a hit to the cell
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        if self.__planesGrid[row][column] == 1:
            self.__planesGrid[row][column] = 0

    def markSuccessfulShot(self, row, column):
        '''
        This function marks a successful shot to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__shotsGrid[row][column] = 1

    def markMissedShot(self, row, column):
        '''
        This function marks a miss to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__shotsGrid[row][column] = 0

    def checkPlaneCell(self, row, column):
        '''
        This function returns the value in the plane grid of the given cell
        :param row: row of the cell
        :param column: column of the cell
        :return: the value of the given cell
        '''
        return self.__planesGrid[row][column]

    def isCellUnknown(self, row, column):
        '''
        This function tells if the specified cell has been shot
        :param row: the row of the cell
        :param column: the column of the cell
        :return: True if it has been shot
                 False otherwise
        '''
        return self.__shotsGrid[row][column] == -1

class TestRepository(unittest.TestCase):
    def setUp(self):
        self.repo = Repository()

    def testInitializeNewGame(self):
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.repo.initializeNewGame()
        self.assertEqual(self.repo.getPlanesGrid(), matrix)
        self.assertEqual(self.repo.getShotsGrid(), matrix)

    def testGetPlanesGridAddPlane(self):
        from model.plane import Plane
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertEqual(self.repo.getPlanesGrid(), matrix)
        self.repo.addPlane(Plane("A5", "left"))
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, 1, -1, -1, -1, -1, -1, -1],
                  [-1, 1, -1, 1, -1, -1, -1, -1],
                  [1, 1, 1, 1, -1, -1, -1, -1],
                  [-1, 1, -1, 1, -1, -1, -1, -1],
                  [-1, 1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertEqual(self.repo.getPlanesGrid(), matrix)
        self.repo.hitCell(3, 1)
        matrix[3][1] = 0
        self.assertEqual(self.repo.getPlanesGrid(), matrix)
        self.assertEqual(self.repo.checkPlaneCell(3, 1), 0)
        self.assertEqual(self.repo.checkPlaneCell(4, 2), 1)
        self.assertEqual(self.repo.checkPlaneCell(0, 0), -1)

    def testGetShotsGridMarkShots(self):
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertEqual(self.repo.getShotsGrid(), matrix)
        matrix[3][2] = 1
        self.repo.markSuccessfulShot(3, 2)
        self.assertEqual(self.repo.getShotsGrid(), matrix)
        matrix[3][2] = 0
        self.repo.markMissedShot(3, 2)
        self.assertEqual(self.repo.getShotsGrid(), matrix)
        self.assertTrue(self.repo.isCellUnknown(5, 3))
        self.assertFalse(self.repo.isCellUnknown(3, 2))