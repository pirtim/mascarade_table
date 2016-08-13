# -*- coding: utf-8 -*-
from __future__ import division
from inputs import input_for_confirmation, input_for_choice

def King(player, board):
    player.gold += 3

def Queen(player, board):
    player.gold += 2

def Bishop(player, board):
    name_richest = board.max_rich_player()[0].name
    board.players[name_richest].gold -= 2
    player.gold += 2
    # a co jesli on jest najbogatszy? eh

def Judge(player, board):
    player.gold += board.court
    board.court = 0

def Thief(player, board):
    board.before_player.gold -= 1
    board.next_player.gold -= 1
    player.gold += 2

def Cheat(player, board):
    board.check_end_condition(cheat = True, cheat_player = player)

def Witch(player, board):
    second_player = input_for_choice(player, 'Which player?', board.players_names)
    player.gold, second_player.gold = second_player.gold, player.gold

def Spy(player, board):
    # przepisac z potential_exchange_handler
    second_player = input_for_choice(player, 'Which player?', board.players_names)
    execute = input_for_confirmation(player, question='Execute?')
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

for name, card in cards.iteritems():
    card.name = name
