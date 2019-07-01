#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk
from nltk.tokenize import sent_tokenize
#nltk.download('nps_chat')
posts = nltk.corpus.nps_chat.xml_posts()[:4000]

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

def Questionfeature(line):
    featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]
    train_set= featuresets
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    Tag = classifier.classify(dialogue_act_features(line))
    return Tag
    


def check_question_or_not(preprocessed_input_string):
    Interrogative_Sent_tags = ['whQuestion','Continuer','Clarify','Other','ynQuestion']
    sent_tags_found = []
    for sent in sent_tokenize(preprocessed_input_string):
        Question_feature = Questionfeature(sent)
        sent_tags_found.append(Question_feature)
    #print(sent_tags_found)
    for tag in sent_tags_found:
        if len(sent_tags_found)>=1:
            if tag in Interrogative_Sent_tags:
                Question_flag = True
                break
            else:
              Question_flag = False
    
    return (sent_tags_found,Question_flag)

#print(check_question_or_not('i have 4 aples. i gave 2 aples to sam'))
