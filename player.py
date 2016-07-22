# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import cards
import operator

class Player(object):
    def __init__(self, index, name, card):
        self.index = index
        self.name = name
        self.card = card
        self.gold = 8

    def peek_card(self):
        pass

    def play_card(self, board):
        self.card.get_logic()(board)

    def potential_exchange(self, second_player, execute):
        if execute:
            self.card, second_player.card = second_player.card, self.card

    def get_repr(self):
        return '{}:{}({})'.format(self.index, self.name, self.gold)
        