# -*- coding: utf-8 -*-
from __future__ import division

from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

def input_for_confirmation(player, question):
    if player.bot == None:
        return prompt_for_confirmation(question)
    else:
        return player.bot.get_confirmation(question)

def input_for_choice(player, question, choices):
    if player.bot == None:
        print question
        return prompt_for_choice(choices)
    else:
        return player.bot.get_choice(question, choices)
