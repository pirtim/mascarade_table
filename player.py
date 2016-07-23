# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import cards
import operator
from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

class Player(object):
    def __init__(self, index, name, card):
        self.index = index
        self.name = name
        self.card = card
        self.gold = 8

    def peek_card(self):
        logging.info('Player: ' + self.get_repr() + ' has peeeked.')

    def play_card(self, board):
        self.card.get_logic()(board, self)

    def potential_exchange_handler(self, players, players_names):   
        print 'Which player?'
        second_player = prompt_for_choice(players_names)
        second_player = players[second_player]
        execute = prompt_for_confirmation('Execute?')
        
        logging.info('Player: '
            + self.get_repr()
            + ' has'
            + str(' not ' if execute == 'N' else ' ')
            + 'exchanged '
            + self.card.name
            + ' for '
            + second_player.card.name
            + ' with '
            + second_player.get_repr() + '.')

        self.potential_exchange(second_player, execute)

    def potential_exchange(self, second_player, execute):
        if execute:
            self.card, second_player.card = second_player.card, self.card

    def get_repr(self):
        return '{}:{}({})'.format(self.index, self.name, self.gold)
        