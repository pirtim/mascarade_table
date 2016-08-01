import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from .helper_test import *
from ..player import Player
from ..board import Board
from ..cards import *
from ..main_human import example_players_names, play

class Test_variables(unittest.TestCase):
    def test__example(self):
        self.assertEqual(len(example_players_names), 12)
        self.assertIn('Lisa',example_players_names)
        self.assertIn('Bob',example_players_names)

class Test_errors_play(unittest.TestCase):
    def test___init__(self):
        self.assertRaises(ValueError, play, 3, ['Tom', 'Bob'], ['King', 'Queen', 'Bishop'])
        self.assertRaises(ValueError, play, 3, ['Tom', 'Bob', 'Mat'], ['King', 'Queen'])
        self.assertRaises(ValueError, play, 2, ['Tom', 'Bob', 'Mat'], ['King', 'Queen'])

class Test_play(unittest.TestCase):
    def setUp(self):
        pass
        # self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'])
        # help_set_up()

    # def test_normal_play(self):

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
