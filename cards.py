# -*- coding: utf-8 -*-
from __future__ import division

class Card(object):
    def get_logic(self):
        return lambda x: None

class King(Card):
    name = "King"
    def get_logic(self):
        def act_on_board(board):
            board.current_player.gold += 3
        return act_on_board

class Queen(Card):
    name = "Queen"
    def get_logic(self):
        def act_on_board(board):
            board.current_player.gold += 2
        return act_on_board

class Bishop(Card):
    name = "Bishop"
    def get_logic(self):
        def act_on_board(board):
            board.max_rich_player()[0].gold -= 2
            board.current_player.gold += 2
        return act_on_board

class Judge(Card):
    name = "Judge"
    def get_logic(self):
        def act_on_board(board):
            board.current_player.gold += board.court
            board.court = 0
        return act_on_board

class Thief(Card):
    name = "Thief"
    def get_logic(self):
        def act_on_board(board):
            board.before_player.gold -= 1
            board.next_player.gold -= 1
            board.current_player.gold += 2
        return act_on_board

class Cheat(Card):
    name = "Cheat"
    def get_logic(self):
        def act_on_board(board):
            board.check_end_condition(cheat = True, cheat_player = board.current_player)
        return act_on_board

class Witch(Card):
    name = "Witch"
    def get_logic(self):
        def act_on_board(board, second_player):
            board.current_player.gold, second_player.gold = second_player.gold, board.current_player.gold
        return act_on_board

class Spy(Card):
    name = "Spy"
    def get_logic(self):
        def act_on_board(board, second_player, execute):
            board.potential_exchange(second_player, execute)
        return act_on_board

cards = {
    'King' : King,
    'Queen' : Queen,
    'Bishop' : Bishop,
    'Judge' : Judge,
    'Thief' : Thief,
    'Cheat' : Cheat,
    'Witch' : Witch,
    'Spy' : Spy,
}
