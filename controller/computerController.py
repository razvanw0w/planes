'''
ComputerController class - the support of the computer moves
'''

from validation.planeValidator import PlaneValidator
from model.plane import Plane
from utilities.queue import Queue
from utilities.gameConstants import GameConstants
import random
import unittest

class ComputerController:
    def __init__(self, computerRepository):
        '''
        This function is the initialiser of the ComputerController object
        :param computerRepository: the storage support of the computer moves - ComputerRepository
        '''
        self.__computerRepository = computerRepository
        self.__planesList = []
        self.__queue = Queue()

    def initializeNewGame(self):
        '''
        This function initializes a new game
        :return: nothing
        '''
        self.__computerRepository.initializeNewGame()
        self.__planesList.clear()
        self.__queue.clear()
        
    def getShotsGrid(self):
        return self.__computerRepository.getShotsGrid()

    def getPlanesGrid(self):
        return self.__computerRepository.getPlanesGrid()

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
        self.__computerRepository.addPlane(plane)
        self.__planesList.append(plane)
        
    def placePlanesRandomly(self):
        '''
        This function generates planes randomly in order to be placed on the grid
        :return: nothing
        '''
        numberOfPlacesPlanes = 0
        columns = "ABCDEFGH"
        rows = "12345689"
        directions = ["up", "down", "left", "right"]
        while numberOfPlacesPlanes < 2:
            cabinLocation = random.choice(columns) + random.choice(rows)
            cabinOrientation = random.choice(directions)
            try:
                self.placePlane(cabinLocation, cabinOrientation)
                numberOfPlacesPlanes += 1
            except:
                pass

    def getRemainingPlanesNumber(self):
        '''
        This function returns the number of remaining active planes
        :return: planesNumber - the number of the remaining planes - integer
        '''
        return len(self.__planesList)

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
        value = self.__computerRepository.checkPlaneCell(row, column)
        answer = {-1: "miss", 1: "hit", 0: "cabin"}
        if value != -1:
            if value == 1:
                index = 0
                while index in range(len(self.__planesList)):
                    plane = self.__planesList[index]
                    computerPlaneCoordinates = GameConstants.cellStringToCoordinates(plane.getCabinLocation())
                    if cellCoordinates == computerPlaneCoordinates:
                        value = 0
                        del self.__planesList[index]
                        break
                    index += 1
            self.__computerRepository.hitCell(row, column)
        return answer[value]
    
    def markMissedShot(self, row, column):
        '''
        This function marks a miss to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__computerRepository.markMissedShot(row, column)

    def markSuccessfulShot(self, row, column):
        '''
        This function marks a successful shot to the shots grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        self.__computerRepository.markSuccessfulShot(row, column)

    def __generateRandomUnknownCell(self):
        '''
        This function randomly generated an unshot cell
        :return: tuple of the generated cell
        '''
        while True:
            row = random.randint(0, 7)
            column = random.randint(0, 7)
            if self.__computerRepository.isCellUnknown(row, column) == True:
                return (row, column)

    def getNextHit(self):
        '''
        This function returns the next hit of the computer
        :return: a tuple representing the cell to be hit
        '''
        if self.__queue.size() == 0:
            return self.__generateRandomUnknownCell()
        else:
            return self.__queue.pop()

    def __isCellInside(self, row, column):
        '''
        This function tells if the cell is inside the grid
        :param row: the row of the cell
        :param column: the column of the cell
        :return: True if the cell is inside the grid
                 False otherwise
        '''
        return row in range(8) and column in range(8)

    def enqueueNeighbors(self, row, column):
        '''
        This function pushes into the computer moves queue the neighbors of the specified cell
        :param row: the row of the cell
        :param column: the column of the cell
        :return: nothing
        '''
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            if self.__isCellInside(row + direction[0], column + direction[1]) == True and self.__computerRepository.isCellUnknown(row + direction[0], column + direction[1]) == True:
                self.__queue.push((row + direction[0], column + direction[1]))

    def clearQueue(self):
        '''
        This function clears the queue of the moves
        :return: nothing
        '''
        self.__queue.clear()

class TestComputerController(unittest.TestCase):
    def setUp(self):
        from repository.repository import Repository
        from utilities.matrixGenerator import MatrixGenerator
        repo = Repository()
        self.computerController = ComputerController(repo)
        self.constantInitialMatrix = MatrixGenerator.generateMatrix(8, 8, -1)

    def testInitializeNewGame(self):
        self.computerController.initializeNewGame()
        self.assertEqual(self.computerController.getPlanesGrid(), self.constantInitialMatrix)
        self.assertEqual(self.computerController.getShotsGrid(), self.constantInitialMatrix)

    def testGetShotsGridMarkShots(self):
        from copy import deepcopy
        matrix = deepcopy(self.constantInitialMatrix)
        self.assertEqual(self.computerController.getShotsGrid(), matrix)
        self.computerController.markMissedShot(1, 1)
        matrix[1][1] = 0
        self.assertEqual(self.computerController.getShotsGrid(), matrix)
        self.computerController.markSuccessfulShot(2, 2)
        matrix[2][2] = 1
        self.assertEqual(self.computerController.getShotsGrid(), matrix)