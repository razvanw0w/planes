'''
PlayerController class - the support of the player moves
'''

from validation.planeValidator import PlaneValidator
from model.plane import Plane
from utilities.gameConstants import GameConstants
import unittest

class PlayerController:
    def __init__(self, playerRepository):
        '''
        This function is the initialiser of the PlayerController object
        :param playerRepository: the storage support of the player moves - PlayerRepository
        '''
        self.__playerRepository = playerRepository
        self.__planesList = []

    def initializeNewGame(self):
        '''
        This function initializes a new game
        :return: nothing
        '''
        self.__playerRepository.initializeNewGame()
        self.__planesList.clear()

    def getShotsGrid(self):
        return self.__playerRepository.getShotsGrid()

    def getPlanesGrid(self):
        return self.__playerRepository.getPlanesGrid()

    def placePlane(self, cabinLocation, cabinOrientation):
        '''
        This function places a plane based on its location and orientation
        :param cabinLocation: the cell of the cabin - string (of the form column+row e.g. A2, C7, H1)
        :param cabinOrientation: the way the cabin points to (up/down/left/right)
        :return: nothing
        '''
        plane = Plane(cabinLocation, cabinOrientation)
        if PlaneValidator.checkPlane(plane) is False:
            raise ValueError("Invalid plane data entered")
        if PlaneValidator.checkPlaneCells(plane) is False:
            raise ValueError("Plane cannot be placed in the grid (some parts are out of the grid)")
        self.__playerRepository.addPlane(plane)
        self.__planesList.append(plane)

    def getRemainingPlanesNumber(self):
        '''
        This function returns the number of remaining active planes
        :return: planesNumber - the number of the remaining planes - integer
        '''
        return len(self.__planesList)

    def markMissedShot(self, row, column):
        '''
        This function marks a miss to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__playerRepository.markMissedShot(row, column)

    def markSuccessfulShot(self, row, column):
        '''
        This function marks a successful shot to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__playerRepository.markSuccessfulShot(row, column)
        
    def checkCell(self, cellCoordinates):
        '''
        This function checks a cell given by its coordinates
        :param cellCoordinates: the coordinates
        :return: "cabin" if the cell is a cabin
                 "hit" if the plane is a part
                 "empty" if the cell is empty
        '''
        row = cellCoordinates[0]
        column = cellCoordinates[1]
        value = self.__playerRepository.checkPlaneCell(row, column)
        answer = {-1: "miss", 1: "hit", 0: "cabin"}
        if value != -1:
            if value == 1:
                index = 0
                while index in range(len(self.__planesList)):
                    plane = self.__planesList[index]
                    playerPlaneCoordinates = GameConstants.cellStringToCoordinates(plane.getCabinLocation())
                    if cellCoordinates == playerPlaneCoordinates:
                        value = 0
                        del self.__planesList[index]
                        break
                    index += 1
            self.__playerRepository.hitCell(row, column)
        return answer[value]

class TestPlayerController(unittest.TestCase):
    def setUp(self):
        from repository.repository import Repository
        from utilities.matrixGenerator import MatrixGenerator
        repo = Repository()
        self.playerController = PlayerController(repo)
        self.constantInitialMatrix = MatrixGenerator.generateMatrix(8, 8, -1)

    def testInitializeNewGame(self):
        self.playerController.initializeNewGame()
        self.assertEqual(self.playerController.getPlanesGrid(), self.constantInitialMatrix)
        self.assertEqual(self.playerController.getShotsGrid(), self.constantInitialMatrix)

    def testGetShotsGridMarkShots(self):
        from copy import deepcopy
        matrix = deepcopy(self.constantInitialMatrix)
        self.assertEqual(self.playerController.getShotsGrid(), matrix)
        self.playerController.markMissedShot(1, 1)
        matrix[1][1] = 0
        self.assertEqual(self.playerController.getShotsGrid(), matrix)
        self.playerController.markSuccessfulShot(2, 2)
        matrix[2][2] = 1
        self.assertEqual(self.playerController.getShotsGrid(), matrix)