# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import cards
import operator
# from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice
from inputs import input_for_confirmation, input_for_choice

class Player(object):
    def __init__(self, index, bot, name, card, gold):
        self.index = index
        self.bot = bot
        self.name = name
        self.card = card
        self.gold = gold
        self.history = None

    def peek_card(self):
        logging.info('Player: ' + self.get_repr() + ' has peeeked.')

    def play_card(self, board):
        self.card.logic(self, board)

    def potential_exchange_handler(self, players, players_names):   
        # print 'Which player?'
        # second_player = prompt_for_choice(players_names)

        question = 'Which player?'
        choices = players_names
        second_player = input_for_choice(self, question, choices)

        second_player = players[second_player]
        # execute = prompt_for_confirmation('Execute?')        
        execute = input_for_confirmation(self, question='Execute?')
        
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
        