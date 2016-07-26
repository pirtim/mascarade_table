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
        self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'], 6)
        self.p = self.b.players['Tom']

    def test_logic_isfunction(self):
        for card_name, card_cls in cards.iteritems():
            logic = card_cls().logic
            self.assertIsInstance(logic, FunctionType)

    def test_King(self):
        card = King()
        logic = card.logic
        self.assertEqual(card.name, 'King')
        logic(self.p, self.b)
        self.assertEqual(self.p.gold, 9)

    def test_Queen(self):
        card = Queen()
        logic = card.logic
        self.assertEqual(card.name, 'Queen')
        logic(self.p, self.b)
        self.assertEqual(self.p.gold, 8)

    def test_Bishop(self):
        self.assertEqual(self.p.gold, 6)
        card = Bishop()
        logic = card.logic
        self.assertEqual(card.name, 'Bishop')
        logic(self.p, self.b)
        self.assertEqual(self.p.gold, 8)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
