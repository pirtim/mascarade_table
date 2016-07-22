import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from .helper_test import *
from ..player import Player
from ..board import Board
from ..cards import *
from ..main import example_players_names, play

class Test_variables(unittest.TestCase):
    def test__example(self):
        self.assertEqual(len(example_players_names), 12)
        self.assertIn('Lisa',example_players_names)
        self.assertIn('Bob',example_players_names)

class Test_errors_play(unittest.TestCase):
    def test___init__(self):
        self.assertRaises(ValueError, play, 3, ['Tom', 'Bob'], ['King', 'Queen', 'Bishop'])
        self.assertRaises(ValueError, play, 3, ['Tom', 'Bob', 'Mat'], ['King', 'Queen'])

class Test_play(unittest.TestCase):
    def setUp(self):
        # self.p = Player(0, 'Tom', King())
        self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'])
        # help_set_up()

    def tearDown(self):
        pass
        # help_tear_down()

if __name__ == '__main__':
    unittest.main()
