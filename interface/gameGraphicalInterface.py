'''
GameGraphicalInterface class
'''

from tkinter import *
from tkinter import messagebox
from utilities.matrixGenerator import MatrixGenerator
from copy import deepcopy
from validation.inputValidator import InputValidator
from controller.gameController import GameController
from utilities.gameConstants import GameConstants

class GameGraphicalInterface:
    def __init__(self, gameController):
        self.__gameController = gameController
        self.__columnList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.__hitResults = {"hit": "{} has hit a cell!", "cabin": "{} has destroyed a plane!", "miss": "{} missed!"}
        self.__root = Tk()
        self.__planesGridFrame = Frame(self.__root)
        self.__shotsGridFrame = Frame(self.__root)
        self.__externalFrame = Frame(self.__root)
        self.__planesGrid = MatrixGenerator.generateMatrix(8, 8, -1)
        self.__shotsGrid = MatrixGenerator.generateMatrix(8, 8, -1)
        self.__planesGridButtonMatrix = MatrixGenerator.generateMatrix(8, 8)
        self.__shotsGridButtonMatrix = MatrixGenerator.generateMatrix(8, 8)
        self.__drawnPlanesCounter = 0
        self.__isHittingPhase = False

    def __GUIpackFrames(self):
        self.__planesGridFrame.pack()
        self.__externalFrame.pack()
        self.__shotsGridFrame.pack()

    def __onPlanesGridButtonClick(self, row, column):
        if self.__isHittingPhase == True:
            messagebox.showinfo("Error", "It is hitting phase, you can't touch your planes anymore.")
        elif self.__planesGrid[row][column] == 1:
            messagebox.showinfo("Error", "You clicked an already set plane's tile!")
        else:
            if self.__planesGrid[row][column] == -1:
                self.__planesGrid[row][column] = 2
                self.__planesGridButtonMatrix[row][column].configure(background = "yellow")
            else:
                self.__planesGrid[row][column] = -1
                self.__planesGridButtonMatrix[row][column].configure(background = "gray")

    def __GUIplayerHit(self, row, column):
        hitResult = self.__gameController.makePlayerHit(GameConstants.coordinatesToCellString(row, column))
        self.__listBox.delete(0, self.__listBox.size() - 1)
        if hitResult == "miss":
            self.__shotsGridButtonMatrix[row][column].configure(background = "red")
            self.__listBox.insert(0, "You have missed!")
        else:
            self.__shotsGridButtonMatrix[row][column].configure(background = "green")
            if hitResult == "hit":
                self.__listBox.insert(0, "You have hit a cell at " + GameConstants.coordinatesToCellString(row, column))
            else:
                self.__listBox.insert(0, "You have destroyed a plane at " + GameConstants.coordinatesToCellString(row, column))

    def __GUIcomputerHit(self):
        hitResult, cellPosition = self.__gameController.makeComputerHit()
        if cellPosition is not None:
            row = cellPosition[0]
            column = cellPosition[1]
        if hitResult == "miss":
            self.__listBox.insert(1, "The computer has missed!")
        else:
            self.__planesGridButtonMatrix[row][column].configure(background = "red")
            if hitResult == "hit":
                self.__listBox.insert(1, "The computer has hit a cell at " + GameConstants.coordinatesToCellString(row, column))
            else:
                self.__listBox.insert(1, "The computer has destroyed your plane at " + GameConstants.coordinatesToCellString(row, column))
            
    def __onShotsGridButtonClick(self, row, column):
        if self.__isHittingPhase == False:
            messagebox.showinfo("Error", "It is plane setting phase, you can't hit the computer's planes.")
        else:
            self.__GUIplayerHit(row, column)
            self.__GUIcomputerHit()
            winner = self.__gameController.getGameWinner()
            if winner != "none":
                if winner == "player":
                    messagebox.showinfo("Winner!", "You have won!")
                else:
                    messagebox.showinfo("Winner!", "The computer has won!")
                self.__initializeGUI()

    def __GUIcreatePlanesGrid(self):
        for i in range(8):
            for j in range(8):
                button = Button(self.__planesGridFrame,
                                command = lambda pair = (i, j): self.__onPlanesGridButtonClick(pair[0], pair[1]), width = 2,
                                background = "gray")
                self.__planesGridButtonMatrix[i][j] = button
                self.__planesGridButtonMatrix[i][j].grid(row = i, column = j)

    def __GUIvalidatePlane(self):
        for i in range(8):
            for j in range(8):
                if self.__planesGrid[i][j] == 2:
                    self.__planesGrid[i][j] = 1
                    self.__planesGridButtonMatrix[i][j].configure(background = "green")

    def __drawPlane(self):
        validationAnswer, cabinLocation, cabinOrientation = InputValidator.checkIfDrawnPlaneIsCorrect(self.__planesGrid)
        if validationAnswer == False:
            messagebox.showinfo("Error", "You haven't drawn a valid plane. Please try again!")
        else:
            self.__GUIvalidatePlane()
            self.__drawnPlanesCounter += 1
            self.__gameController.placePlayerPlane(cabinLocation, cabinOrientation)
            if self.__drawnPlanesCounter == 2:
                self.__isHittingPhase = True
                self.__listBox.delete(0, self.__listBox.size() - 1)
                self.__listBox.insert(0, "It is hitting phase now, hit a cell!")

    def __GUIcreateExternalObjects(self):
        self.__listBox = Listbox(self.__externalFrame, width = 55, height = 3)
        self.__listBox.grid(row = 0, column = 0)
        self.__drawPlaneButton = Button(self.__externalFrame, text = "Draw plane", command = self.__drawPlane)
        self.__drawPlaneButton.grid(row = 1, column = 0)

    def __GUIcreateShotsGrid(self):
        for i in range(8):
            for j in range(8):
                button = Button(self.__shotsGridFrame,
                                command = lambda pair = (i, j): self.__onShotsGridButtonClick(pair[0], pair[1]), width = 2,
                                background = "gray")
                self.__shotsGridButtonMatrix[i][j] = button
                self.__shotsGridButtonMatrix[i][j].grid(row = i, column = j)

    def __drawGUI(self):
        self.__root.title("Planes")
        self.__GUIpackFrames()
        self.__GUIcreatePlanesGrid()
        self.__GUIcreateExternalObjects()
        self.__GUIcreateShotsGrid()

    def __initializeGUI(self):
        self.__gameController.initializeNewGame()
        self.__drawnPlanesCounter = 0
        self.__isHittingPhase = False
        self.__initializeGraphicalMatrices()
        self.__initializeListbox()

    def __initializeGraphicalMatrices(self):
        for i in range(8):
            for j in range(8):
                self.__shotsGridButtonMatrix[i][j].configure(bg = "gray")
                self.__planesGridButtonMatrix[i][j].configure(bg = "gray")
                self.__planesGrid[i][j] = -1
                self.__shotsGrid[i][j] = -1

    def __initializeListbox(self):
        self.__listBox.delete(0, self.__listBox.size() - 1)
        self.__listBox.insert(0, "Please draw two planes to begin the game.")
        self.__listBox.insert(1, "Please press the 'draw plane' button after you drew one plane.")

    def UIrunApplication(self):
        self.__drawGUI()
        self.__initializeGUI()
        self.__root.mainloop()