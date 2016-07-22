import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from .helper_test import *
from ..player import Player
from ..board import Board
from ..cards import *

class Test_Cards(unittest.TestCase):
    def setUp(self):
        # self.p = Player(0, 'Tom', King())
        self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'])
        # help_set_up()

    def tearDown(self):
        pass
        # help_tear_down()

if __name__ == '__main__':
    unittest.main()
