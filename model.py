#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 12:24:23 2019

@author: shameem bin kareem
"""
import warnings
warnings.filterwarnings("ignore", category=Warning)
import subprocess
import tkinter
from tkinter import *
from tkinter import filedialog


def Folder():
    global Dirname
    global file_name
    Dirname = filedialog.askopenfilename(filetypes=[("Text files","*.*")])
    file_name=open(Dirname,'r',encoding='utf-8')
    file_name=file_name.read()

def preprocess_input_string(text):
    from coreference_resolution import resolve_coref
    from Preprocess import text_to_wordlist
    from spell_correction import spell_correction
    from Extract_Numbers import Find_Numbers
    preprocessed_input_string = text_to_wordlist(text)
    co_ref_input_string = resolve_coref(preprocessed_input_string)
    corrected_input_string = spell_correction(co_ref_input_string)
    _,Preprocessed_Word_problem = Find_Numbers(corrected_input_string)
    
    print("\nGiven word problem:\n",text)
    print("\n------------------------------------------------------------------------------\n")
    print("After contraction handling and remove unwanted punctuations and spaces:\n",preprocessed_input_string)
    print("\n------------------------------------------------------------------------------\n")
    print("\nAfter resolving coreference resoltion:\n",co_ref_input_string)
    print("\n------------------------------------------------------------------------------\n")
    print("\nAfter spelling correction:\n",corrected_input_string)
    print("\n------------------------------------------------------------------------------\n")
    print("After replacing word to numbers:\n",Preprocessed_Word_problem)
    print("\n------------------------------------------------------------------------------\n")

    
    return Preprocessed_Word_problem
    

def takeinput_from_keyboard():
    input_string = input_string_Box.get("1.0",'end-1c')
    preprocessed_input_string = preprocess_input_string(input_string)    
    Display_model(input_string,preprocessed_input_string)
    

def takeinput_from_sound():
    from speech_reco import record_to_text
    input_string = record_to_text()
    input_string_Box.delete(1.0, END)
    input_string_Box.insert(END,input_string)
    
def voice_output():
    from voice_out import voice_output
    output_string = ResultBox.get("1.0",'end-1c')
    voice_output(output_string)
    
    

    
def takeinput_from_doc():
    from readFile import readFile
    global file_name
    file_name = filedialog.askopenfilename(filetypes=[("Text files","*.*")])
    print("selected_filename: ",file_name)
    input_string = readFile(file_name)
    input_string_Box.delete(1.0, END)
    input_string_Box.insert(END,input_string)

def write_File():
    from translate import translate_lang
    proc = subprocess.Popen(['gedit', 'sample_docs/lang_file.txt'])
    proc.wait()
    file = open("sample_docs/lang_file.txt", "r",encoding="utf-8")
    content = file.read()
    file.close()
    translated_lang, input_string = translate_lang(content)
    input_string_Box.delete(1.0, END)
    input_string_Box.insert(END,input_string)

def clear_text():
    input_string_Box.delete(1.0, END)
    ResultBox.delete(1.0, END)
        
def Display_model(input_string,preprocessed_input_string):
    
    try:
        print('entering regex model1------->')
        from calculate_shapes import calc_logic
        Calc_eqn,answer = calc_logic(preprocessed_input_string)
        if Calc_eqn!=None:
            ResultBox.delete(1.0, END)
            ResultBox.insert(END,"Mathematical expression returned by regular expression model\n")
            ResultBox.insert(2.0,'Mathematical Expression : ')
            ResultBox.insert(END,Calc_eqn)
            ResultBox.insert(END, '\n')
            ResultBox.insert(3.0,'Answer : ')
            ResultBox.insert(END, answer)
        else:
            print('Trying to solve using verb classification model...\n')
            raise ValueError
        
    except:
        try:
            str_len = len(input_string.split())
            #print('input string length is: ',str_len)
            if str_len >= 10:
                print('Input word problem:\n',input_string)
                print('\n\n entering Rule-based model------->')
                from MWPS_rulebased import Rule_model_output
                equation,ans = Rule_model_output(input_string)
                ResultBox.delete(1.0, END)
                ResultBox.insert(END,"Mathematical expression returned by verb classification model\n")
                ResultBox.insert(2.0,'Mathematical Expression : ')
                ResultBox.insert(END,equation)
                ResultBox.insert(END,'\n')
                ResultBox.insert(3.0,'Answer : ')
                ResultBox.insert(END, ans)
            else:
                print('Trying to solve using encoder-decoder model...\n')
                raise ValueError
        except:
            try:
                str_len = len(preprocessed_input_string.split())
                #print('preprocessed length of a string is: ',str_len)
                if str_len >= 6:
                    print('\n\n entering DNN model------>')
                    from MWPS_rnn import RNN_model_output 
                    Math_Expression,ans = RNN_model_output(preprocessed_input_string)
                    if Math_Expression != None:
                        print('Mathematical expression: ',Math_Expression)
                        print('Answer: ',ans )
                        ResultBox.delete(1.0, END)
                        ResultBox.insert(END,"Mathematical expression returned by encoder-decoder model\n")
                        ResultBox.insert(2.0,'Mathematical Expression is: ')
                        ResultBox.insert(END,Math_Expression)
                        ResultBox.insert(END, '\n')
                        ResultBox.insert(3.0,'Answer : ')
                        ResultBox.insert(END, ans)
                else:
                    raise ValueError
            except:
                try:
                    print('\n\n entering regex model1------->')
                    from solveExpression import Mathematical_expression
                    Math_Expression,ans = Mathematical_expression(input_string)  
                    if Math_Expression != None:    
                        ResultBox.delete(1.0, END)
                        ResultBox.insert(END,"Input question seems like a mathematical expression..!\n")
                        ResultBox.insert(2.0,'Mathematical Expression : ')
                        ResultBox.insert(END,Math_Expression)
                        ResultBox.insert(END, '\n')
                        ResultBox.insert(3.0,'Answer : ')
                        ResultBox.insert(END, ans)
                except:
                    ResultBox.delete(1.0, END)
                    ResultBox.insert(END,"Please Enter  Word Problem Properly")
           

window = tkinter.Tk()
window.title('Math Word Problem Solver')
window.geometry("1400x1000")
window.resizable(width=True, height=True)
image = tkinter.PhotoImage(file="GUI_images/bg.png")
label = tkinter.Label(image=image)
label.pack()

L1 = Label(window, text="Math Word Problem Solver",fg='white',bg='grey20',padx = 5, pady = 5)
labelfont = ('Times', 26, 'bold')
L1.config(font=labelfont)
L1.place(x=310, y=30)

input_string_Box = Text(window,height=10,width=80)
input_string_font = ('Helvetica', 15,'bold')
input_string_Box.config(font=input_string_font)
input_string_Box.place(x=100,y=150)


input_string_Button = Button(window, text='Solve Problem',command = takeinput_from_keyboard, highlightcolor='blue',bg='forest green')
button_font = ('Times', 15, 'bold')
input_string_Button.config(font=button_font)
input_string_Button.place(x=460, y=390)

input_doc_Button = Button(window, text='Upload Document',command = takeinput_from_doc, highlightcolor='blue',bg='Cadetblue')
button_font = ('Times', 15, 'bold')
input_doc_Button.config(font=button_font)
input_doc_Button.place(x=1050, y=250)

input_lang_Button = Button(window, text='Question in other languages',command = write_File, highlightcolor='blue',bg='plum3')
button_font_lang = ('Times', 15, 'bold')
input_lang_Button.config(font=button_font_lang)
input_lang_Button.place(x=1010, y=310)

mic = PhotoImage(file="GUI_images/micro.png")
input_sound_Button = Button(window, text="say something", image=mic, command=takeinput_from_sound,highlightcolor='blue',bg='grey')
input_sound_Button.place(x=1110, y=170)

head_phone = PhotoImage(file="GUI_images/speaker.png")
voice_out_Button = Button(window, text="voice_otput", image=head_phone, command=voice_output,highlightcolor='blue',bg='grey')
voice_out_Button.place(x=1110, y=525)

clear_Button = Button(window, text='Clear All',command = clear_text, highlightcolor='green',bg='red3')
button_font_clear = ('Verdana', 15)
clear_Button.config(font=button_font_clear)
clear_Button.place(x=480, y=625)

ResultBox = Text(window, height=5, width=80)
ResultBox_font = ('Helvetica', 15,'bold')
ResultBox.config(font=input_string_font)
ResultBox.place(x=100, y=500)

window.mainloop()				
