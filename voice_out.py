#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 10:02:27 2019

@author: user
"""
from gtts import gTTS 
import os
def voice_output(output): 
    language = 'en'
    try:
        myobj = gTTS(text=output, lang=language, slow=False) 
    except:
        output = 'Sorry..Please enter word problem'
        myobj = gTTS(text=output, lang=language, slow=False) 
        
    myobj.save("output.mp3") 
    os.system("mpg321 output.mp3") 
    
