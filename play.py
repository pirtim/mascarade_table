# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import operator

import cards
from player import Player
from board import Board
from bots import SimpleBot

example_players_names_M = ['Chris', 'Tom', 'Marcus', 'Bob', 'Adam', 'Iris']
example_players_names_F = ['Iris', 'Eve', 'Julie', 'Lisa', 'Mary', 'Tara']
example_players_names = example_players_names_M + example_players_names_F

def rewrite_player_type(player_type):
    if type(player_type) == str:
        if player_type.upper() == 'H' or player_type.upper() == 'HUMAN':
            return 'human'
        else:
            print player_type, type(player_type)
            raise ValueError('Not recognized player type. Get: "{}", should be: "human" or type of bot.'.format(player_type))
    elif not issubclass(player_type, SimpleBot):
        raise ValueError('Not recognized bot type. Get: {}, should be subclass of: SimpleBot.'.format(player_type.__name__))

def play(players_num, types_of_players, players_names=None, cards_names=None, start_gold=6):
    if players_names == None:
        players_names = example_players_names[:players_num]
    if cards_names == None:
        cards_names = ['King'] * players_num
    types_of_players = map(rewrite_player_type, types_of_players)

    if players_num < 3:
        raise ValueError('Not enough players (min: 3).')
    if players_num > len(players_names):
        raise ValueError('Not enough names of players (min: {}).'.format(players_num))
    if players_num > len(cards_names):
        raise ValueError('Not enough types of cards (min: {}).'.format(players_num))
    if players_num != len(types_of_players):
        raise ValueError('Not enough types of players (should be: {}).'.format(players_num))
        
    mygame = Board(players_num, types_of_players, players_names, cards_names, start_gold)
    end_of_game = False
    while not end_of_game:
        end_of_game = mygame.next_step()

if __name__ == '__main__':    
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='logging.log',
                        filemode='w', level=logging.DEBUG)
    logging.info('Started')

    cards_names = ['King', 'Queen', 'Judge', 'Bishop']
    play(players_num=4, types_of_players=['human', 'human', 'human', 'human'], cards_names=cards_names)
    
    logging.info('Finished')
