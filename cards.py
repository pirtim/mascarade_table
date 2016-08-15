# -*- coding: utf-8 -*-
from __future__ import division
from inputs import input_for_confirmation, input_for_choice

def King(player, board):
    'The King receives three gold coins from the bank.'
    player.gold += 3

def Queen(player, board):
    'The Queen receives two gold coins from the bank.'
    player.gold += 2

def Bishop(player, board):
    'The Bishop takes two gold coins from the richest of the other players. In case of a tie, the Bishop chooses from which player the two coins are taken.'
    ps_gold = filter(lambda (name, gold): name != player.name, board.max_rich_player(True))
    richest_vec = filter(lambda x: x.val == ps_gold[0].val, ps_gold)

    if len(richest_vec) == 1:
        name_richest = richest_vec[0].name        
    elif len(richest_vec) > 1:
        richest_vec = map(lambda (name, gold): name, richest_vec)
        name_richest = input_for_choice(player, 'Which player?', richest_vec)
    else:
        raise ValueError('Not enough players.')

    board.players[name_richest].gold -= 2
    player.gold += 2

def Judge(player, board):
    '''The Judge takes all the coins (fines) currently on the courthouse board.
    Clarification: If players have falsely claimed to be the Judge and must pay a fine, that fine is paid after the Judge’s power is resolved, and therefore those fines will not be claimed by the Judge during this turn.
    The Judge is the only mandatory character in each game.
    '''
    player.gold += board.court
    board.court = 0

def Thief(player, board):
    board.before_player.gold -= 1
    board.next_player.gold -= 1
    player.gold += 2

def Cheat(player, board):
    'If they have 10 gold coins or more, the Cheat wins the game.'
    board.check_end_condition(cheat_player = player)

def Witch(player, board):
    'The Witch can swap all of her fortune with that of another player of their choice.'
    second_player = input_for_choice(player, 'Which player?', board.players_names)
    second_player = board.players[second_player]
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
