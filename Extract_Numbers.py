#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:53:26 2019

@author: ShameemBinKareem
"""
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 
from word2number import w2n
import re


def Find_Numbers(txt):
    numberVector = []
    word_replaced_input = txt.lower() 
    numberVector = re.findall(r"[-+]?\d*\.\d+|\d+", word_replaced_input)
    wordsList = nltk.word_tokenize(word_replaced_input)
    tagged = nltk.pos_tag(wordsList) 
    try:             
        for i in range(len(tagged)):
#            print(tagged[i][0],tagged[i][1])
            if tagged[i][0] not in numberVector:
                    word = tagged[i][0]
                    try:
                        number = w2n.word_to_num(tagged[i][0])
                        numberVector.append(number)
                        word_replaced_input = word_replaced_input.replace(word,str(number))
                    except:
                        number = word        
        return(numberVector,word_replaced_input)   
    except:
        return(numberVector,txt)
        
    



#print(Find_Numbers('How many one are in twenty??')) 