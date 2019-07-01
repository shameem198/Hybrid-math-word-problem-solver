#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 10:29:35 2019

@author: shameembinkareem
"""
import warnings
warnings.filterwarnings("ignore",category=Warning)
from nltk.parse.stanford import StanfordDependencyParser
import nltk
from word2number import w2n
from find_similar import find_similar

ps = nltk.PorterStemmer()


from gensim.models import KeyedVectors
wvec = KeyedVectors.load_word2vec_format("Word2Vec/GoogleNews-vectors-negative300-SLIM.bin", binary=True)
fl = open("verb.txt")
seedverbs = []

seedtype  = {}
for line in fl:
    seedtype[line.split()[0]] = line.split()[1]
    line = line.strip().split(" ")[0]
    seedverbs.append(line.split()[0])

class linguistic_operations():
    def __init__(self):
        self.depRelations = []
        self.lastrelation = []
        self.question = ""
        self.ind = {}
        self.visited = []
        self.path_to_jar = "/home/user/stanford-parser/stanford-parser-3.4.1.jar"
        self.path_to_models_jar = "/home/user/stanford-parser/stanford-parser-3.4.1-models.jar"
        self.dependency_parser = StanfordDependencyParser(path_to_jar = self.path_to_jar, path_to_models_jar = self.path_to_models_jar)
        return
    
    def dependencyParse(self,sentence):
        self.question = sentence
        result = self.dependency_parser.raw_parse(sentence)
        dep = result.__next__()
        self.depRelations = list(dep.triples())
        print('Stanford Parsing: \n',self.depRelations)
        return self.depRelations
    
    
    def numNoun(self):
        allrelations = {}
        for relation in self.depRelations:
            if relation[1] == 'nummod':
                seed = ps.stem(relation[0][0])
                if seed not in allrelations:
                    allrelations[seed] = []
                allrelations[seed].append(w2n.word_to_num(str(relation[2][0])))
        self.allrelations =  allrelations
        return allrelations
    
        
    def LastRelation(self):
        
        last = nltk.sent_tokenize(self.question)[-1]
        allwords = self.makeseedvocab(last)
        result = self.dependency_parser.raw_parse(last)
        dep = result.__next__()
        self.lastrelation = list(dep.triples())
        return 
               
    
    def makeseedvocab(self,last):
        allwords = set()
        sentences = nltk.word_tokenize(last)
        for word in sentences:
            allwords.add(ps.stem(word))
        return allwords
    
    
    def whoseQuantity(self):
        for relation in self.lastrelation:
            if (relation[0][1] == "NNS" or relation[0][1] == "NN") and ps.stem(relation[0][0]) in self.allrelations:
                print('Whose_quantity:',ps.stem(relation[0][0]))
                return ps.stem(relation[0][0])
            elif (relation[2][1]== "NNS" or relation[2][1]== "NN") and ps.stem(relation[2][0]) in self.allrelations:
                print('Whose_quantity:',ps.stem(relation[2][0]))
                return ps.stem(relation[2][0])
            

def findtransition(linguistic,x):
        temp = nltk.sent_tokenize(linguistic.question)
        sentences = temp[0:-1]
        premsentence = ""
        for i in sentences:
            premsentence += i
        result = linguistic.dependency_parser.raw_parse(premsentence)
        dep = result.__next__()
        deppremise = list(dep.triples())
        for relation in deppremise:
            if relation[0][1][0:2] ==u"VB":
                ms = x.most_similar(relation[0][0],seedverbs,wvec)
                print("1st_entity_VB:",relation[0][0]," Similar_verb:",ms)
                if seedtype[ms] == '+' or seedtype[ms] =='-' or seedtype[ms] =='/' or seedtype[ms] =='*':
                    return seedtype[ms]
            if relation[2][1][0:2] ==u"VB":
                ms = x.most_similar(relation[2][0],seedverbs,wvec)
                print("2nd_entity_VB:",relation[2][0]," Similar_verb:",ms)
                if seedtype[ms] == '+' or seedtype[ms] =='-' or seedtype[ms] =='/' or seedtype[ms] =='*':
                    return seedtype[ms]
        return "0"
    
def findanswer(allrelations,trans,qentity):
    quantities = allrelations[qentity]
    ans =0.0
    if len(quantities)==1 and len(allrelations)==2:
        if trans == '/':
            SecondQentity = [*allrelations][1]
            SecondQuantity = allrelations[SecondQentity]
            if SecondQentity != quantities[0]:
                ans = abs(int(quantities[0])/int(SecondQuantity[0]))
                equation = quantities[0],'/',SecondQuantity[0]
                equation = ' '.join(map(str,equation))
    if len(quantities)==2:
        if trans == '+' :
            for i in quantities:
                ans+=int(i)
                equation = quantities[0],'+',quantities[1]
                equation = ' '.join(map(str,equation))
        if trans == '-':
            if quantities[0]>quantities[1]:
                ans = abs(int(quantities[0])-int(quantities[1]))
                equation = quantities[0],'-',quantities[1]
                equation = ' '.join(map(str,equation))
            else:
                ans = abs(int(quantities[1])-int(quantities[0]))
                equation = quantities[1],'-',quantities[0]
                equation = ' '.join(map(str,equation)) 
    if len(quantities)==3:
        if trans == '+' :
            for i in quantities:
                ans+=int(i)
                equation = quantities[0],'+',quantities[1],'+',quantities[2]
                equation = ' '.join(map(str,equation))
    print('Mathematical expression: ',equation)
    print('Answer: ',ans)
    return(equation,ans)

def Rule_model_output(inp_sent):
    linguistic = linguistic_operations()
    linguistic.dependencyParse(inp_sent)
    allrelation = linguistic.numNoun()
    print('Extracted quantites: ',allrelation)
    linguistic.LastRelation()
    qentity = linguistic.whoseQuantity()
    x = find_similar()
    trans = findtransition(linguistic,x)
    print("Operator: ",trans)
    return findanswer(allrelation,trans,qentity)

#print(Rule_model_output('john had 10 apples and he shared among 10 students. how many apple each will get?'))
