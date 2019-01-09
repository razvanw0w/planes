'''
Plane class - abstractization of a plane
'''

from utilities.gameConstants import GameConstants
import unittest

class Plane:
    def __init__(self, cabinLocation, cabinOrientation):
        '''
        The initialiser of the Plane object
        :param cabinLocation: the location of the plane
        :param cabinOrientation: the orientation of the plane
        '''
        self.__cabinLocation = cabinLocation
        self.__cabinOrientation = cabinOrientation

    def getCabinLocation(self):
        '''
        cabinLocation getter
        :return: cabinLocation - the location of the cabin
        '''
        return self.__cabinLocation

    def getCabinOrientation(self):
        '''
        cabinOrientation getter
        :return: cabinOrientation - the orientation of the cabin
        '''
        return self.__cabinOrientation

    def getPlaneCellsList(self):
        '''
        This function generates a list of cells which represent the cells of the plane
        :return: cells - the list described above
        '''
        directions = GameConstants.directions[self.__cabinOrientation][:]
        sign = GameConstants.directionSign[self.__cabinOrientation]
        cells = []
        cabinLocation = GameConstants.cellStringToCoordinates(self.__cabinLocation)
        for direction in directions:
            newRow = cabinLocation[0] + sign * direction[0]
            newColumn = cabinLocation[1] + sign * direction[1]
            cells.append((newRow, newColumn))
        return cells

class TestPlane(unittest.TestCase):
    def testGetCabinLocation(self):
        plane = Plane("A5", "left")
        self.assertEqual(plane.getCabinLocation(), "A5")
        plane = Plane("F5", "down")
        self.assertEqual(plane.getCabinLocation(), "F5")

    def testGetCabinOrientation(self):
        plane = Plane("A5", "left")
        self.assertEqual(plane.getCabinOrientation(), "left")
        plane = Plane("F5", "down")
        self.assertEqual(plane.getCabinOrientation(), "down")

    def testGetPlaneCellsList(self):
        plane = Plane("A5", "left")
        cellsList = plane.getPlaneCellsList()
        realCellsList = [(4, 0), (3, 1), (4, 1), (5, 1), (4, 2), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3)]
        for cell in realCellsList:
            if cell not in cellsList:
                assert False