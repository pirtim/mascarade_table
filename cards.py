# -*- coding: utf-8 -*-
from __future__ import division

# mozna sobie odpuscic klasy i zrobic to jako zwyczajne funkcje

class Card(object):
    logic = lambda x: None
    def get_logic(self):
        return lambda x: None

class King(Card):
    name = "King"

    @staticmethod
    def logic(player, board):
        player.gold += 3

class Queen(Card):
    name = "Queen"

    @staticmethod
    def logic(player, board):
        player.gold += 2

class Bishop(Card):
    name = "Bishop"

    @staticmethod
    def logic(player, board):
        name_richest = board.max_rich_player()[0].name
        board.players[name_richest].gold -= 2
        player.gold += 2
        # a co jesli on jest najbohatszy? eh

class Judge(Card):
    name = "Judge"

    @staticmethod
    def logic(player, board):
        player.gold += board.court
        board.court = 0

class Thief(Card):
    name = "Thief"
    @staticmethod
    def logic(player, board):
        board.before_player.gold -= 1
        board.next_player.gold -= 1
        player.gold += 2

class Cheat(Card):
    name = "Cheat"
    @staticmethod
    def logic(player, board):
        board.check_end_condition(cheat = True, cheat_player = player)

class Witch(Card):
    name = "Witch"
    @staticmethod
    def logic(player, board, second_player):
        player.gold, second_player.gold = second_player.gold, player.gold

class Spy(Card):
    name = "Spy"
    @staticmethod
    def logic(player, board, second_player, execute):
        board.potential_exchange(second_player, execute)

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
