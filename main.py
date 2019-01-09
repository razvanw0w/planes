from interface.gameConsoleInterface import GameConsoleInterface
from interface.gameGraphicalInterface import GameGraphicalInterface
from controller import *
from repository.repository import Repository

# repositories
playerRepository = Repository()
computerRepository = Repository()

# controllers
playerController = PlayerController(playerRepository)
computerController = ComputerController(computerRepository)
gameController = GameController(playerController, computerController)

userChoice = input("console or gui?: ")

# interfaces
userInterface = GameConsoleInterface(gameController)
if userChoice == "gui":
    userInterface = GameGraphicalInterface(gameController)

# source code
userInterface.UIrunApplication()