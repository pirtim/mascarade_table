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

def play(players_num=4, bots=None, players_names=None, cards_names=None, start_gold=6):
    if players_names == None:
        players_names = example_players_names[:players_num]
    if cards_names == None:
        cards_names = ['King'] * players_num
    if bots == None:
        raise ValueError

    if players_num < 4:
        raise ValueError
    if players_num > len(players_names) or players_num > len(cards_names) or players_num > len(bots):
        raise ValueError
        
    mygame = Board(players_num, players_names, cards_names, start_gold, bots)
    end_of_game = False
    while not end_of_game:
        end_of_game = mygame.next_step()

if __name__ == '__main__':    
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='play.log',
                        filemode='w', level=logging.DEBUG)
    logging.info('Started')
    N = 4
    my_bots = ['SimpleBot'] * N
    cards_names = ['King', 'Queen', 'Judge', 'Bishop']
    play(players_num=N, bots=my_bots, cards_names=cards_names)
    
    logging.info('Finished')
