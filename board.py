# -*- coding: utf-8 -*-
#pylint: disable=W1202
from __future__ import division

import functools
import logging
import operator
from collections import OrderedDict, namedtuple

import cards
from inputs import input_for_choice, input_for_confirmation
from player import Player

# dodac named tuple na (player, val), bedzie ladniej
PlayerVal = namedtuple('PlayerVal', ['name', 'val'])
OrderedDictPlayers = OrderedDict
OrderedDictPlayers.items_p = lambda self: [PlayerVal(key, val) for key, val in self.items()]
OrderedDictPlayers.iteritems_p = lambda self: (PlayerVal(key, val) for key, val in self.iteritems())


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

class PublicBoard(object):
    def __init__(self, players_with_gold, public_history):
        self.players_with_gold = players_with_gold
        self.public_history = public_history

class GameHistory(OrderedDict):
    pass

class Board(object):
    def __init__(self, players_num, types_of_players, players_names, cards_names, start_gold):
        self.players_num = players_num
        self.types_of_players = types_of_players
        self.players_names = players_names        
        self.cards_names = cards_names
        self.players = OrderedDict()
        for index, (Bot, name, card_name) in enumerate(zip(self.types_of_players, self.players_names, self.cards_names)):
            self.players[name] = Player(index, Bot(), name, cards.cards[card_name], start_gold)
        self.current_player = self.players.items()[0][1]
        self.court = 0
        self.round_num = 0
        self.public_history = GameHistory({})
        self.true_history = GameHistory({})
        self.public_board = PublicBoard(self.method_from_players('gold'), self.public_history)

        for name, player in self.players.iteritems():
            player.bot.public_board = self.public_board
    
    def public_board_update(self):
        self.public_board.players_with_gold = self.method_from_players('gold')

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

        question = '{}, what do you do?'.format(self.current_player.get_repr())
        choices = ['PEEK', 'ANNOUNCE', 'EXCHANGE']
        decision = input_for_choice(self.current_player, question, choices)

        if decision == 'PEEK':
            self.current_player.peek_card()
        elif decision == 'ANNOUNCE':
            self.announcement()
        elif decision == 'EXCHANGE':
            self.current_player.potential_exchange_handler(self.players, self.players_names)
        else:
            raise ValueError('Wrong decision. Get: \'{}\'. Should be one from: {}.'.format(
                decision, choices))

        if not self.true_history.has_key('game_result'):
            self.check_end_condition()
        if self.true_history.has_key('game_result'):
            logging.info('End of game at round number {}'.format(self.round_num))
            logging.info('Player {} won!'.format('Not Implemented'))
            logging.debug('Players Gold: {}'.format(self.method_from_players('gold')))
            return True, self.true_history

        self.next_player()
        return False, self.public_history

    def announcement(self):
        question = 'What do you announce?'
        choices = set(self.cards_names)
        what_declare = input_for_choice(self.current_player, question, choices)

        logging.info('Player: ' + self.current_player.get_repr() + ' has declared ' 
                    + what_declare + '.')

        # for name, index in gen_next_players_list(self.method_from_players('index').items(), self.current_player.index):
        claimants = []
        for name in gen_next_players_list(self.players_names, self.current_player.index):
            question = '{}, do you claim {} yourself?'.format(
                                            self.players[name].get_repr(), what_declare)
            claim = input_for_confirmation(self.current_player, question)
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
            # tutaj powinien sprawdzac koniec gry, a moze nie?
            for name, card_name in claimants_with_cards.iteritems():
                if card_name != what_declare:
                    self.players[name].gold -= 1 
                    self.court += 1
                    logging.info('{} lied. He really is a {}, not a {}.'.format(self.players[name].get_repr(), self.players[name].card.name, what_declare))
        else:
            self.current_player.play_card(self, cards.cards[what_declare])

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

    def check_end_condition(self, cheat_player = None):
        if cheat_player != None:
            if cheat_player.gold >= 10:
                result = OrderedDict([
                ('type_of_end', 'rich_win'),
                ('name', cheat_player.name),
                ('gold', cheat_player.gold),
                ('info', 'cheat_win')
                ])
                self.true_history.update([('game_result', result)])
            return

        richest = self.max_rich_player()
        poorest = self.min_rich_player()
        if richest[0].val >= 13:
            result = OrderedDict([
                ('type_of_end', 'rich_win'),
                ('name', richest[0].name),
                ('gold', richest[0].val),
                ('info', None)
            ])
            self.true_history.update([('game_result', result)])
            return

        if poorest[0].val <= 0:
            result = OrderedDict([
                ('type_of_end', 'poor_win'),
                ('name', richest[0].name),
                ('gold', richest[0].val),
                ('info', None)
            ])
            self.true_history.update([('game_result', result)])
            return

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
