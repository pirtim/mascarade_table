# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import cards

example_players_names_M = ['Chris', 'Tom', 'Marcus', 'Bob', 'Adam', 'Iris']
example_players_names_F = ['Iris', 'Eve', 'Julie', 'Lisa', 'Mary', 'Tara']
example_players_names = example_players_names_M + example_players_names_F

class Board(object):
    def __init__(self, players_num = 2, players_names = None, cards_names = None):
        self.players_num = players_num
        if players_names == None:
            self.players_names = example_players_names[:players_num]  

        self.players = OrderedDict()
        for name in self.players_names:
            self.players[name] = Player(cards.King())
        self.current_player = self.players[self.players_names[0]]
        self.court = 0

    def next_step(self):
        decision = raw_input('PEEK, DECL, EXCH?').upper()
        if decision == 'PEEK' or decision == 'P':
            self.current_player.peek_card()

        elif decision == 'DECL' or decision == 'D':
            self.current_player.card.get_logic()(self) 

        elif decision == 'EXCH' or decision == 'E':
            second_player = raw_input('Which player?')
            if second_player not in self.players_names:
                raise ValueError

            execute = raw_input('Execute [Y/N]?').upper()
            if execute != 'Y' or execute != 'N':
                raise ValueError 
                
            self.current_player.potential_exchange(second_player, execute == 'Y')

        else:
            raise ValueError

        self.check_win_condition()
    
    def check_win_condition(self):
        return NotImplemented

    def max_rich_player(self):
        return NotImplemented

class Player(object):
    def __init__(self, card):
        self.card = card
        self.gold = 8

    def peek_card(self):
        pass

    def play_card(self):
        pass

    def potential_exchange(self, second_player, execute):
        if execute:
            self.card, second_player.card = second_player.card, self.card


if __name__ == '__main__':
    mygame = Board(3)
    print mygame.players
    mygame.play()
    print mygame.players['Chris'].gold