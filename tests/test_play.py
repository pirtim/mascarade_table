import unittest
import datetime
import uuid
import logging
from collections import namedtuple, OrderedDict
from mock import patch, MagicMock, Mock

from .. import inputs
from .helper_test import *
from ..player import Player
from ..board import Board, GameHistory
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
            play(3, ['human', 'human', 'human'], ['Tom', 'Bob'], ['King', 'Queen', 'Bishop'])
        with self.assertRaisesRegexp(ValueError, r'Not enough types of cards \(min: 3\)\.'):
            play(3, ['human', 'human', 'human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen'])
        with self.assertRaisesRegexp(ValueError, r'Not recognized player type.'):
            play(3, ['human', 'xuman', 'human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
        with self.assertRaisesRegexp(ValueError, r'Not recognized bot type.'):
            class HardBot(object):
                pass
            play(3, ['human', HardBot,'human'], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])

class Test_bot_play(unittest.TestCase):
    def test_normal_play(self):
        play(3, [SimpleBot, SimpleBot, SimpleBot], ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])

class Test_human_play_1(unittest.TestCase):
    def test_normal_play_1(self):
        with patch.object(inputs, 'prompt_for_choice', create=True, side_effect = ['ANNOUNCE','King']*7):
            with patch.object(inputs, 'prompt_for_confirmation', create=True, side_effect = [False]*14):
                result = play(3, ['human']*3, ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
                self.assertIsInstance(result, GameHistory)
                self.assertIsInstance(result, OrderedDict)
                game_result = OrderedDict([
                    ('type_of_end', 'rich_win'),
                    ('name', 'Tom'),
                    ('gold', 15),
                    ('info', None)
                    ])
                self.assertEqual(result['game_result'], game_result)

    def test_normal_play_2(self):
        choices = ['ANNOUNCE','King', 'PEEK', 'PEEK']*3
        confirmation = [True, True]*3
        with patch.object(inputs, 'prompt_for_choice', create=True, side_effect=choices):
            with patch.object(inputs, 'prompt_for_confirmation', create=True, side_effect=confirmation):
                result = play(3, ['human']*3, ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
                game_result = OrderedDict([
                    ('type_of_end', 'rich_win'),
                    ('name', 'Tom'),
                    ('gold', 15),
                    ('info', None)
                    ])
                self.assertEqual(result['game_result'], game_result)

    def test_normal_play_3(self):
        choices = ['ANNOUNCE','Queen', 'PEEK', 'PEEK']*6
        confirmation = [False, True]*6
        with patch.object(inputs, 'prompt_for_choice', create=True, side_effect=choices):
            with patch.object(inputs, 'prompt_for_confirmation', create=True, side_effect=confirmation):
                result = play(3, ['human']*3, ['Tom', 'Bob', 'Mat'], ['King', 'Queen', 'Bishop'])
                game_result = OrderedDict([
                    ('type_of_end', 'poor_win'),
                    ('name', 'Bob'),
                    ('gold', 6),
                    ('info', None)
                    ])
                self.assertEqual(result['game_result'], game_result)

    def test_normal_play_4(self):
        N = 6        
        choices = ['PEEK']*N
        choices += ['PEEK', 'PEEK', 'PEEK', 'PEEK', 'ANNOUNCE', 'Queen', 'PEEK']
        choices += ['PEEK', 'PEEK', 'PEEK', 'PEEK', 'ANNOUNCE', 'Queen', 'PEEK']
        choices += ['PEEK', 'PEEK', 'PEEK', 'PEEK', 'ANNOUNCE', 'Cheat']
        confirmation = [False]*5*2
        confirmation += [True]*5
        with patch.object(inputs, 'prompt_for_choice', create=True, side_effect=choices):
            with patch.object(inputs, 'prompt_for_confirmation', create=True, side_effect=confirmation): 
                my_minds = ['human'] * N
                cards_names = ['King', 'Queen', 'Bishop', 'Judge', 'Cheat', 'Witch']
                result = play(players_num=N,  types_of_players=my_minds, cards_names=cards_names)
                game_result = OrderedDict([
                    ('type_of_end', 'rich_win'),
                    ('name', 'Adam'),
                    ('gold', 10),
                    ('info', 'cheat_win')
                    ])
                self.assertEqual(result['game_result'], game_result)

if __name__ == '__main__':
    unittest.main()
