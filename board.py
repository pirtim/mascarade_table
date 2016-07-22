# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import cards
import operator
from player import Player

example_players_names_M = ['Chris', 'Tom', 'Marcus', 'Bob', 'Adam', 'Iris']
example_players_names_F = ['Iris', 'Eve', 'Julie', 'Lisa', 'Mary', 'Tara']
example_players_names = example_players_names_M + example_players_names_F

class Board(object):
    def __init__(self, players_num, players_names, cards_names = None):
        self.players_num = players_num
        self.players_names = players_names
        self.players = OrderedDict()
        for index, name in enumerate(self.players_names):
            self.players[name] = Player(index, name, cards.King())
        self.current_player = self.players.items()[0][1]
        self.court = 0
        self.round_num = 0

    def next_step(self):
        logging.info('Start of round number {}'.format(self.round_num))
        logging.debug('Players Gold: {}'.format(self.gold_from_players()))

        print '{}({}), what do you do?'.format(self.current_player.name, self.current_player.gold)
        decision = raw_input('PEEK, DECL, EXCH?').upper()
        if decision == 'PEEK' or decision == 'P':
            logging.info('Player: ' + self.current_player.get_repr() + ' has peeeked.')
            self.current_player.peek_card()

        elif decision == 'DECL' or decision == 'D':
            logging.info('Player: ' + self.current_player.get_repr() + ' has declared ' + self.current_player.card.name + '.')
            self.current_player.play_card(self)

        elif decision == 'EXCH' or decision == 'E':
            second_player = raw_input('Which player?')
            if second_player not in self.players_names:
                raise ValueError

            execute = raw_input('Execute [Y/N]?').upper()
            if execute != 'Y' or execute != 'N':
                raise ValueError 
            
            logging.info('Player: ' + self.current_player.get_repr() + ' has exchanged with ' + second_player + '.')
            self.current_player.potential_exchange(second_player, execute == 'Y')

        else:
            raise ValueError

        if self.check_end_condition():
            logging.info('End of game at round number {}'.format(self.round_num))
            logging.info('Player {} won!'.format('Not Implemented'))
            logging.debug('Players Gold: {}'.format(self.gold_from_players()))
            return True

        self.next_player()
        return False

    def next_player(self):
        # logging.debug('index:{}, index+1:{}, num:{}, nowy:{}'.format(
        #     self.current_player.index, 
        #     self.current_player.index + 1, 
        #     self.players_num, 
        #     (self.current_player.index + 1) % self.players_num
        #     ))
        self.current_player = self.players.items()[(self.current_player.index + 1) % self.players_num][1]
        self.round_num += 1
    
    def gold_from_players(self):
        return {key:value.gold for key, value in self.players.iteritems()}

    def check_end_condition(self):
        'przepisac'
        richest = self.max_rich_player()
        poorest = self.min_rich_player()
        if richest[1] >= 12:
            return True        
        if poorest[1] <= 0:
            return True        
        return False        

    def max_rich_player(self):        
        '''Returns tuple(richest_player, his_gold)'''
        gold = self.gold_from_players()
        return max(gold.iteritems(), key=lambda x: x[1])

    def min_rich_player(self):        
        '''Returns tuple(poorest_player, his_gold)'''
        gold = self.gold_from_players()
        return min(gold.iteritems(), key=lambda x: x[1])
