# -*- coding: utf-8 -*-
from __future__ import division

class Card(object):
    logic = lambda x: None
    def get_logic(self):
        return lambda x: None

class King(Card):
    name = "King"

    @staticmethod
    def act_on_board(player, board):
        player.gold += 3
    logic = act_on_board

class Queen(Card):
    name = "Queen"

    @staticmethod
    def act_on_board(player, board):
        player.gold += 2
    logic = act_on_board

class Bishop(Card):
    name = "Bishop"

    @staticmethod
    def act_on_board(player, board):
        name_richest = board.max_rich_player()[0].name
        board.players[name_richest].gold -= 2
        player.gold += 2
    logic = act_on_board

class Judge(Card):
    name = "Judge"

    @staticmethod
    def act_on_board(player, board):
        player.gold += board.court
        board.court = 0
    logic = act_on_board

class Thief(Card):
    name = "Thief"
    @staticmethod
    def act_on_board(player, board):
        board.before_player.gold -= 1
        board.next_player.gold -= 1
        player.gold += 2
    logic = act_on_board

class Cheat(Card):
    name = "Cheat"
    @staticmethod
    def act_on_board(player, board):
        board.check_end_condition(cheat = True, cheat_player = player)
    logic = act_on_board

class Witch(Card):
    name = "Witch"
    @staticmethod
    def act_on_board(player, board, second_player):
        player.gold, second_player.gold = second_player.gold, player.gold
    logic = act_on_board

class Spy(Card):
    name = "Spy"
    @staticmethod
    def act_on_board(player, board, second_player, execute):
        board.potential_exchange(second_player, execute)
    logic = act_on_board

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
