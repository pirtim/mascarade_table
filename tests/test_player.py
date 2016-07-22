import unittest
import datetime
import uuid
import logging
from collections import namedtuple

from .helper_test import *
from ..player import Player
from ..cards import *

class Test_Player(unittest.TestCase):
    def setUp(self):
        self.p = Player(0, 'Tom', King())
        # help_set_up()

    def test___init__(self):
        
        self.assertEqual(self.p.index, 0)
        self.assertEqual(self.p.name, 'Tom')
        self.assertEqual(self.p.card.name, 'King')

    def test_get_repr(self):
        self.assertEqual(self.p.get_repr(), '0:Tom(8)')

    def tearDown(self):
        pass
        # help_tear_down()

if __name__ == '__main__':
    unittest.main()
