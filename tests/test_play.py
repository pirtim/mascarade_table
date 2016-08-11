import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from .helper_test import *
from ..player import Player
from ..board import Board
from ..cards import *
from ..bots import SimpleBot
from ..play import example_players_names, play

class Test_variables(unittest.TestCase):
    def test__example(self):
        self.assertEqual(len(example_players_names), 12)
        self.assertIn('Lisa',example_players_names)
        self.assertIn('Bob',example_players_names)

class Test_errors_play(unittest.TestCase):
    def test___init__(self):
        with self.assertRaisesRegexp(ValueError, r'Not enough players \(min: 3\)\.$'):
            play(2, ['human', 'human'],['Tom', 'Bob'], ['King', 'Queen'])
        with self.assertRaisesRegexp(ValueError, r'Not enough types of players \(should be: 3\)\.'):
            play(3, ['human', 'human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
        with self.assertRaisesRegexp(ValueError, r'Not enough names of players \(min: 3\)\.'):
            play(3, ['human', 'human','human'], ['Tom', 'Bob'], ['King', 'Queen', 'Bishop'])
        with self.assertRaisesRegexp(ValueError, r'Not enough types of cards \(min: 3\)\.'):
            play(3, ['human', 'human','human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen'])
        with self.assertRaisesRegexp(ValueError, r'Not recognized player type.'):
            play(3, ['human', 'xuman','human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
        with self.assertRaisesRegexp(ValueError, r'Not recognized bot type.'):
            class HardBot(object):
                pass
            play(3, ['human', HardBot,'human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])

class Test_bot_play(unittest.TestCase):
    def setUp(self):
        pass
        # self.b = Board(3,['Tom','Ben','Mat'], ['King', 'Queen', 'King'])
        # help_set_up()

    def test_normal_play(self):
        play(3, [SimpleBot, SimpleBot, SimpleBot], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()