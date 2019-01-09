'''
InputValidator class - responsible for the validation of the user input
'''

import unittest
from utilities.gameConstants import GameConstants

class InputValidator:
    @staticmethod
    def getIntegerFromString(givenString):
        '''
        This function returns an integer from a given string
        :param givenString: a string entered by the user - string
        :return: givenInteger: an integer converted from the string
                 None if the string doesn't represent an integer
        '''
        try:
            givenInteger = int(givenString)
            return givenInteger
        except:
            return None

    @staticmethod
    def checkIfIntegerInInterval(lowerBound, upperBound, givenValue):
        '''
        This function checks if a given integer value is between a lower bound and an upper bound
        :param lowerBound: the lower bound of the interval - integer
        :param upperBound: the upper bound of the interval - integer
        :param givenValue: the given integer value - integer
        :return: True if the integer is in the given closed interval
                 False otherwise
        '''
        return givenValue >= lowerBound and givenValue <= upperBound

    @staticmethod
    def checkIfCellIsCorrect(cellString):
        '''
        This function checks if a user-entered string represents a valid cell
        :param cellString: user-entered string
        :return: True if the provided strings denotes a valid cell (e.g. A3, B7, C2 etc.)
                 False otherwise
        '''
        columns = "ABCDEFGH"
        rows = "12345678"
        if len(cellString) != 2:
            return False
        if cellString[0] not in columns:
            return False
        if cellString[1] not in rows:
            return False
        return True

    @staticmethod
    def __checkForEnoughTilesForPlane(matrix):
        '''
        This function checks if a matrix has enough completed tiles for a plane
        :param matrix: the grid of planes
        :return: True or False accordingly
        '''
        planeTilesCounter = 0
        for line in matrix:
            planeTilesCounter += line.count(2)
        if planeTilesCounter != 10:
            return False

    @staticmethod
    def __getEnclosingPlaneMatrixLimits(matrix):
        '''
        This function returns the upper-left corner and down-right corner of a 'plane'
        :param matrix: the grid of planes
        :return: minimumRow, minimumColumn, maximumRow, maximumColumn - integers
        '''
        minimumRow = minimumColumn = 8
        maximumRow = maximumColumn = -1
        for i in range(8):
            for j in range(8):
                if matrix[i][j] == 2:
                    minimumRow = min(minimumRow, i)
                    maximumRow = max(maximumRow, i)
                    minimumColumn = min(minimumColumn, j)
                    maximumColumn = max(maximumColumn, j)
        return minimumRow, minimumColumn, maximumRow, maximumColumn

    @staticmethod
    def __checkIfAlike(constantMatrix, planeMatrix, minimumRow, minimumColumn, maximumRow, maximumColumn):
        '''
        This function checks if the constant matrix and the plane matrix are alike in the given boundaries
        :param constantMatrix:
        :param planeMatrix:
        :param minimumRow: the minimum row of the so-called plane
        :param minimumColumn: the minimum column of the so-called plane
        :param maximumRow: the maximum row of the so-called plane
        :param maximumColumn: the maximum column of the so-called plane
        :return: True or False accordingly
        '''
        for i in range(maximumRow - minimumRow + 1):
            for j in range(maximumColumn - minimumColumn + 1):
                if constantMatrix[i][j] == 1:
                    if planeMatrix[minimumRow + i][minimumColumn + j] != 2:
                        return False
                else:
                    if planeMatrix[minimumRow + i][minimumColumn + j] == 2:
                        return False
        return True

    @staticmethod
    def checkIfDrawnPlaneIsCorrect(matrix):
        '''
        This function checks if a drawn 'plane' is drawn correctly
        :param matrix: the matrix of planes
        :return: True or False whether the plane is drawn correctly on the grid
                 if it is correctly placed, it will return the cabin location as well
        '''
        if InputValidator.__checkForEnoughTilesForPlane(matrix) == False:
            return False, None, None
        minimumRow, minimumColumn, maximumRow, maximumColumn = InputValidator.__getEnclosingPlaneMatrixLimits(matrix)
        if maximumRow - minimumRow + 1 == 4 and maximumColumn - minimumColumn + 1 == 5:
            if InputValidator.__checkIfAlike(GameConstants.upPlane, matrix, minimumRow, minimumColumn, maximumRow, maximumColumn) == True:
                return True, GameConstants.coordinatesToCellString(minimumRow, minimumColumn + 2), "up"
            if InputValidator.__checkIfAlike(GameConstants.downPlane, matrix, minimumRow, minimumColumn, maximumRow, maximumColumn) == True:
                return True, GameConstants.coordinatesToCellString(maximumRow, minimumColumn + 2), "down"
        elif maximumRow - minimumRow + 1 == 5 and maximumColumn - minimumColumn + 1 == 4:
            if InputValidator.__checkIfAlike(GameConstants.leftPlane, matrix, minimumRow, minimumColumn, maximumRow, maximumColumn) == True:
                return True, GameConstants.coordinatesToCellString(minimumRow + 2, minimumColumn), "left"
            if InputValidator.__checkIfAlike(GameConstants.rightPlane, matrix, minimumRow, minimumColumn, maximumRow, maximumColumn) == True:
                return True, GameConstants.coordinatesToCellString(minimumRow + 2, maximumColumn), "right"
        return False, None, None

class TestInputValidator(unittest.TestCase):
    def testGetIntegerFromString(self):
        integer = InputValidator.getIntegerFromString("12")
        self.assertEqual(integer, 12)
        integer = InputValidator.getIntegerFromString("-12")
        self.assertEqual(integer, -12)
        integer = InputValidator.getIntegerFromString("1e")
        self.assertIsNone(integer)

    def testCheckIfIntegerInInterval(self):
        self.assertTrue(InputValidator.checkIfIntegerInInterval(2, 5, 3))
        self.assertFalse(InputValidator.checkIfIntegerInInterval(2, 5, -1))
        self.assertTrue(InputValidator.checkIfIntegerInInterval(2, 5, 2))
        self.assertFalse(InputValidator.checkIfIntegerInInterval(2, 5, 6))
        self.assertTrue(InputValidator.checkIfIntegerInInterval(2, 3, 2))

    def testCheckIfCellIsCorrect(self):
        self.assertTrue(InputValidator.checkIfCellIsCorrect("A2"))
        self.assertFalse(InputValidator.checkIfCellIsCorrect("A9"))
        self.assertFalse(InputValidator.checkIfCellIsCorrect("2X"))
        self.assertFalse(InputValidator.checkIfCellIsCorrect("2A"))
        self.assertTrue(InputValidator.checkIfCellIsCorrect("H8"))

    def testCheckIfDrawnPlaneIsCorrect(self):
        matrix = [[-1, 2, 2, -1, -1, -1, -1, -1],
                  [2, 2, 2, 2, 2, -1, -1, -1],
                  [-1, -1, 2, -1, -1, -1, -1, -1],
                  [-1, 2, 2, 2, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        answer, location, orientation = InputValidator.checkIfDrawnPlaneIsCorrect(matrix)
        self.assertFalse(answer)
        matrix[0][1] = -1
        answer, location, orientation = InputValidator.checkIfDrawnPlaneIsCorrect(matrix)
        self.assertTrue(answer)
        self.assertEqual(location, "C1")
        self.assertEqual(orientation, "up")