import unittest
import datetime
import uuid
import logging
from collections import namedtuple, OrderedDict

from .helper_test import *
from ..player import Player
from ..board import Board, PlayerVal
from ..cards import *

class Test_Board(unittest.TestCase):
    def setUp(self):
        self.b = Board(3, human_vec(3), ['Tom','Ben','Mat'], ['King', 'Queen', 'King'],  6)

    def test_end_condition_over(self):
        self.assertFalse(self.b.true_history.has_key('game_result'))
        self.b.players['Tom'].gold = 13
        self.b.check_end_condition()
        self.assertTrue(self.b.true_history.has_key('game_result'))
        game_result = OrderedDict([
            ('type_of_end', 'rich_win'),
            ('name', 'Tom'),
            ('gold', 13),
            ('info', None)
            ])
        self.assertEqual(self.b.true_history['game_result'], game_result)

    def test_end_condition_under(self):        
        self.assertFalse(self.b.true_history.has_key('game_result'))
        self.b.players['Tom'].gold = 0
        self.b.check_end_condition()
        self.assertTrue(self.b.true_history.has_key('game_result'))
        game_result = OrderedDict([
            ('type_of_end', 'poor_win'),
            ('name', 'Ben'),
            ('gold', 6),
            ('info', None)
            ])
        self.assertEqual(self.b.true_history['game_result'], game_result)

    def test_max_rich_player1(self):
        result = self.b.max_rich_player()
        self.assertIsInstance(result, list) 
        self.assertEqual(len(result), 3)

    def test_max_rich_player2(self):
        self.b.players['Tom'].gold += 1
        result = self.b.max_rich_player()
        self.assertIsInstance(result, list) 
        self.assertListEqual(result, [('Tom', 7)]) 
        self.assertEqual(len(result), 1)

    def test_min_rich_player(self):
        result = self.b.min_rich_player()
        self.assertIsInstance(result, list) 
        self.assertEqual(len(result), 3)

    def test_min_rich_player2(self):
        self.b.players['Tom'].gold += 1
        result = self.b.min_rich_player()
        self.assertIsInstance(result, list) 
        self.assertListEqual(result, [('Ben', 6), ('Mat', 6)]) 
        self.assertEqual(len(result), 2)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
