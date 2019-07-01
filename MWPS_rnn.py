#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:34:49 2019

@author: shameembinkareem
"""
import warnings
warnings.filterwarnings("ignore",category=Warning)
import pandas as pd
from numpy import argmax
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from Extract_Numbers import Find_Numbers
from QuestionFeature import check_question_or_not
import re
#from ExtractNumbers import extractNumberVectorFromQuestion






df_Train = pd.read_csv('train_data/MWPS_traindata_mod3.csv', engine='python',sep='\t')


questions = df_Train['Questions']
Eqn_Template = df_Train['Equations_Template']



def create_tokenizer(lines):
    tokenizer = Tokenizer(filters='!"#$%&,:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=" ")
    tokenizer.fit_on_texts(lines)
    return tokenizer


def max_length(lines):
    return max(len(line.split()) for line in lines)



Qstn_tokenizer = create_tokenizer(questions)
Qstn_max_length = max_length(questions)
#print('max_length_of_question',Qstn_max_length)
Eqn_tokenizer = create_tokenizer(Eqn_Template)



def encode_sequences(tokenizer, length, lines):
    X = tokenizer.texts_to_sequences(lines)
    X = pad_sequences(X, maxlen=length, padding='post')
    return X

def word_for_id(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def predict_sequence(model, tokenizer, source):
    prediction = model.predict(source)[0]
    integers = [argmax(vector) for vector in prediction]
    target = list()
    for i in integers:
        word = word_for_id(i, tokenizer)
        if word is None:
            break
        target.append(word)
    return ' '.join(target)

def evaluate_model(model, tokenizer, sources):
    for i, source in enumerate(sources):
        source = source.reshape((1, source.shape[0]))
        translation = predict_sequence(model, tokenizer, source)
        return translation


      
def RNN_model_output(preprocessed_input_string):           
    sent_tags_found,Question_flag = check_question_or_not(preprocessed_input_string)
    Number_features,_ = Find_Numbers(preprocessed_input_string)
    #print(Number_features,Question_flag)

    if len(Number_features) == 1 and Question_flag == True :
        model = load_model('saved_rnn_models/MWPS_rnn_model7.h5')
        test_sent = pd.Series(preprocessed_input_string)
        testX = encode_sequences(Qstn_tokenizer, Qstn_max_length, test_sent)
        Predicted_template = evaluate_model(model, Eqn_tokenizer, testX)
        RNN_Math_Expression = Predicted_template.split()
        print(RNN_Math_Expression)
        if RNN_Math_Expression[1] =='-' and float(Number_features[0])< float(1):
            
            num_dis = {}
            num_dis['num1'] = float(1)
            num_dis['num2'] = float(Number_features[0])
#            print(RNN_Math_Expression)
        if RNN_Math_Expression[1]=='+' and 'whQuestion' in sent_tags_found:
             num_dis = {}
             num_dis['num1'] = float(0)
             num_dis['num2'] = float(Number_features[0])
        if RNN_Math_Expression[1]=='*':
            regx_square = re.compile(r'square')
            regx_cube = re.compile(r'cube')
            if regx_square.search(preprocessed_input_string):
                num_dis = {}
                num_dis['num1'] = float(Number_features[0])
                num_dis['num2'] = float(2)
            elif regx_cube.search(preprocessed_input_string):
                num_dis = {}
                num_dis['num1'] = float(Number_features[0])
                num_dis['num2'] = float(3)
            else:
                num_dis['num1'] = float(Number_features[0])
                
           
        fit_Math_Exp = []
        for item in RNN_Math_Expression:
            if item in num_dis.keys():
                fit_Math_Exp.append(num_dis.get(item))
            else:
                fit_Math_Exp.append(item)       
        Math_Expression = ' '.join(map(str,fit_Math_Exp))
        ans = eval(Math_Expression)
        return(Math_Expression,ans)

            
    elif len(Number_features)>=2 and Question_flag == True:
        model = load_model('saved_rnn_models/MWPS_rnn_model7.h5')
        test_sent = pd.Series(preprocessed_input_string)
        testX = encode_sequences(Qstn_tokenizer, Qstn_max_length, test_sent)
        Predicted_template = evaluate_model(model, Eqn_tokenizer, testX)
        print("Generated math expression template: ",Predicted_template)
        Operators_list = ['+','-','*','/']
        Operands_list = ['num1','num2','num3']
        operators = []
        operands = []
        RNN_Math_Expression = Predicted_template.split()
#        print(RNN_Math_Expression)
        for item in RNN_Math_Expression:
            if item in Operators_list:
                operators.append(item)
            if item in Operands_list:
                operands.append(item)
        num_dis = {}
        op_dis = {}
#        print(len(operands))
        if len(Number_features) < len(operands):
            num_dis[operands[0]] = float(1)
            for i in range(len(operands)-1):
                num_dis[operands[i+1]] = float(Number_features[i])
            for i in  range(len(operators)):
                op_dis['op'+str(i)] = operators[i] 
            print(num_dis,op_dis)
            fit_Math_Exp = []
            if op_dis['op'+str(i)] == '+' or op_dis['op'+str(i)] == '*' or op_dis['op'+str(i)] == '-' or op_dis['op'+str(i)] == '/': 
                for item in RNN_Math_Expression:
                    if item in num_dis.keys():
                        fit_Math_Exp.append(num_dis.get(item))
                    else:
                        fit_Math_Exp.append(item)
                         
            Math_Expression = ' '.join(map(str,fit_Math_Exp))
            ans = eval(Math_Expression)
            return(Math_Expression,ans)
        
        if len(Number_features) >= len(operands) :
            for i in range(len(operands)):
                num_dis[operands[i]] = float(Number_features[i])
            for i in  range(len(operators)):
                op_dis['op'+str(i)] = operators[i]
            fit_Math_Exp = []
            print(num_dis,op_dis) 
            for i in range(len(op_dis)):              
                if op_dis['op'+str(i)] == '+' or op_dis['op'+str(i)] == '*' or op_dis['op'+str(i)] == '-' : 
                    for item in RNN_Math_Expression:
                        if item in num_dis.keys():
                            fit_Math_Exp.append(num_dis.get(item))
                        else:
                            fit_Math_Exp.append(item)  
                    break          
                if op_dis['op'+str(i)] == '/':
                    regx_rev_div = re.compile(r'in\s*\d+')
                    if regx_rev_div.search(preprocessed_input_string) and len(num_dis)==2:
                        fit_Math_Exp.append(num_dis['num2'])
                        fit_Math_Exp.append('/')
                        fit_Math_Exp.append(num_dis['num1'])
                        #print(fit_Math_Exp)
                    else:
                        for item in RNN_Math_Expression:
                            if item in num_dis.keys():
                                fit_Math_Exp.append(num_dis.get(item))
                            else:
                                fit_Math_Exp.append(item) 
                        
            Math_Expression = ' '.join(map(str,fit_Math_Exp))
            ans = eval(Math_Expression)
            return(Math_Expression,ans)
            
    
    else:
        pass

#print(RNN_model_output('john had 123 apples. how many apples he left if he ate 23 apples'))
