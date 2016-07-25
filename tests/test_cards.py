import unittest
import datetime
import uuid
import logging
from types import FunctionType
from collections import namedtuple


from .helper_test import *
from ..player import Player
from ..board import Board
from ..cards import *

class Test_Cards(unittest.TestCase):
    def setUp(self):
        # self.p = Player(0, 'Tom', King(), 6)
        self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'], 6)
        # help_set_up()


    def test_logic_isfunction(self):
        for card_name, card_cls in cards.iteritems():
            logic = card_cls().logic
            self.assertIsInstance(logic, FunctionType)

    def test_King(self):
        card = King()
        logic = card.logic
        self.assertEqual(card.name, 'King')
        self.assertIsInstance(logic, FunctionType)

    def tearDown(self):
        pass
        # help_tear_down()



if __name__ == '__main__':
    unittest.main()
