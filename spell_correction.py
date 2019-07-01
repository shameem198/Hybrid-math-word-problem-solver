#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 23:35:30 2019

@author: user
"""

from spellchecker import SpellChecker
def spell_correction(text):
    txt1 = text.split()
    spell = SpellChecker()
    misspelled = spell.unknown(txt1)
    for word in misspelled:
        text=text.replace(word,spell.correction(word))
    return text


'''
import enchant
from enchant.checker import SpellChecker
def spell_correction(text):
    chkr = SpellChecker("en_UK","en_US")
    chkr.set_text(text)
    for err in chkr:
        sug = err.suggest()[0]
        err.replace("%s" % (sug))  
        Spellchecked = chkr.get_text()
    try:
        return Spellchecked
    except:
        text
'''
#print(spell_correction('what is the area . of square size 10'))
