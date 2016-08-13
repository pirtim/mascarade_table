# -*- coding: utf-8 -*-
from __future__ import division

import logging

from play import play

if __name__ == '__main__':    
    logging.basicConfig(format='%(levelname)s:%(message)s', filename='logging.log',
                        filemode='w', level=logging.DEBUG)
    logging.info('Started')
    N = 3
    my_minds = ['human'] * N
    cards_names = ['King', 'Queen', 'Bishop']
    play(players_num=3,  types_of_players=my_minds, cards_names=cards_names)
    
    logging.info('Finished')
