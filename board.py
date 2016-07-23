# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import operator
import functools
from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

import cards
from player import Player

example_players_names_M = ['Chris', 'Tom', 'Marcus', 'Bob', 'Adam', 'Iris']
example_players_names_F = ['Iris', 'Eve', 'Julie', 'Lisa', 'Mary', 'Tara']
example_players_names = example_players_names_M + example_players_names_F

# http://stackoverflow.com/a/31174427
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

sentinel = object()
def rgetattr(obj, attr, default=sentinel):
    if default is sentinel:
        _getattr = getattr
    else:
        def _getattr(obj, name):
            return getattr(obj, name, default)
    return functools.reduce(_getattr, [obj]+attr.split('.'))

def gen_next_players_list(players_list, index):
    for i in players_list[index+1:]:
        yield i
    for i in players_list[:index]:
        yield i

class Board(object):
    def __init__(self, players_num, players_names, cards_names = None):
        self.players_num = players_num
        self.players_names = players_names        
        self.cards_names = cards_names
        self.players = OrderedDict()
        for index, name in enumerate(self.players_names):
            self.players[name] = Player(index, name, cards.cards[cards_names[index]]())
        self.current_player = self.players.items()[0][1]
        self.court = 0
        self.round_num = 0

    def reshufle_cards(self):
        return NotImplemented

    def next_step(self):
        logging.info('Start of round number {}'.format(self.round_num))
        logging.debug('Players Cards: {}'.format(self.method_from_players('card.name')))
        logging.debug('Players Gold: {}'.format(self.method_from_players('gold')))

        print '{}, what do you do?'.format(self.current_player.get_repr())
        decision = prompt_for_choice(['PEEK', 'ANNOUNCE', 'EXCHANGE'])

        if decision == 'PEEK':            
            self.current_player.peek_card()

        elif decision == 'ANNOUNCE':
            print 'What do you announce?'
            what_declare = prompt_for_choice(set(self.cards_names))

            logging.info('Player: ' + self.current_player.get_repr() + ' has declared ' 
                        + what_declare + '.')

            # for name, index in gen_next_players_list(self.method_from_players('index').items(), self.current_player.index):
            for name in gen_next_players_list(self.players_names, self.current_player.index):
                claim = prompt_for_confirmation('{}, do you claim {} yourself?'.format(
                                                self.players[name].get_repr(), what_declare))
                if claim:
                    print name
                # print self.method_from_players('card.name')

            logging.info('Player: ' + self.current_player.get_repr() + ' has declared ' + self.current_player.card.name + '.')
            self.current_player.play_card(self)

        elif decision == 'EXCHANGE':
            print 'Which player?'
            second_player = prompt_for_choice(self.players_names)
            second_player = self.players[second_player]
            execute = prompt_for_confirmation('Execute?')
            
            logging.info('Player: '
                + self.current_player.get_repr()
                + ' has'
                + str(' not ' if execute == 'N' else ' ')
                + 'exchanged '
                + self.current_player.card.name
                + ' for '
                + second_player.card.name
                + ' with '
                + second_player.get_repr() + '.')
            self.current_player.potential_exchange(second_player, execute)
        else:
            raise ValueError

        if self.check_end_condition():
            logging.info('End of game at round number {}'.format(self.round_num))
            logging.info('Player {} won!'.format('Not Implemented'))
            logging.debug('Players Gold: {}'.format(self.method_from_players('gold')))
            return True

        self.next_player()
        return False

    def next_player(self):
        self.current_player = self.players.items()[(self.current_player.index + 1) % self.players_num][1]
        self.round_num += 1    

    def method_from_players(self, method):
        return OrderedDict([(key,rgetattr(value, method)) for key, value in self.players.iteritems()])

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
        gold = self.method_from_players('gold')
        return max(gold.iteritems(), key=lambda x: x[1])

    def min_rich_player(self):        
        '''Returns tuple(poorest_player, his_gold)'''
        gold = self.method_from_players('gold')
        return min(gold.iteritems(), key=lambda x: x[1])
