'''
GameConsoleInterface class - console-based user interface
'''

from validation.inputValidator import InputValidator
from texttable import *
from utilities.gameConstants import GameConstants

class GameConsoleInterface:
    def __init__(self, gameController):
        '''
        This function initialises the GameConsoleInterface object
        :param gameController: the game controller (brain of the game) - GameController
        '''
        self.__gameController = gameController
        self.__columnList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.__hitResults = {"hit": "{} has hit a cell!", "cabin": "{} has destroyed a plane!", "miss": "{} missed!"}

    def __UIexitGame(self):
        print("Thank you for playing Planes!")

    def __UIprintShotsGrid(self, grid):
        textTable = Texttable()
        textTable.add_row([' '] + self.__columnList)
        for i in range(8):
            row = [str(i + 1)]
            for j in range(8):
                entry = '?'
                if grid[i][j] == 0:
                    entry = 'O'
                elif grid[i][j] == 1:
                    entry = 'X'
                row += [entry]
            textTable.add_row(row)
        print("==============Your shots==============")
        print(textTable.draw())
        print("==============Your shots==============")

    def __UIprintPlanesGrid(self, grid):
        textTable = Texttable()
        textTable.add_row([' '] + self.__columnList)
        for i in range(8):
            row = [str(i + 1)]
            for j in range(8):
                entry = 'O'
                if grid[i][j] == 1:
                    entry = '#'
                if grid[i][j] == 0:
                    entry = 'X'
                row += [entry]
            textTable.add_row(row)
        print("==============Your planes==============")
        print(textTable.draw())
        print("==============Your planes==============")

    def __UIplacePlayerPlanes(self):
        print("You must place 2 planes first.")
        numberOfPlacedPlanes = 0
        while numberOfPlacedPlanes < 2:
            cabinCellString = input("Please provide the cell of the cabin (e.g. A3, C7, H5 etc.): ")
            cabinOrientationString = input("Please provide where the cabin should point to (up/down/left/right): ").lower()
            try:
                self.__gameController.placePlayerPlane(cabinCellString, cabinOrientationString)
                numberOfPlacedPlanes += 1
            except ValueError as error:
                print(str(error))

    def __UIprintPlayerInformation(self):
        playerPlanesGrid = self.__gameController.getPlayerPlanesGrid()
        playerShotsGrid = self.__gameController.getPlayerShotsGrid()
        self.__UIprintPlanesGrid(playerPlanesGrid)
        self.__UIprintShotsGrid(playerShotsGrid)

    def __UIplayerHitCell(self):
        receivedCorrectCell = False
        while receivedCorrectCell == False:
            cellString = input("Please provide the cell you would like to hit (e.g. A3, C7, H5 etc.): ")
            if InputValidator.checkIfCellIsCorrect(cellString) == False:
                print("Please provide a valid cell.")
            else:
                receivedCorrectCell = True
                hitResult = self.__gameController.makePlayerHit(cellString)
                print(self.__hitResults[hitResult].format("Player"))

    def __UIhittingPhasePlayerChoice(self):
        userChoiceInteger = 0
        while userChoiceInteger != 1:
            print("1. Hit a cell")
            print("2. View the planes grid and the hit grid")
            userChoiceString = input("Pick your choice: ")
            userChoiceInteger = InputValidator.getIntegerFromString(userChoiceString)
            if userChoiceInteger is None:
                print("Please enter a valid integer choice.")
                userChoiceInteger = 0
            else:
                if InputValidator.checkIfIntegerInInterval(1, 2, userChoiceInteger) is True:
                    if userChoiceInteger == 1:
                        self.__UIplayerHitCell()
                    else:
                        self.__UIprintPlayerInformation()
                else:
                    print("Please enter a valid choice between 1 and 2.")
                    userChoiceInteger = 0

    def __UIhittingPhaseComputerChoice(self):
        hitResult, cellPosition = self.__gameController.makeComputerHit()
        print(self.__hitResults[hitResult].format("Computer"))
        if hitResult != "miss":
            print("\tThe computer has hit " + GameConstants.coordinatesToCellString(cellPosition[0], cellPosition[1]))

    def __UIrunNewGame(self):
        self.__gameController.initializeNewGame()
        self.__UIplacePlayerPlanes()
        winner = self.__gameController.getGameWinner()
        while winner == "none":
            self.__UIhittingPhasePlayerChoice()
            self.__UIhittingPhaseComputerChoice()
            winner = self.__gameController.getGameWinner()
        if winner == "player":
            print("You have won! Congratulations!")
        else:
            print("You have lost! Don't worry, be happy! :)")

    def __UIendGamePrompt(self):
        userAnswer = input("Do you want to play another game? (yes/no): ")
        return userAnswer.lower()

    def UIrunApplication(self):
        '''
        This function makes a menu available to the user to operate with
        :return: nothing
        '''
        continuePlaying = True
        while continuePlaying is True:
            print("1. Start a new game")
            print("2. Exit the game")
            userChoiceString = input("Pick your choice: ")
            userChoiceInteger = InputValidator.getIntegerFromString(userChoiceString)
            if userChoiceInteger is None:
                print("Please enter a valid integer choice.")
            else:
                if InputValidator.checkIfIntegerInInterval(1, 2, userChoiceInteger) is True:
                    if userChoiceInteger == 1:
                        self.__UIrunNewGame()
                        userContinueAnswer = self.__UIendGamePrompt()
                        if userContinueAnswer == "no":
                            continuePlaying = False
                    else:
                        continuePlaying = False
                else:
                    print("Please enter a valid choice between 1 and 2.")
        self.__UIexitGame()
