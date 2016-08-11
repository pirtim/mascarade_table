# -*- coding: utf-8 -*-
from __future__ import division

import logging
from collections import namedtuple, OrderedDict
import operator
import functools

import cards

class Human(object):
    def __init__(self):
        self.public_history = None

class SimpleBot(object):
    def __init__(self):
        self.public_history = None

    def get_move(self, type_of_move, question, choices=None):
        pass
