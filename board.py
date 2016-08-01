# -*- coding: utf-8 -*-
#pylint: disable=W1202
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import operator
import functools
# from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

import cards
from player import Player
from inputs import input_for_confirmation, input_for_choice


# dodac named tuple na (player, val), bedzie ladniej
PlayerVal = namedtuple('PlayerVal', ['name', 'val'])
OrderedDictPlayers = OrderedDict
OrderedDictPlayers.items_p = lambda self: [PlayerVal(key, val) for key, val in self.items()]
OrderedDictPlayers.iteritems_p = lambda self: (PlayerVal(key, val) for key, val in self.iteritems())

class PublicBoard(object):
    def __init__(self, players_with_gold, public_history):
        self.players_with_gold = players_with_gold
        self.public_history = public_history

# PublicBoard = namedtuple('PublicBoard', ['players_with_gold'])

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
    def __init__(self, players_num, players_names, cards_names, start_gold, bots=None):
        self.players_num = players_num
        self.bots = bots
        self.players_names = players_names        
        self.cards_names = cards_names
        self.players = OrderedDict()
        for index, name in enumerate(self.players_names):
            if bots != None:
                self.players[name] = Player(index, name, cards.cards[cards_names[index]](), start_gold, bots[index])
            else:
                self.players[name] = Player(index, name, cards.cards[cards_names[index]](), start_gold)
        self.current_player = self.players.items()[0][1]
        self.court = 0
        self.round_num = 0
        self.public_history = None
        self.true_history = None
        self.public_board = PublicBoard(self.method_from_players('gold'), self.public_history)

        for name, player in self.players.iteritems():
            # czy to zadziala?
            if player.bot != None:
                player.bot.public_board = self.public_board

    # def get_public_board(self):
    #     '''
    #     Returns tuple, eg: (OrderedDictPlayers('Tom' : 8, 'Mark' : 6, ...), PublicHistory())
    #     Example:
    #     >>> my_board = Board(4, ['Tom', 'Mark', 'Bob', 'Chris'], ['King', 'Queen', 'Judge', 'Bishop'],  6)
    #     >>> pb = my_board.get_public_board()
    #     >>> pb.players_with_gold
    #     OrderedDict([('Tom', 6), ('Mark', 6), ('Bob', 6), ('Chris', 6)])
    #     >>> pb.players_with_gold['Tom']
    #     6
    #     >>> pb.players_with_gold.items_p()[0].name
    #     'Tom'
    #     '''
    #     return PublicBoard(self.method_from_players('gold'), self.public_history)

    def reshufle_cards(self):
        return NotImplemented

    def next_step(self):
        logging.info('Start of round number {}'.format(self.round_num))
        logging.debug('Players Cards: {}'.format(self.method_from_players('card.name')))
        logging.debug('Players Gold: {}'.format(self.method_from_players('gold')))

        print '{}, what do you do?'.format(self.current_player.get_repr())
        decision = prompt_for_choice(['PEEK', 'ANNOUNCE', 'EXCHANGE'])
    
        # question = '{}, what do you do?'.format(self.current_player.get_repr())
        # choices = ['PEEK', 'ANNOUNCE', 'EXCHANGE']
        # decision = input_for_choice(self.current_player, question, choices)

        if decision == 'PEEK':            
            self.current_player.peek_card()
        elif decision == 'ANNOUNCE':
            self.announcement()
        elif decision == 'EXCHANGE':
            self.current_player.potential_exchange_handler(self.players, self.players_names)

        if self.check_end_condition():
            logging.info('End of game at round number {}'.format(self.round_num))
            logging.info('Player {} won!'.format('Not Implemented'))
            logging.debug('Players Gold: {}'.format(self.method_from_players('gold')))
            return True

        self.next_player()
        return False

    def announcement(self):
        print 'What do you announce?'
        what_declare = prompt_for_choice(set(self.cards_names))
        logging.info('Player: ' + self.current_player.get_repr() + ' has declared ' 
                    + what_declare + '.')

        # for name, index in gen_next_players_list(self.method_from_players('index').items(), self.current_player.index):
        claimants = []
        for name in gen_next_players_list(self.players_names, self.current_player.index):
            claim = prompt_for_confirmation('{}, do you claim {} yourself?'.format(
                                            self.players[name].get_repr(), what_declare))
            if claim:
                claimants.append(name) 
                logging.info('{} has claimed {}.'.format(self.players[name].get_repr(), what_declare))

        if claimants:
            claimants = [self.current_player.name] + claimants            
            claimants_with_cards = self.method_from_players('card.name', claimants)         

            for name, card_name in claimants_with_cards.iteritems():
                if card_name == what_declare:
                    self.players[name].play_card(self)
                    logging.info('{} said the truth. He is a {}.'.format(self.players[name].get_repr(), what_declare))
                else:
                    self.players[name].gold -= 1 
                    self.court += 1
                    logging.info('{} lied. He really is a {}, not a {}.'.format(self.players[name].get_repr(), self.players[name].card.name, what_declare))

    def next_player(self):
        self.current_player = self.players.items()[(self.current_player.index + 1) % self.players_num][1]
        self.round_num += 1

    def method_from_players(self, method, players=None):
        if players == None:
            players = self.players
        if hasattr(players, 'iteritems'):
            return OrderedDictPlayers([(key,rgetattr(value, method)) for key, value in players.iteritems()])
        else:
            return OrderedDictPlayers([(name,rgetattr(self.players[name], method)) for name in players])

    def check_end_condition(self):
        'przepisac'
        richest = self.max_rich_player()
        poorest = self.min_rich_player()
        if richest[0].val >= 12:
            return True
        if poorest[0].val <= 0:
            return True
        return False

    def max_rich_player(self, all_players = False):
        '''Returns list(tuple(richest_player1, his_gold),tuple(richest_player2, his_gold),...)'''
        gold = self.method_from_players('gold')
        gold_sorted = sorted(gold.iteritems_p(), key=lambda x:-x.val)
        if all_players:
            return gold_sorted
        else:   
            return filter(lambda x: x.val == gold_sorted[0].val, gold_sorted)

    def min_rich_player(self, all_players = False):     
        '''Returns list(tuple(poorest_player1, his_gold),tuple(poorest_player2, his_gold),...)'''
        gold = self.method_from_players('gold')
        gold_sorted = sorted(gold.iteritems_p(), key=lambda x:+x.val) 
        if all_players:
            return gold_sorted
        else:   
            return filter(lambda x: x.val == gold_sorted[0].val, gold_sorted)

if __name__ == "__main__":
    import doctest
    doctest.testmod()