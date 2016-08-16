# -*- coding: utf-8 -*-
from __future__ import division
from bots import Human

from humanfriendly.prompts import prompt_for_confirmation, prompt_for_choice

basic_types_of_decisions = ['which_action', 'what_announce', 'swap_who', 'swap_exe', 'claim']
cards_types_of_decisions = [
    'spy_swap_who', 'spy_swap_exe', 'bishop_who',
    'fool_swap_who', 'fool_swap_exe', 'witch_who']

class BotError(Exception):
    pass

def input_for_confirmation(player, info, question):
    if info not in (basic_types_of_decisions + cards_types_of_decisions):
        raise ValueError('type_of_decision not recognized.')
    if isinstance(player.bot, Human):
        return prompt_for_confirmation(question)
    else:
        result = player.bot.get_move('confirmation', info, question)
        if type(result) != bool:
            raise BotError('Bot\'s choice is not bool type.')
        return result

def input_for_choice(player, info, choices, question):
    if isinstance(player.bot, Human):
        print question
        return prompt_for_choice(choices)
    else:
        result = player.bot.get_move('choices', info, choices, question)
        if result not in choices:
            raise BotError('Bot\'s choice is not on the list of permitted choices.')
        return result
