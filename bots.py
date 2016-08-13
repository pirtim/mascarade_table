# -*- coding: utf-8 -*-
from __future__ import division

import logging

class Human(object):
    def __init__(self):
        self.public_history = None

class SimpleBot(object):
    def __init__(self):
        self.public_history = None

    def get_move(self, type_of_move, question, choices=None):
        raise NotImplementedError
