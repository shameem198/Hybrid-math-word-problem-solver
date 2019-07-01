#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 09:54:53 2019

@author: shameemBinKareem
"""

import docx2txt
import PyPDF2 
        
def readFile(fileName):
        extension = fileName.split(".")[-1]
        if extension == "txt":
            f = open(fileName, 'r',encoding='utf-8')
            string = f.read()
            f.close() 
            return string
        elif extension == "docx":
            try:
                return docx2txt.process(fileName)
            except:
                return ''
                pass
        elif extension == "pdf":
            try:
                read_pdf = PyPDF2.PdfFileReader(fileName)
                page = read_pdf.getPage(0)
                page_content = page.extractText()
                return page_content
               
            except:
                return ''
                pass
        else:
            print('Unsupported format')
            return '', ''
