'''
GameConstants class - encapsulates the constants of the game
'''

import unittest

class GameConstants:
    upDownCabinDirections = [(0, 0), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, 0), (3, -1), (3, 0), (3, 1)]
    leftRightCabinDirections = [(0, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]
    realColumn = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    realRow = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
    realStringColumn = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    realStringRow = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8'}
    directions = {'up': upDownCabinDirections, 'down': upDownCabinDirections,
                         'left': leftRightCabinDirections, 'right': leftRightCabinDirections}
    directionSign = {'up': 1, 'down': -1, 'left': 1, 'right': -1}
    upPlane = [[0, 0, 1, 0, 0],
               [1, 1, 1, 1, 1],
               [0, 0, 1, 0, 0],
               [0, 1, 1, 1, 0]]
    downPlane = [[0, 1, 1, 1, 0],
                 [0, 0, 1, 0, 0],
                 [1, 1, 1, 1, 1],
                 [0, 0, 1, 0, 0]]
    leftPlane = [[0, 1, 0, 0],
                 [0, 1, 0, 1],
                 [1, 1, 1, 1],
                 [0, 1, 0, 1],
                 [0, 1, 0, 0]]
    rightPlane = [[0, 0, 1, 0],
                  [1, 0, 1, 0],
                  [1, 1, 1, 1],
                  [1, 0, 1, 0],
                  [0, 0, 1, 0]]
    
    @staticmethod
    def cellStringToCoordinates(cellString):
        '''
        This function converts a valid cell given by a string into real coordinates
        :return: cellCoordinates - the coordinates of the cell
        '''
        return (GameConstants.realRow[cellString[1]], GameConstants.realColumn[cellString[0]])

    @staticmethod
    def coordinatesToCellString(row, column):
        '''
        This function converts a cell given by its coordinates into a string
        :param row: the given row
        :param column: the given column
        :return: cellString - the string which represents the cell
        '''
        return GameConstants.realStringColumn[column] + GameConstants.realStringRow[row]

class TestGameConstants(unittest.TestCase):
    def testCellStringToCoordinates(self):
        self.assertEqual(GameConstants.cellStringToCoordinates("A3"), (2, 0))
        self.assertEqual(GameConstants.cellStringToCoordinates("D3"), (2, 3))
        self.assertEqual(GameConstants.cellStringToCoordinates("C7"), (6, 2))
        self.assertEqual(GameConstants.cellStringToCoordinates("H1"), (0, 7))

    def testCoordinatesToCellString(self):
        self.assertEqual(GameConstants.coordinatesToCellString(2, 0), "A3")
        self.assertEqual(GameConstants.coordinatesToCellString(2, 3), "D3")
        self.assertEqual(GameConstants.coordinatesToCellString(6, 2), "C7")
        self.assertEqual(GameConstants.coordinatesToCellString(0, 7), "H1")