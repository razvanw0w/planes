'''
PlaneValidator class - validates if a plane can be places in a 8x8 grid
'''

import unittest

class PlaneValidator:
    @staticmethod
    def checkPlane(plane):
        '''
        This function checks if the user typed valid cabin information in
        :param plane: the given plane
        :return: True if both the strings represent valid cabin information
                 False otherwise
        '''
        directions = ["up", "down", "left", "right"]
        columns = "ABCDEFGH"
        rows = "12345678"
        cabinCellString = plane.getCabinLocation()
        cabinOrientation = plane.getCabinOrientation()

        if len(cabinCellString) != 2:
            return False
        if cabinOrientation not in directions:
            return False
        if cabinCellString[0] not in columns:
            return False
        if cabinCellString[1] not in rows:
            return False
        return True

    @staticmethod
    def checkPlaneCells(plane):
        '''
        This function checks if a plane can be placed in the grid
        :param plane: a given plane - Plane
        :return: True if the plane can be placed in the grid
                 False otherwise
        '''
        planeCells = plane.getPlaneCellsList()
        for planeCell in planeCells:
            row = planeCell[0]
            column = planeCell[1]
            if row not in range(8):
                return False
            if column not in range(8):
                return False
        return True

class TestPlaneValidator(unittest.TestCase):
    def testCheckPlane(self):
        from model.plane import Plane
        plane = Plane("a", "down")
        self.assertFalse(PlaneValidator.checkPlane(plane))
        plane = Plane("A3", "right")
        self.assertTrue(PlaneValidator.checkPlane(plane))
        plane = Plane("9A", "eee")
        self.assertFalse(PlaneValidator.checkPlane(plane))
        plane = Plane("A9", "up")
        self.assertFalse(PlaneValidator.checkPlane(plane))
        plane = Plane("K9", "down")
        self.assertFalse(PlaneValidator.checkPlane(plane))
        plane = Plane("C7", "right")
        self.assertTrue(PlaneValidator.checkPlane(plane))

    def testCheckPlaneCells(self):
        from model.plane import Plane
        plane = Plane("A5", "left")
        self.assertTrue(PlaneValidator.checkPlaneCells(plane))
        plane = Plane("A5", "right")
        self.assertFalse(PlaneValidator.checkPlaneCells(plane))