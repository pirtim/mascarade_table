import unittest
import datetime
import uuid
import logging
import sys
from collections import namedtuple, OrderedDict
from mock import patch, MagicMock, Mock

from .helper_test import *
# from ..player import Player
from .. import player
from .. import cards
from .. import inputs
from ..bots import Human

King, Queen = cards.King, cards.Queen
# from ..cards import King, Queen

class Test_Player(unittest.TestCase):
    def setUp(self):
        self.p = player.Player(0, Human(), 'Tom', King(), 6)
        self.sp = player.Player(1, Human(), 'Mark', Queen(), 6)
        self.players_names = ['Tom', 'Mark']
        self.players = OrderedDict(zip(self.players_names,[self.p, self.sp]))
        # help_set_up()

    def test___init__(self):        
        self.assertEqual(self.p.index, 0)
        self.assertEqual(self.p.name, 'Tom')
        self.assertIsInstance(self.p.card, King)
        self.assertEqual(self.p.card.name, 'King')
        self.assertEqual(self.p.gold, 6)

    def test__play_card(self): 
        board = Mock()
        self.p.play_card(board)
        self.assertEqual(self.p.gold, 9)
        board.assert_not_called()
        self.sp.play_card(board)
        self.assertEqual(self.sp.gold, 8)
        board.assert_not_called()

#~ http://stackoverflow.com/questions/6271947/how-can-i-simulate-input-to-stdin-for-pyunit
    def test_potential_exchange_handler(self):
        self.p.potential_exchange = Mock()
        # with patch.object(player, 'prompt_for_choice', create=True, return_value='Mark'):
        #     with patch.object(player, 'prompt_for_confirmation', create=True, return_value=True):
        #         self.p.potential_exchange_handler(self.players, self.players_names)
        
        with patch.object(inputs, 'prompt_for_choice', create=True, return_value='Mark'):
            with patch.object(inputs, 'prompt_for_confirmation', create=True, return_value=True):
                self.p.potential_exchange_handler(self.players, self.players_names)
        
        self.p.potential_exchange.assert_called_once_with(self.sp, True)

    def test_potential_exchange_execute(self):
        self.assertIsInstance(self.p.card, King)
        self.assertIsInstance(self.sp.card, Queen)
        self.p.potential_exchange(self.sp, True)
        self.assertIsInstance(self.p.card, Queen)
        self.assertIsInstance(self.sp.card, King)

    def test_potential_exchange_nonexecute(self):
        self.assertIsInstance(self.p.card, King)
        self.assertIsInstance(self.sp.card, Queen)
        self.p.potential_exchange(self.sp, False)
        self.assertIsInstance(self.p.card, King)
        self.assertIsInstance(self.sp.card, Queen)

    def test_get_repr(self):
        self.assertEqual(self.p.get_repr(), '0:Tom(6)')

    def tearDown(self):
        pass
        # help_tear_down()

if __name__ == '__main__':
    unittest.main()
