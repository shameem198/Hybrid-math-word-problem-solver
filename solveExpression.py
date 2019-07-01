#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 00:03:54 2019

@author: user
"""
import re
def Mathematical_expression(text):
#    mathematical_expression = re.compile(r'(\(*(\s*\d+\s*[\*/+-]\s*)*(\(*\s*(\d+\s*[\*/+-]\s*)+\)*)*(\d+\s*)\s*\)*)+(\s*[\*/+-]\s*\d+)*(\s*[\*/+-]\s*)*(\(*\s*(\d+\s*[\*/+-]\s*)+(\d+\s*)\s*\)*)*(\s*[\*/+-]\s*\d+)*')
    mathematical_expression = re.compile(r'(\(*(\s*\d+[,.]?\d*\s*\)*\s*[\*/+-]\s*))+(\s*\(*\s*(\d+[,.]?\d*\s*)+\)*\s*)+')
    if mathematical_expression.search(text):
        matched_eqn = mathematical_expression.search(text)
        eqn = matched_eqn.group(0)
        ans = eval(matched_eqn.group(0))
        return(eqn,ans)
    
#print(Mathematical_expression('( 12.34 / 2 ) + 12.12'))