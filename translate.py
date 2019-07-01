#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 22:21:34 2019

@author: user
"""
from googletrans import Translator
def translate_lang(input_text):
    translator = Translator()
    language_found = translator.detect(input_text)
    translated_text = translator.translate(input_text)
    return (language_found.lang,translated_text.text )

#tr,tr1=translate_lang('യോഹന്നാൻ 100 ആപ്പിൾ ഉണ്ടായിരുന്നു. അവൻ 5 കുട്ടികൾക്ക് വിതരണം ചെയ്തു. ഓരോ കുട്ടിക്ക് എത്ര ആപ്പിൾ കിട്ടും?')
#print(tr,tr1)