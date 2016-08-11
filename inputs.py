# -*- coding: utf-8 -*-
from __future__ import division
from bots import Human

from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

def input_for_confirmation(player, question):
    if isinstance(player.bot, Human):
        return prompt_for_confirmation(question)
    else:
        return player.bot.get_move('confirmation', question)

def input_for_choice(player, question, choices):
    if isinstance(player.bot, Human):
        print question
        return prompt_for_choice(choices)
    else:
        return player.bot.get_move('choices', question, choices)
