#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 17:46:42 2019

@author: user
"""

import speech_recognition as sr

def record_to_text():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    
    try:
        whatyousaid = r.recognize_google(audio)
        print("You said: " + r.recognize_google(audio))
        return whatyousaid
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
   

