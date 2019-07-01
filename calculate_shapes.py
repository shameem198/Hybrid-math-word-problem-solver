import math
import re
regx_digit = re.compile(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?')
regx_square = re.compile(r'(S|s)quare')
regx_area = re.compile(r'(A|a)rea')
regx_rectangle = re.compile(r'(R|r)ectangle')
regx_triangle = re.compile(r'(T|t)riangle')
regx_circle = re.compile(r'(C|c)ircle')

def calc_square(a_side):
    square_area = a_side ** 2
    square_area_eq = str(a_side)+' * '+str(a_side)
    return square_area_eq,square_area

def calc_rectangle(w_side, l_side):
    rect_area = l_side * w_side
    rect_area_eq = str(l_side)+' * '+str(w_side)
    return rect_area_eq,rect_area

def calc_triangle(base, height):
    triangle_area = (base * height) / 2
    triangle_area_eq = '( '+str(base)+' * '+str(height)+' )'+' / '+str(2)
    return triangle_area_eq,triangle_area

def calc_circle(radius):
    circle_area = math.pi * radius ** 2
    circle_area_eq = str(math.pi)+' * '+'('+str(radius)+')**'+str(2)
    return circle_area_eq,circle_area


def calc_logic(input_str):
#area of square
    if regx_digit.search(input_str) and regx_area.search(input_str) and regx_square.search(input_str):
        if len(regx_digit.findall(input_str))==1:
            a_side = float(regx_digit.findall(input_str)[0])
            square_area_eq,square_area = calc_square(a_side)
            return square_area_eq,square_area
#area of rectangle
    elif regx_digit.search(input_str) and regx_area.search(input_str) and regx_rectangle.search(input_str):
        if len(regx_digit.findall(input_str))==2:
            w_side,l_side = float(regx_digit.findall(input_str)[0]),float(regx_digit.findall(input_str)[1])
            rect_area_eq,rect_area = calc_rectangle(w_side, l_side)
            return rect_area_eq,rect_area
#area of traingle
    elif regx_digit.search(input_str) and regx_area.search(input_str) and regx_triangle.search(input_str):
        if len(regx_digit.findall(input_str))==2:
            base, height = float(regx_digit.findall(input_str)[0]),float(regx_digit.findall(input_str)[1])
            triangle_area_eq,triangle_area = calc_triangle(base, height)
            return triangle_area_eq,triangle_area
#area of circle
    elif regx_digit.search(input_str) and regx_area.search(input_str) and regx_circle.search(input_str):
        if len(regx_digit.findall(input_str))==1:
            radius = float(regx_digit.findall(input_str)[0])
            circle_area_eq,circle_area = calc_circle(radius)
            return circle_area_eq,circle_area
    else:
        pass

#print(calc_logic('area of a square with size 100'))
