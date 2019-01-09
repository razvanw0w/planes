'''
GameController class - the "brain" of the game
'''

from utilities.gameConstants import GameConstants
import unittest

class GameController:
    def __init__(self, playerController, computerController):
        '''
        This function is the initialiser of the game controller
        :param playerController: the support of the player moves - PlayerController
        :param computerController: the support of the computer moves - ComputerController
        '''
        self.__playerController = playerController
        self.__computerController = computerController

    def initializeNewGame(self):
        '''
        This function initializes a new game (resets all the hit/plane progress)
        :return: nothing
        '''
        self.__playerController.initializeNewGame()
        self.__computerController.initializeNewGame()
        self.__computerController.placePlanesRandomly()

    def getPlayerShotsGrid(self):
        '''
        This function returns the matrix which represents the shots of the player
        :return: the player shots matrix
        '''
        return self.__playerController.getShotsGrid()

    def getPlayerPlanesGrid(self):
        '''
        This function returns the matrix with represents the planes of the player
        :return: the player planes matrix
        '''
        return self.__playerController.getPlanesGrid()

    def getComputerPlanesGrid(self):
        '''
        This function returns the matrix with represents the planes of the computer
        :return: the computer planes matrix
        '''
        return self.__computerController.getPlanesGrid()

    def placePlayerPlane(self, cabinLocation, cabinOrientation):
        '''
        This function places a plane for the human player based on its cabin location and cabin orientation
        :param cabinLocation: the cell of the cabin - string (of the form column+row e.g. A2, C7, H1)
        :param cabinOrientation: the way the cabin points to (up/down/left/right)
        :return: nothing
        '''
        self.__playerController.placePlane(cabinLocation, cabinOrientation)

    def getGameWinner(self):
        '''
        This function returns a specific value meaning the winner of the game
        :return: "none" if the game hasn't ended yet
                 "player" if the player won
                 "computer if the computer won
        '''
        playerPlanesNumber = self.__playerController.getRemainingPlanesNumber()
        computerPlanesNumber = self.__computerController.getRemainingPlanesNumber()
        if computerPlanesNumber == 0:
            return "player"
        if playerPlanesNumber == 0:
            return "computer"
        return "none"

    def makePlayerHit(self, cellString):
        '''
        This function hits a cell provided by a player
        :param cellString - the string which represents a valid cell
        :return: "hit" if the player hit a regular cell
                 "cabin" if the player hit a cabin (destroyed a plane)
                 "miss" if the player missed
        '''
        cellPosition = GameConstants.cellStringToCoordinates(cellString)
        row = cellPosition[0]
        column = cellPosition[1]
        hitResult = self.__computerController.checkCell(cellPosition)
        if hitResult == "miss":
            self.__playerController.markMissedShot(row, column)
        else:
            self.__playerController.markSuccessfulShot(row, column)
        return hitResult
    
    def makeComputerHit(self):
        '''
        This function hits a cell provided by a computer
        :return: "hit" if the computer hit a regular cell
                 "cabin" if the computer hit a cabin (destroyed a plane)
                 "miss" if the computer missed
        '''
        cellPosition = self.__computerController.getNextHit()
        row = cellPosition[0]
        column = cellPosition[1]
        hitResult = self.__playerController.checkCell(cellPosition)
        if hitResult == "miss":
            self.__computerController.markMissedShot(row, column)
        else:
            self.__computerController.markSuccessfulShot(row, column)
            if hitResult == "hit":
                self.__computerController.enqueueNeighbors(row, column)
            else:
                self.__computerController.clearQueue()
        if hitResult == "miss":
            return hitResult, None
        else:
            return hitResult, cellPosition

class TestGameController(unittest.TestCase):
    def setUp(self):
        from repository.repository import Repository
        from controller.playerController import PlayerController
        from controller.computerController import ComputerController
        from utilities.matrixGenerator import MatrixGenerator
        playerRepository = Repository()
        computerRepository = Repository()
        playerController = PlayerController(playerRepository)
        computerController = ComputerController(computerRepository)
        self.gameController = GameController(playerController, computerController)
        self.matrix = MatrixGenerator.generateMatrix(8, 8, -1)

    def testInitializeNewGame(self):
        self.gameController.initializeNewGame()
        matrix = self.gameController.getPlayerShotsGrid()
        self.assertEqual(self.gameController.getPlayerPlanesGrid(), self.matrix)
        self.assertEqual(self.gameController.getPlayerShotsGrid(), self.matrix)
        self.assertNotEqual(self.gameController.getComputerPlanesGrid(), self.matrix)

    def testPlacePlayerPlane(self):
        self.gameController.placePlayerPlane("A5", "left")
        matrix = [[-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1],
                  [-1, 1, -1, -1, -1, -1, -1, -1],
                  [-1, 1, -1, 1, -1, -1, -1, -1],
                  [1, 1, 1, 1, -1, -1, -1, -1],
                  [-1, 1, -1, 1, -1, -1, -1, -1],
                  [-1, 1, -1, -1, -1, -1, -1, -1],
                  [-1, -1, -1, -1, -1, -1, -1, -1]]
        self.assertEqual(self.gameController.getPlayerPlanesGrid(), matrix)