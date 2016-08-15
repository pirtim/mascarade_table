import unittest
import datetime
import uuid
import logging
from types import FunctionType
from collections import namedtuple
from mock import patch, MagicMock, Mock

from .helper_test import *
from .. import inputs
from ..player import Player
from ..board import Board
from ..cards import cards, King, Queen, Bishop

class Test_Cards(unittest.TestCase):
    def setUp(self):
        self.b = Board(3,human_vec(3), ['Tom','Ben','Mat'], ['King', 'Queen', 'King'], 6)
        self.p = self.b.players['Tom']

    def test_card_isfunction(self):
        for card in cards.values():
            self.assertIsInstance(card, FunctionType)

    def test_King(self):
        self.assertEqual(King.name, 'King') 
        King(self.p, self.b)
        self.assertEqual(self.p.gold, 9)

    def test_Queen(self):
        self.assertEqual(Queen.name, 'Queen')
        Queen(self.p, self.b)
        self.assertEqual(self.p.gold, 8)

    def test_Bishop(self):
        self.assertEqual(self.p.gold, 6)
        self.assertEqual(Bishop.name, 'Bishop')
        with patch.object(inputs, 'prompt_for_choice', create=True, return_value = 'Ben'):
            Bishop(self.p, self.b)
        self.assertEqual(self.p.gold, 8)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
