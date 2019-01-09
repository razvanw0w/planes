'''
Queue class - used in a BFS-like strategy for the computer moves
'''

import unittest

class Queue:
    def __init__(self):
        '''
        Initialiser of the Queue class
        '''
        self.__data = []

    def push(self, item):
        '''
        This function pushes an item into the queue (at the end of the queue)
        :param item: the given item
        :return: nothing
        '''
        self.__data.append(item)

    def pop(self):
        '''
        This function deletes the first item of the queue and returns it
        :return: item - the first item in the queue
                 None if there are no elements in the queue
        '''
        if len(self.__data) == 0:
            return None
        return self.__data.pop(0)

    def size(self):
        '''
        This function returns the number of the elements in the queue
        :return: size - integer
        '''
        return len(self.__data)

    def clear(self):
        '''
        This function empties the queue
        :return: nothing
        '''
        self.__data.clear()

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def testPushPopSize(self):
        self.queue.push(1)
        self.queue.push(2)
        self.assertEqual(self.queue.size(), 2)
        self.queue.push(3)
        self.assertEqual(self.queue.size(), 3)
        self.assertEqual(self.queue.pop(), 1)
        self.assertEqual(self.queue.pop(), 2)
        self.assertEqual(self.queue.pop(), 3)

    def testClear(self):
        self.queue.push(1)
        self.queue.push(1)
        self.queue.push(1)
        self.assertEqual(self.queue.size(), 3)
        self.queue.clear()
        self.assertEqual(self.queue.size(), 0)