#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 10:17:09 2019

@author: user
"""
import random
import re
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 
from nltk.corpus import wordnet 
nounwords = [ 'Pencils', 'Sharks','Aprons', 'Oranges','Desks','Sheep','Ties','Tables','Turkey','Bows','Pomegranates','Chairs','Donkeys','Vest','Cheeks','Gauva','Stairs','Dogs','Pants','Grapes' ,'Books','Cats','Trousers','Brinjal','Pigeon','Bermudas','Lips','Laptops','Sparrows','Crests' ,'Desktops','Tigers','Hairs','Mobiles','Elephants','Belts','Crow','Buckles','Lion', 'Gown' ,'Shoulders','Onion','Bear','Jersey','Hands','Grains','Fans','Ostrich','Boxers','Fingers','Pipe','Parrot', 'Sweaters' ,'Spoons','Fox','Jackets','Rice','Pads','Wolf' ,'Suitcases','Mangos','Monkey','Legs' ,'Panther', 'Sandals' ,'Foot' ,'Potato','Peacock','Shoes','Balloons','Pandas','Leggings','Deers','Bikini','Lungs','Beans','Arrows','Swan','Sari','Bones','Bread','Stove','Cows','Frock','Brain','Butter','Lighter','Goat','Toes','Cheese','Buffalos','Shirts','Palm','Noodles','Keyboard','Suits','Ribs','Pastas','Mouse','Hat','Eggs','Bulbs','Frogs', 'Caps','Televisions']
person_name = [ 'James','David','Christopher','George','Ronald','Johny','Richard','Daniel','Kenneth','Anthony','Robert','Charles','Paul','Steven','Kevin','Michael','Joseph','Mark','Edward','Jason','William','Thomas','Donald','Bria','Jeff']
regx_not_NNS = re.compile(r'kwh|months|miles|befor|acres|hours|kilometeters|meters|days|times|days|km|years|minutes|kilograms|kg|rows|pieces|points|kinds|blocks|tons|dollars|equals|sets|liters|runs|needs|competitions|pairings|games|multipliers|walks|beats|flies|stores|results|numbers|pages|words|units|calls|hectares|nails|savings|parts|methods|pairs|ways|children|people|friends|students|degree|grades')
regex_not_NNP = re.compile(r'\b(?:(J|j)an(?:uary)?|(F|f)eb(?:ruary)?|(M|m)ar(?:ch)?|(A|a)pr(?:il)?|(M|m)ay|(J|j)un(?:e)?|(J|j)ul(?:y)?|(A|a)ug(?:ust)?|(S|s)ep(?:tember)?|(O|o)ct(?:ober)?|((N|n)ov|(D|d)ec)(?:ember)?)\b|\b(((M|m)on|(T|t)ues|(W|w)ed(nes)?|(T|t)hur(s)?|(F|f)ri|(S|s)at(ur)?|(S|s)un)(day)?)\b|kilogram|How|kg|km|Substract|/|Area|Sum|Mount|Everest|Mount|Anchorage|Alaska|F.|Los|Angeles|California|Management|DVDs')
regex_not_CD = re.compile(r'zero|(O|o)ne|(T|t)wo|(T|t)hree|billion|thousand|million')
import pandas as pd
data_frame = pd.read_csv('train_data/ADD.csv', engine='python')
Questions = data_frame['Questions']
final_questions=[]
for Qn in Questions:
    wordsList = nltk.word_tokenize(Qn)
    tagged = nltk.pos_tag(wordsList) 
#    print(Qn)
#    print(tagged)
    for i in range(len(tagged)):
        if tagged[i][1] == 'NNS' and not regx_not_NNS.search(tagged[i][0]):
            Qn = Qn.replace(tagged[i][0],nounwords[random.randint(1,104)].lower()) 
#            print(tagged[i][0])
            break
#    print(Qn)
    for i in range(len(tagged)):
        if tagged[i][1] == 'NNP' and not regex_not_NNP.search(tagged[i][0]):
            Qn = Qn.replace(tagged[i][0],person_name[random.randint(1,24)].lower())
#            print(tagged[i][0])
            break
#    print(Qn)
    for i in range(len(tagged)):
        if tagged[i][1] == 'CD' and not regex_not_CD.search(tagged[i][0]): 
#            print(tagged[i][0])
            Qn = Qn.replace(tagged[i][0],str(random.randint(1,1000))) 
    final_questions.append(Qn)
        
#print(final_questions)  
Questions = pd.DataFrame({'Questions':final_questions})
Questions.to_csv('10.csv')


