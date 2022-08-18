# -*- coding: utf-8 -*-
"""
Created on Wed Jul 1 2022
@author: Antoine BOTTENMULLER
"""

import math
import numpy as np


# WRITER class to sticky-draw letters or numbers on ndarray-formatted images
class writer :
    
    
    ### INITIALIZATION OF THE 'WRITER' OBJECT
    
    # DESCRIPTION OF REQUIRED STATIC PARAMETERS
    """
    # drawing_size : a int/float for the length of the drawing area squares (in pixels)
    # proportion : a float/int between 0 and 1 included for the proportion of the drawings on images relative to the drawing size
    # adapt_proportion : a boolean to automatically adapt or not the size of the letters or numerals in the limits of drawing_size value
    # color_values : an object for the chosen color. It can be a float/int (-> NOT colorized, ie Black&White) or a list/ndarray of floats (-> colorized)
    # main_contrast_exponent : a positive float/int for the global contrast exponent of the chosen color regarding the image colors MEANS. ==1 -> Neutral ; <1 -> less contrasted ; >1 -> more contrasted
    # color_contrast_proportion : a float/int between 0 and 1 included for the proportion of the contrast between the three colors (BGR) of the chosen colors. ==0.5 -> Neutral ; <0.5 -> less contrasted ; >0.5 -> more contrasted
    # pixel_color_study_proportion : a float/int between 0 and 1 included for the proportion of the weight of the currently studied pixel colors taken into account. ==0 <-> Pixel not taken into account (faster!!)
    # transparency : a float/int between 0 and 1 included for the transparency of the drawings on the considered 2D or 3D images
    # message : a boolean to allow or not the display of warning messages
    """
    
    # Initialization of the static parameters
    def __init__(self, drawing_size, proportion = 1.0, adapt_proportion = False, color_values = 'inverted_mean_proportion', main_contrast_exponent = 1.0, color_contrast_proportion = 0.5, pixel_color_study_proportion = 0.0, transparency = 1.0, message = False):
        self.set_message_allowed(message)
        self.set_drawing_size(drawing_size)
        self.set_proportion(proportion)
        self.set_adapt_proportion(adapt_proportion)
        self.set_color_values(color_values)
        self.set_main_contrast_exponent(main_contrast_exponent)
        self.set_color_contrast_proportion(color_contrast_proportion)
        self.set_pixel_color_study_proportion(pixel_color_study_proportion)
        self.set_transparency(transparency)
        self.color_already_calculated = False # Dynamic parameter
    
    
    ### GETTERS AND SETTERS OF THE 'WRITER' PARAMETERS
    
    # Getting current writing length
    def get_drawing_size(self):
        return self.drawing_size
    
    # Setting current writing length
    def set_drawing_size(self, drawing_size):
        if(type(drawing_size) is float or type(drawing_size) is int):
            if(drawing_size>=1):
                self.drawing_size = drawing_size
            else:
                self.drawing_size = 1.0
                if(self.message):
                    print("WARNING : Value of 'drawing_size' must be 1 pxl at minimum. This value has been adapted to 1 pxl.")
        else:
            self.drawing_size = 10.0
            if(self.message):
                print("WARNING : Wrong object format for 'drawing_size'! Must be an int or a float. Value of 'drawing_size' has been adapted to 10 pxls.")
    
    # Getting current proportion
    def get_proportion(self):
        return self.proportion
    
    # Setting current proportion
    def set_proportion(self, proportion):
        if(type(proportion) is float or type(proportion) is int):
            if(proportion<=1 and proportion>=0):
                self.proportion = float(proportion)
            else:
                self.proportion = 1.0
                if(self.message):
                    print("WARNING : Value of 'proportion' must be between 0 and 1 included. This value has been adapted to 1.0.")
        else:
            self.proportion = 1.0
            if(self.message):
                print("WARNING : Wrong object format for 'proportion'! Must be a float or an int, between 0 and 1 included. Value of 'proportion' has been adapted to 1.0.")
    
    # Getting current adapt_proportion
    def get_adapt_proportion(self):
        return self.adapt_proportion
    
    # Setting current adapt_proportion
    def set_adapt_proportion(self, adapt_proportion):
        if(type(adapt_proportion) is bool):
            self.adapt_proportion = adapt_proportion
        else:
            self.adapt_proportion = False
            if(self.message):
                print("WARNING : Wrong object format for 'adapt_proportion'! Must be a bool. Position of 'adapt_proportion' has been adapted to False. Writing proportions will be preserved.")
    
    # Getting current color values
    def get_color_values(self):
        return self.color_values
    
    # Setting current color values
    def set_color_values(self, color_values):
        if((type(color_values) is str and color_values=='inverted_mean_proportion') or color_values is None):
            self.color_values = 'inverted_mean_proportion'
        elif(type(color_values) is np.ndarray or type(color_values) is list or type(color_values) is tuple): # 'color_values' is a list/ndarray <=> image is colorized (3 dim)
            if(type(color_values) is list or type(color_values) is tuple):
                color_values = np.array(color_values)
            number_of_dimensions = np.shape(np.shape(color_values))[0]
            if(number_of_dimensions==1):
                if(color_values.dtype == np.float_ or color_values.dtype == np.int_):
                    number_of_floats = np.shape(color_values)[0]
                    if(number_of_floats!=3):
                        if(number_of_floats<=0):
                            self.color_values = np.array([0.5,0.5,0.5])
                        elif(number_of_floats==1):
                            self.color_values = np.array([float(color_values[0]),float(color_values[0]),float(color_values[0])])
                        elif(number_of_floats==2):
                            self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[1])])
                        else: # Too many floats!
                            self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[2])])
                        if(self.message):
                            print("WARNING : Wrong number of floats in 'color_values' list/ndarray! Must be 3 if image is colorized, or a float if not. Found:",number_of_floats,". Array has now been adapted.")
                    else:
                        self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[2])])
                else:
                    self.color_values = 'inverted_mean_proportion'
                    if(self.message):
                        print("WARNING : Wrong object format inside 'color_values' list/ndarray! Must be only floats. Array has been adapted to 'inverted_mean_proportion'.")
            else:
                self.color_values = 'inverted_mean_proportion'
                if(self.message):
                    print("WARNING : Wrong number of dimensions in 'color_values' list/ndarray! Must be only 1 if image is colorized, or a float if not. Found:",number_of_dimensions,". Array has now been adapted to 'inverted_mean_proportion'.")
        elif(type(color_values) is float or type(color_values) is int): # 'color_values' is a float/int <=> image is not colorized (2 dim)
            self.color_values = float(color_values)
        else:
            self.color_values = 'inverted_mean_proportion'
            if(self.message):
                print("WARNING : Wrong object format for 'color_values'! Must be a float/int if image is not colorized (2D), or a list/ndarray of 3 floats if colorized (3D). Value of 'color_values' has been adapted to 'inverted_mean_proportion'.")
    
    # Getting current main_contrast_exponent
    def get_main_contrast_exponent(self):
        return self.main_contrast_exponent
    
    # Setting current main_contrast_exponent
    def set_main_contrast_exponent(self, main_contrast_exponent): # 'main_contrast_exponent' is float >=0
        if(type(main_contrast_exponent) is float or type(main_contrast_exponent) is int):
            if(main_contrast_exponent>=0):
                self.main_contrast_exponent = main_contrast_exponent
            else:
                self.drawmain_contrast_exponenting_size = 0.0
                if(self.message):
                    print("WARNING : Value of 'main_contrast_exponent' must be >=0. This value has been adapted to 0.0.")
        else:
            self.main_contrast_exponent = 1.0
            if(self.message):
                print("WARNING : Wrong object format for 'main_contrast_exponent'! Must be an int or a float. Value of 'main_contrast_exponent' has been adapted to 1.0.")
    
    # Getting current color_contrast_proportion
    def get_color_contrast_proportion(self):
        return self.color_contrast_proportion
    
    # Setting current color_contrast_proportion
    def set_color_contrast_proportion(self, color_contrast_proportion):
        if(type(color_contrast_proportion) is float or type(color_contrast_proportion) is int):
            if(color_contrast_proportion<=1 and color_contrast_proportion>=0):
                self.color_contrast_proportion = float(color_contrast_proportion)
            else:
                self.color_contrast_proportion = 0.5
                if(self.message):
                    print("WARNING : Value of 'color_contrast_proportion' must be between 0 and 1 included. This value has been adapted to 0.5.")
        else:
            self.color_contrast_proportion = 0.5
            if(self.message):
                print("WARNING : Wrong object format for 'color_contrast_proportion'! Must be a float or an int, between 0 and 1 included. Value of 'color_contrast_proportion' has been adapted to 0.5.")
    
    # Getting current pixel_color_study_proportion
    def get_pixel_color_study_proportion(self):
        return self.pixel_color_study_proportion
    
    # Setting current pixel_color_study_proportion
    def set_pixel_color_study_proportion(self, pixel_color_study_proportion):
        if(type(pixel_color_study_proportion) is float or type(pixel_color_study_proportion) is int):
            if(pixel_color_study_proportion<=1 and pixel_color_study_proportion>=0):
                self.pixel_color_study_proportion = float(pixel_color_study_proportion)
            else:
                self.pixel_color_study_proportion = 0.0
                if(self.message):
                    print("WARNING : Value of 'pixel_color_study_proportion' must be between 0 and 1 included. This value has been adapted to 0.0.")
        else:
            self.pixel_color_study_proportion = 0.0
            if(self.message):
                print("WARNING : Wrong object format for 'pixel_color_study_proportion'! Must be a float or an int, between 0 and 1 included. Value of 'pixel_color_study_proportion' has been adapted to 0.0.")
    
    # Getting current transparency
    def get_transparency(self):
        return self.transparency
    
    # Setting current transparency
    def set_transparency(self, transparency):
        if(type(transparency) is float or type(transparency) is int):
            if(transparency<=1 and transparency>=0):
                self.transparency = float(transparency)
            else:
                self.transparency = 1.0
                if(self.message):
                    print("WARNING : Value of 'transparency' must be between 0 and 1 included. This value has been adapted to 1.0.")
        else:
            self.transparency = 1.0
            if(self.message):
                print("WARNING : Wrong object format for 'transparency'! Must be a float or an int, between 0 and 1 included. Value of 'transparency' has been adapted to 1.0.")
    
    # Getting current message
    def get_message_allowed(self):
        return self.message
    
    # Setting current message
    def set_message_allowed(self, message):
        if(type(message) is bool):
            self.message = message
        else:
            self.message = False
            if(message):
                print("WARNING : Wrong object format for 'message'! Must be a bool. Position of 'message' has been adapted to False. No more warnings will be displayed.")
    
    
    ### MAIN SPECIFIC METHODS OF THE 'WRITER' CLASS
    
    # Drawing letter A
    def draw_A(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
        
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # First line
                    for i in range(0,length):
                        self.draw_pixel(image, up+length-i, left+i//2)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length+i-up)//2)
                    # Third line
                    for j in range(left+length//4+1,left+length*3//4):
                        self.draw_pixel(image, up+length//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter B
    def draw_B(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right_up = int(length*1/2)
                    line_right_down = int(length*2/3)
                    if(line_right_up<=0):
                        line_right_up = 1
                    if(line_right_down<=0):
                        line_right_down = 1
                    # First line
                    for j in range(left+1,left+line_right_up):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+line_right_down+1):
                        self.draw_pixel(image, up+length, j)
                    # Third line
                    for j in range(left+1,left+line_right_down):
                        self.draw_pixel(image, up+length//2, j)
                    # Fourth line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left)
                    # Two demi-circles
                    j_save = left
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left
                        self.draw_pixel(image, up+i, line_right_up+j)
                        self.draw_pixel(image, up+i+length//2, line_right_down+j)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up, u+line_right_up)
                                self.draw_pixel(image, i+1+up+length//2, u+line_right_down)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+up, u+line_right_up)
                                self.draw_pixel(image, i+1+up+length//2, u+line_right_down)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
     
    # Drawing letter C
    def draw_C(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # Demi-circle
                    j_save = left + length//2
                    for i in range(0,length+1):
                        j = left + length//2 - int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 )
                        self.draw_pixel(image, i+up, j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+up, u)
                        elif(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i-1+up, u)
                        j_save = j
                    # Two quart-circles
                    j_save = left + length//2
                    for i in range(1,length//3):
                        j = int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 ) + left + length//2
                        self.draw_pixel(image, i+up, j)
                        self.draw_pixel(image, up+length-i, j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i-1+up, u)
                                self.draw_pixel(image, up+length-i+1, u)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter D
    def draw_D(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length/2)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+1,left+line_right):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+line_right):
                        self.draw_pixel(image, up+length, j)
                    # Fird line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left)
                    # Demi-circle
                    j_save = left + line_right
                    for i in range(0,length+1):
                        j = left + int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 ) + line_right
                        self.draw_pixel(image, up+i, j)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+i, u)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i-1, u)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter E
    def draw_E(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right_side = int(length*3/4)
                    line_right_mid = int(length*1/2)
                    if(line_right_side<=0):
                        line_right_side = 1
                    if(line_right_mid<=0):
                        line_right_mid = 1
                    # First line
                    for j in range(left+1,left+line_right_side):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+line_right_side):
                        self.draw_pixel(image, up+length, j)
                    # Fird line
                    for j in range(left+1,left+line_right_mid):
                        self.draw_pixel(image, up+length//2, j)
                    # Fourth line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter F
    def draw_F(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right_side = int(length*3/4)
                    line_right_mid = int(length*1/2)
                    if(line_right_side<=0):
                        line_right_side = 1
                    if(line_right_mid<=0):
                        line_right_mid = 1
                    # First line
                    for j in range(left+1,left+line_right_side):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+line_right_mid):
                        self.draw_pixel(image, up+length//2, j)
                    # Fird line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter G
    def draw_G(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # Demi-circle
                    j_save = left + length//2
                    for i in range(0,length+1):
                        j = left + length//2 - int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 )
                        self.draw_pixel(image, up+i, j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i, u)
                        elif(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+i-1, u)
                        j_save = j
                    # Two quart-circles
                    j_save = left + length//2
                    for i in range(1,length//4):
                        j = int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 ) + left + length//2
                        self.draw_pixel(image, up+i, j)
                        self.draw_pixel(image, up+length-i, j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i-1, u)
                                self.draw_pixel(image, up+length-i+1, u)
                        j_save = j
                    # First bar
                    for i in range(length//2+1,length*3//4+2):
                        self.draw_pixel(image, up+i, j_save)
                    # Second bar
                    for j in range(length//2,length+1):
                        self.draw_pixel(image, up+length//2, left+j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter H
    def draw_H(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length-bar_length)//2)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+bar_length+(length-bar_length)//2)
                    # Fird line
                    for j in range(left+1+(length-bar_length)//2,left+bar_length+(length-bar_length)//2):
                        self.draw_pixel(image, up+length//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter I
    def draw_I(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*2/3)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up+length, j)
                    # Fird line
                    for i in range(up+1,up+length):
                        self.draw_pixel(image, i, left+length//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter J
    def draw_J(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*4/5)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up, j)
                    # Fird line
                    for i in range(up+1,up+length-line_right//4):
                        self.draw_pixel(image, i, left+length//2)
                    # Demi-circle
                    i_save = up+length-line_right//4
                    for j in range(0,line_right//2+1):
                        i = up + int( math.sin(math.acos((j-line_right/4)/(line_right/4)))*line_right/4 ) + length-line_right//4
                        self.draw_pixel(image, i, left+length//2-j)
                        if(i+1<i_save):
                            for u in range(i+1,i_save):
                                self.draw_pixel(image, u, left+length//2-j)
                        elif(i>i_save+1):
                            for u in range(i_save+1,i):
                                self.draw_pixel(image, u, left+length//2-j+1)
                        i_save = i
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter K
    def draw_K(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # First line
                    for i in range(up,up+length):
                        self.draw_pixel(image, i, left)
                    # Second line
                    for j in range(left+1,left+length*4//5):
                        self.draw_pixel(image, up+(length*4//5-j+left)*5//8, j)
                    # Fird line
                    for j in range(left+1,left+length*4//5+1):
                        self.draw_pixel(image, up+(length+(j-left)*5//4)//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter L
    def draw_L(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*3/4)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+1+(length-line_right)//2,left+line_right+(length-line_right)//2):
                        self.draw_pixel(image, up+length, j)
                    # Fird line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length-line_right)//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter M
    def draw_M(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # First line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+length)
                    # Fird line
                    for i in range(1,length//2+1):
                        self.draw_pixel(image, up+i, left+i)
                    # Fourth line
                    for i in range(length//2,length):
                        self.draw_pixel(image, up+length-i, left+i)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter N
    def draw_N(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*3/4)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length-line_right)//2)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+line_right+(length-line_right)//2)
                    # Fird line
                    for i in range(1,length):
                        self.draw_pixel(image, up+i, left+i*line_right//length+(length-line_right)//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter O
    def draw_O(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # Circle
                    j_save = left + length//2
                    for i in range(0,length+1):
                        j = left + length//2 - int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 )
                        if(i!=0 and i!=length):
                            self.draw_pixel(image, up+i, j)
                        self.draw_pixel(image, up+i, 2*left+length-j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i, u)
                                self.draw_pixel(image, up+i, 2*left+length-u)
                        elif(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+i-1, u)
                                self.draw_pixel(image, up+i-1, 2*left+length-u)
                        j_save = j
                    j_border = left + length//2
                    self.draw_pixel(image, up, j_border)
                    self.draw_pixel(image, up+length, j_border)
                    for u in range(j_save+1,j_border):
                        self.draw_pixel(image, length+up, u)
                        self.draw_pixel(image, length+up, 2*left+length-u)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter P
    def draw_P(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*1/2)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+1+(length*3//4-line_right)//2,left+line_right+(length*3//4-line_right)//2):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1+(length*3//4-line_right)//2,left+line_right+(length*3//4-line_right)//2+1):
                        self.draw_pixel(image, up+length//2, j)
                    # Third line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length*3//4-line_right)//2)
                    # Demi-circle
                    j_save = left+(length*3//4-line_right)//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + (length*3//4-line_right)//2
                        self.draw_pixel(image, up+i, line_right+j)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up, u+line_right)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up, u+line_right)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter Q
    def draw_Q(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # Circle
                    j_save = left + length//2
                    for i in range(0,length+1):
                        j = left + length//2 - int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 )
                        if(i!=0 and i!=length):
                            self.draw_pixel(image, up+i, j)
                        self.draw_pixel(image, up+i, 2*left+length-j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i, u)
                                self.draw_pixel(image, up+i, 2*left+length-u)
                        elif(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+i-1, u)
                                self.draw_pixel(image, up+i-1, 2*left+length-u)
                        j_save = j
                    j_border = left + length//2
                    self.draw_pixel(image, up, j_border)
                    self.draw_pixel(image, up+length, j_border)
                    for u in range(j_save+1,j_border):
                        self.draw_pixel(image, length+up, u)
                        self.draw_pixel(image, length+up, 2*left+length-u)
                    # Bar
                    for i in range(length*2//3,length+1):
                        self.draw_pixel(image, up+i, left+i)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter R
    def draw_R(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*1/2)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+1+(length*3//4-line_right)//2,left+line_right+(length*3//4-line_right)//2):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1+(length*3//4-line_right)//2,left+line_right+(length*3//4-line_right)//2+1):
                        self.draw_pixel(image, up+length//2, j)
                    # Third line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length*3//4-line_right)//2)
                    # Demi-circle
                    j_save = left+(length*3//4-line_right)//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + (length*3//4-line_right)//2
                        self.draw_pixel(image, up+i, line_right+j)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up, u+line_right)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up, u+line_right)
                        j_save = j
                    # Bar
                    for i in range(length//2,length+1):
                        j = int(float(left+(length*3/4-line_right)/2+(length/2+i)*(length/2-2*(length*3/4-line_right)/2)/(length/2))-0.000001)+1
                        self.draw_pixel(image, up+i, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter S
    def draw_S(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_length = int(length*1/3)
                    if(line_length<=0):
                        line_length = 1
                    # First line
                    for j in range(left+length//2-line_length//2+1,left+length*3//4+line_length//2):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+length//2-line_length//2+1,left+length//2+line_length//2):
                        self.draw_pixel(image, up+length//2, j)
                    # Third line
                    for j in range(left+length//4-line_length//2+1,left+length//2+line_length//2+1):
                        self.draw_pixel(image, up+length, j)
                    # Two demi-circles
                    j_save = left + length//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + length//2
                        self.draw_pixel(image, i+up, 2*left + length-j-line_length//2)
                        self.draw_pixel(image, i+up+length//2, j+line_length//2)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up, 2*left+length-u-line_length//2)
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up, 2*left+length-u-line_length//2)
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter T
    def draw_T(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*9/10)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for i in range(up+1,up+length+1):
                        self.draw_pixel(image, i, left+length//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter U
    def draw_U(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(up,up+length-bar_length//2):
                        self.draw_pixel(image, i, left+(length-bar_length)//2)
                    # Second line
                    for i in range(up,up+length-bar_length//2):
                        self.draw_pixel(image, i, left+bar_length+(length-bar_length)//2)
                    # Demi-circle
                    j_save = 0
                    for i in range(0,bar_length+1):
                        j = int( math.sin(math.acos((i-bar_length/2)/(bar_length/2)))*bar_length/2 )
                        self.draw_pixel(image, up+length-bar_length//2+j, left+(length-bar_length)//2+i)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+length-bar_length//2+u, left+(length-bar_length)//2+i)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+length-bar_length//2+u, left+(length-bar_length)//2+i-1)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter V
    def draw_V(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # First line
                    for i in range(1,length+1):
                        self.draw_pixel(image, up+length-i, left+(length+i)//2)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(i-up)//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter W
    def draw_W(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    # First line
                    for i in range(1,length+1):
                        self.draw_pixel(image, up+length-i, left+(length*3+i)//4)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(i-up)//4)
                    # Third line
                    for i in range(1,length//2):
                        self.draw_pixel(image, up+length-i, left+(length//2+i)//2)
                    # Fourth line
                    for i in range(up+length//2,up+length+1):
                        self.draw_pixel(image, i, left+(length//2+i-up)//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter X
    def draw_X(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(0,length+1):
                        self.draw_pixel(image, up+length-i, left+(length-bar_length)//2+i*bar_length//length)
                    # Second line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+(length-bar_length)//2+(i-up)*bar_length//length)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter Y
    def draw_Y(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(length//2+1,length+1):
                        self.draw_pixel(image, up+length-i, left+(length-bar_length)//2+i*bar_length//length)
                    # Second line
                    for i in range(up,up+length//2+1):
                        self.draw_pixel(image, i, left+(length-bar_length)//2+(i-up)*bar_length//length)
                    # Third line
                    for i in range(up+length//2,up+length+1):
                        self.draw_pixel(image, i, left+length//2)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter Z
    def draw_Z(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_right = int(length*2/3)
                    if(line_right<=0):
                        line_right = 1
                    # First line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+(length-line_right)//2,left+(length-line_right)//2+line_right+1):
                        self.draw_pixel(image, up+length, j)
                    # Third line
                    for i in range(1,length):
                        self.draw_pixel(image, up+length-i, left+(length-line_right)//2+i*line_right//length)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing word of index idx in N+
    def draw_word(self, image, pos_x, pos_y, idx): # Position : pos=(pos_x,pos_y)
        
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                original_color_values = self.color_values
                if(number_of_dimensions==2 and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(number_of_dimensions==3 and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                base = 26
                exponent = math.floor( math.log( 1 - idx*(1-base)/base )/math.log(base) )
                series = sum(base**k for k in range(1,exponent+1))
                
                num = idx-series
                mod = []
                while(num//base>0):
                    mod.append(num%base)
                    num = num//base
                mod.append(num%base)
                
                length = exponent+1
                for i in range(len(mod),length):
                    mod.append(0)
                
                if(self.adapt_proportion):
                    original_size = self.drawing_size
                    self.drawing_size /= length
                    for i in range(length):
                        self.__draw_letter(image, pos_x+(original_size-self.drawing_size)//2, pos_y+original_size-self.drawing_size*(i+1), mod[i])
                    self.drawing_size = original_size
                else:
                    for i in range(length):
                        self.__draw_letter(image, pos_x, pos_y+self.drawing_size*(length-i-1), mod[i])
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing letter of index idx in [0,25]
    def __draw_letter(self, image, pos_x, pos_y, idx): # Position : pos=(pos_x,pos_y)
        if(idx>=0 and idx<=25):
            if(idx==0):
                self.draw_A(image, pos_x, pos_y)
            elif(idx==1):
                self.draw_B(image, pos_x, pos_y)
            elif(idx==2):
                self.draw_C(image, pos_x, pos_y)
            elif(idx==3):
                self.draw_D(image, pos_x, pos_y)
            elif(idx==4):
                self.draw_E(image, pos_x, pos_y)
            elif(idx==5):
                self.draw_F(image, pos_x, pos_y)
            elif(idx==6):
                self.draw_G(image, pos_x, pos_y)
            elif(idx==7):
                self.draw_H(image, pos_x, pos_y)
            elif(idx==8):
                self.draw_I(image, pos_x, pos_y)
            elif(idx==9):
                self.draw_J(image, pos_x, pos_y)
            elif(idx==10):
                self.draw_K(image, pos_x, pos_y)
            elif(idx==11):
                self.draw_L(image, pos_x, pos_y)
            elif(idx==12):
                self.draw_M(image, pos_x, pos_y)
            elif(idx==13):
                self.draw_N(image, pos_x, pos_y)
            elif(idx==14):
                self.draw_O(image, pos_x, pos_y)
            elif(idx==15):
                self.draw_P(image, pos_x, pos_y)
            elif(idx==16):
                self.draw_Q(image, pos_x, pos_y)
            elif(idx==17):
                self.draw_R(image, pos_x, pos_y)
            elif(idx==18):
                self.draw_S(image, pos_x, pos_y)
            elif(idx==19):
                self.draw_T(image, pos_x, pos_y)
            elif(idx==20):
                self.draw_U(image, pos_x, pos_y)
            elif(idx==21):
                self.draw_V(image, pos_x, pos_y)
            elif(idx==22):
                self.draw_W(image, pos_x, pos_y)
            elif(idx==23):
                self.draw_X(image, pos_x, pos_y)
            elif(idx==24):
                self.draw_Y(image, pos_x, pos_y)
            else:
                self.draw_Z(image, pos_x, pos_y)
        else:
            if(self.message):
                print("WARNING : Index of letter is not between 0 and 25. Drawing canceled.")
    
    # Drawing number 0
    def draw_0(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # Circle
                    j_save = left + length//2
                    for i in range(0,length+1):
                        j = left + length//2 - int( math.sin(math.acos((i-length/2)/(length/2)))*length*(4/5)/2 )
                        if(i!=0 and i!=length):
                            self.draw_pixel(image, up+i, j)
                        self.draw_pixel(image, up+i, 2*left+length-j)
                        if(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, up+i, u)
                                self.draw_pixel(image, up+i, 2*left+length-u)
                        elif(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, up+i-1, u)
                                self.draw_pixel(image, up+i-1, 2*left+length-u)
                        j_save = j
                    j_border = left + length//2
                    self.draw_pixel(image, up, j_border)
                    self.draw_pixel(image, up+length, j_border)
                    for u in range(j_save+1,j_border):
                        self.draw_pixel(image, up+length, u)
                        self.draw_pixel(image, up+length, 2*left+length-u)
                    # Middle line
                    for j in range(left+1+(length-bar_length*2//3)//2,left+bar_length*2//3+(length-bar_length*2//3)//2):
                        self.draw_pixel(image, up+length//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 1
    def draw_1(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(up,up+length):
                        self.draw_pixel(image, i, left+length//2)
                    # Second line
                    for i in range(up+int(length/bar_length-0.000001)+1,up+length//2+1):
                        self.draw_pixel(image, i, left+length//2-(i-up)*bar_length//length)
                    # Third line
                    for j in range(left+(length-bar_length)//2,left+(length-bar_length)//2+bar_length+1):
                        self.draw_pixel(image, up+length, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 2
    def draw_2(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    circle_prop = 0.7
                    begin = length*math.sqrt(2)/2
                    # Two demi-circles - top
                    js_save = int(circle_prop * int( math.sin(math.acos((length-int(length-begin)-length/2)/(length/2)))*length/2 ) + left + length//2)
                    for k in range(int(circle_prop*(length-begin)),int(circle_prop*length-0.000001)+2):
                        i = -1.0/circle_prop*k+length
                        if(i<0):
                            i = 0.0
                        elif(i>length):
                            i = length
                        js = int(circle_prop * int( math.sin(math.acos((i-length/2)/(length/2)))*length/2 ) + left + length//2 - 0.000001) + 1
                        if(k!=int(circle_prop*(length-begin))):
                            self.draw_pixel(image, int(circle_prop*i+up), js)
                        if(k!=int(circle_prop*length-0.000001)+1):
                            self.draw_pixel(image, int(circle_prop*i+up), 2*left+length-js)
                        
                        if(js+1<js_save):
                            for u in range(js+1,js_save):
                                self.draw_pixel(image, int(circle_prop*i+up), u)
                                self.draw_pixel(image, int(circle_prop*i+up), 2*left+length-u)
                        elif(js>js_save+1):
                            for u in range(js_save+1,js):
                                self.draw_pixel(image, int(circle_prop*i+1+up), u)
                                self.draw_pixel(image, int(circle_prop*i+1+up), 2*left+length-u)
                        js_save = js
                    # First line
                    j_start = int(circle_prop * int( math.sin(math.acos((length-int(length-begin)-length/2)/(length/2)))*length/2 ) + length/2 - 0.000001) + 1
                    i_start = int(circle_prop*(-1.0/circle_prop*int(circle_prop*(length-begin))+length))
                    for j in range(int((1.0-circle_prop)*length/2),j_start):
                        i = int( 1.0*length-float(j-int((1.0-circle_prop)*length/2))/(j_start-int((1.0-circle_prop)*length/2))*(length-i_start) )
                        self.draw_pixel(image, up+i, left+j)
                    # Second line
                    for j in range(int(-circle_prop*length/2+left+length/2)+1,int(circle_prop*length/2+left+length/2-0.000001)+2):
                        self.draw_pixel(image, up+length, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 3
    def draw_3(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_length = int(length*1/3)
                    if(line_length<=0):
                        line_length = 1
                    # First line
                    for j in range(left+length//4-line_length//2+1,left+length//2+line_length//2):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+length//2,left+length//2+line_length//2+1):
                        self.draw_pixel(image, int(-0.000001+up+length/2)+1, j)
                    # Third line
                    for j in range(left+length//4-line_length//2+1,left+length//2+line_length//2+1):
                        self.draw_pixel(image, up+length, j)
                    # Two demi-circles
                    j_save = left + length//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + length//2
                        self.draw_pixel(image, i+up, j+line_length//2)
                        if(k!=length//2):
                            self.draw_pixel(image, i+up+length//2, j+line_length//2)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up, u+line_length//2)
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up, u+line_length//2)
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 4
    def draw_4(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for i in range(up,up+length+1):
                        self.draw_pixel(image, i, left+length//2)
                    # Second line
                    for j in range(left+1,left+length//2):
                        self.draw_pixel(image, up+length//2-j+left, j)
                    # Third line
                    for j in range(left,left+(length-bar_length)//2+bar_length+1):
                        self.draw_pixel(image, up+length//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 5
    def draw_5(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_length = int(length*1/3)
                    if(line_length<=0):
                        line_length = 1
                    # First line
                    for j in range(left+1,left+length*3//4+line_length//2):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+length//2+line_length//2):
                        self.draw_pixel(image, up+length//2, j)
                    # Third line
                    for j in range(left,left+length//2+line_length//2+1):
                        self.draw_pixel(image, up+length, j)
                    # Fourth line
                    for i in range(up,up+length//2+1):
                        self.draw_pixel(image, i, left)
                    # Two demi-circles
                    j_save = left + length//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + length//2
                        self.draw_pixel(image, i+up+length//2, j+line_length//2)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 6
    def draw_6(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_length = int(length*1/3)
                    if(line_length<=0):
                        line_length = 1
                    # Bee line
                    for i in range(up+1,up+length//4):
                        self.draw_pixel(image, i, left+length*3//4+line_length//2-1)
                    # First line
                    for j in range(left+1,left+length*3//4+line_length//2-1):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for j in range(left+1,left+length//2+line_length//2):
                        self.draw_pixel(image, up+length//2, j)
                    # Third line
                    for j in range(left+1,left+length//2+line_length//2+1):
                        self.draw_pixel(image, up+length, j)
                    # Fourth line
                    for i in range(up+1,up+length):
                        self.draw_pixel(image, i, left)
                    # Demi-circles
                    j_save = left + length//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + length//2
                        self.draw_pixel(image, i+up+length//2, j+line_length//2)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, i+1+up+length//2, u+line_length//2)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 7
    def draw_7(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    bar_length = length*3//4
                    if(bar_length<=0):
                        bar_length = 1
                    # First line
                    for j in range(left,left+length+1):
                        self.draw_pixel(image, up, j)
                    # Second line
                    for i in range(up+1,up+length+1):
                        self.draw_pixel(image, i, left+length-i+up)
                    # Third line
                    for j in range(left+(length-bar_length)//2+1,left+(length-bar_length)//2+bar_length+1):
                        self.draw_pixel(image, up+length//2, j)
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 8
    def draw_8(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    circle_prop = 0.45
                    begin = length
                    # Two demi-circles - top
                    js_save = int(circle_prop * int( math.sin(math.acos((length-int(length-begin)-length/2)/(length/2)))*length/2 ) + left + length//2)
                    for k in range(int(circle_prop*(length-begin)),int(circle_prop*length-0.000001)+2):
                        i = -1.0/circle_prop*k+length
                        if(i<0):
                            i = 0.0
                        elif(i>length):
                            i = length
                        js = int(circle_prop * int( math.sin(math.acos((i-length/2)/(length/2)))*length/2*1.5 ) + left + length//2 - 0.000001) + 1
                        self.draw_pixel(image, int(circle_prop*i+up), js)
                        if(k!=int(circle_prop*length-0.000001)+1 and k!=int(circle_prop*(length-begin))):
                            self.draw_pixel(image, int(circle_prop*i+up), 2*left+length-js)
                        if(js+1<js_save):
                            for u in range(js+1,js_save):
                                self.draw_pixel(image, int(circle_prop*i+up), u)
                                self.draw_pixel(image, int(circle_prop*i+up), 2*left+length-u)
                        elif(js>js_save+1):
                            for u in range(js_save+1,js):
                                self.draw_pixel(image, int(circle_prop*i+1+up), u)
                                self.draw_pixel(image, int(circle_prop*i+1+up), 2*left+length-u)
                        js_save = js
                    # Two demi-circles - bottom
                    circle_prop = 1.0-circle_prop
                    begin = length
                    js_save = int(circle_prop * int( math.sin(math.acos((length-int(length-begin)-length/2)/(length/2)))*length/2 ) + left + length//2)
                    for k in range(int(circle_prop*(length-begin)),int(circle_prop*length-0.000001)+2):
                        i = -1.0/circle_prop*k+length
                        if(i<0):
                            i = 0.0
                        elif(i>length):
                            i = length
                        js = int(circle_prop * int( math.sin(math.acos((i-length/2)/(length/2)))*length/2*1.5 ) + left + length//2 - 0.000001) + 1
                        self.draw_pixel(image, int(circle_prop*i+up+length*(1.0-circle_prop)), js)
                        if(k!=int(circle_prop*length-0.000001)+1 and k!=int(circle_prop*(length-begin))):
                            self.draw_pixel(image, int(circle_prop*i+up+length*(1.0-circle_prop)), 2*left+length-js)
                        if(js+1<js_save):
                            for u in range(js+1,js_save):
                                self.draw_pixel(image, int(circle_prop*i+up+length*(1.0-circle_prop)), u)
                                self.draw_pixel(image, int(circle_prop*i+up+length*(1.0-circle_prop)), 2*left+length-u)
                        elif(js>js_save+1):
                            for u in range(js_save+1,js):
                                self.draw_pixel(image, int(circle_prop*i+1+up+length*(1.0-circle_prop)), u)
                                self.draw_pixel(image, int(circle_prop*i+1+up+length*(1.0-circle_prop)), 2*left+length-u)
                        js_save = js
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number 9
    def draw_9(self, image, pos_x, pos_y): # Position : pos=(pos_x,pos_y)
    
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                is_2D = number_of_dimensions==2
                
                original_color_values = self.color_values
                if(is_2D and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(not(is_2D) and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                up = int(pos_x + self.drawing_size*(1-self.proportion)/2)
                left = int(pos_y + self.drawing_size*(1-self.proportion)/2)
                length = int(self.drawing_size*self.proportion)
                
                if(length>0):
                    line_length = int(length*1/3)
                    if(line_length<=0):
                        line_length = 1
                    # First line
                    for j in range(left+2,left+length*3//4+line_length//2+1):
                        self.draw_pixel(image, up+length, 2*left+length-j)
                    # Second line
                    for j in range(left+2,left+length//2+line_length//2+1):
                        self.draw_pixel(image, up+length//2, 2*left+length-j)
                    # Third line
                    for j in range(left+2,left+length//2+line_length//2+2):
                        self.draw_pixel(image, up, 2*left+length-j)
                    # Fourth line
                    for i in range(up+1,up+length):
                        self.draw_pixel(image, 2*up+length-i, left+length-1)
                    # Two demi-circles
                    j_save = left + length//2
                    for k in range(0,length//2+1):
                        i = length//2-k
                        j = int( math.sin(math.acos((i-length/4)/(length/4)))*length/4 ) + left + length//2
                        self.draw_pixel(image, int(-0.000001+up-i+length/2)+1, 2*left+length-j-line_length//2-1)
                        if(j+1<j_save):
                            for u in range(j+1,j_save):
                                self.draw_pixel(image, int(-0.000001+up-i-1+length/2)+1, 2*left+length-u-line_length//2-1)
                        elif(j>j_save+1):
                            for u in range(j_save+1,j):
                                self.draw_pixel(image, int(-0.000001+up-i-1+length/2)+1, 2*left+length-u-line_length//2-1)
                        j_save = j
                else:
                    self.draw_pixel(image, up, left)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing number of index idx in N+
    def draw_number(self, image, pos_x, pos_y, idx): # Position : pos=(pos_x,pos_y)
        
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                original_color_values = self.color_values
                if(number_of_dimensions==2 and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(number_of_dimensions==3 and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                num = idx
                mod = []
                while(num//10>0):
                    mod.append(num%10)
                    num = num//10
                mod.append(num%10)
                length = len(mod)
                if(self.adapt_proportion):
                    original_size = self.drawing_size
                    self.drawing_size /= length
                    for i in range(0,length):
                        self.__draw_numeral(image, pos_x+(original_size-self.drawing_size)//2, pos_y+original_size-self.drawing_size*(i+1), mod[i])
                    self.drawing_size = original_size
                else:
                    for i in range(0,length):
                        self.__draw_numeral(image, pos_x, pos_y+self.drawing_size*(length-i-1), mod[i])
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing numeral of index idx in [0,25]
    def __draw_numeral(self, image, pos_x, pos_y, idx): # Position : pos=(pos_x,pos_y)
        if(idx>=0 and idx<=9):
            if(idx==0):
                self.draw_0(image, pos_x, pos_y)
            elif(idx==1):
                self.draw_1(image, pos_x, pos_y)
            elif(idx==2):
                self.draw_2(image, pos_x, pos_y)
            elif(idx==3):
                self.draw_3(image, pos_x, pos_y)
            elif(idx==4):
                self.draw_4(image, pos_x, pos_y)
            elif(idx==5):
                self.draw_5(image, pos_x, pos_y)
            elif(idx==6):
                self.draw_6(image, pos_x, pos_y)
            elif(idx==7):
                self.draw_7(image, pos_x, pos_y)
            elif(idx==8):
                self.draw_8(image, pos_x, pos_y)
            else:
                self.draw_9(image, pos_x, pos_y)
        else:
            if(self.message):
                print("WARNING : Index of numeral is not between 0 and 9. Drawing canceled.")
    
    # Drawing a string on image : all letters and numerals considered
    def draw_string(self, image, pos_x, pos_y, string): # 'string' is a string
        
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                original_color_values = self.color_values
                if(number_of_dimensions==2 and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(number_of_dimensions==3 and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                string = str(string)
                length = len(string)
                if(self.adapt_proportion):
                    original_size = self.drawing_size
                    self.drawing_size /= length
                    for i in range(0,length):
                        self.__draw_symbol(image, pos_x+(original_size-self.drawing_size)//2, pos_y+self.drawing_size*i, string[i])
                    self.drawing_size = original_size
                else:
                    for i in range(0,length):
                        self.__draw_symbol(image, pos_x, pos_y+self.drawing_size*i, string[i])
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Writing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Writing canceled.")
    
    # Drawing a symbol on image : either a letter or a numeral
    def __draw_symbol(self, image, pos_x, pos_y, symbol): # 'symbol' is a string
        if(type(symbol) is str):
            if(len(symbol)>=1):
                if(len(symbol)>1 and self.message):
                    print("WARNING : Entered 'symbol' string contains at least two chars. Only the first char of 'symbol' string will be drawn.")
                
                sym = symbol[0]
                
                if(sym=='a' or sym=='A'):
                    self.draw_A(image, pos_x, pos_y)
                elif(sym=='b' or sym=='B'):
                    self.draw_B(image, pos_x, pos_y)
                elif(sym=='c' or sym=='C'):
                    self.draw_C(image, pos_x, pos_y)
                elif(sym=='d' or sym=='D'):
                    self.draw_D(image, pos_x, pos_y)
                elif(sym=='e' or sym=='E'):
                    self.draw_E(image, pos_x, pos_y)
                elif(sym=='f' or sym=='F'):
                    self.draw_F(image, pos_x, pos_y)
                elif(sym=='g' or sym=='G'):
                    self.draw_G(image, pos_x, pos_y)
                elif(sym=='h' or sym=='H'):
                    self.draw_H(image, pos_x, pos_y)
                elif(sym=='i' or sym=='I'):
                    self.draw_I(image, pos_x, pos_y)
                elif(sym=='j' or sym=='J'):
                    self.draw_J(image, pos_x, pos_y)
                elif(sym=='k' or sym=='K'):
                    self.draw_K(image, pos_x, pos_y)
                elif(sym=='l' or sym=='L'):
                    self.draw_L(image, pos_x, pos_y)
                elif(sym=='m' or sym=='M'):
                    self.draw_M(image, pos_x, pos_y)
                elif(sym=='n' or sym=='N'):
                    self.draw_N(image, pos_x, pos_y)
                elif(sym=='o' or sym=='O'):
                    self.draw_O(image, pos_x, pos_y)
                elif(sym=='p' or sym=='P'):
                    self.draw_P(image, pos_x, pos_y)
                elif(sym=='q' or sym=='Q'):
                    self.draw_Q(image, pos_x, pos_y)
                elif(sym=='r' or sym=='R'):
                    self.draw_R(image, pos_x, pos_y)
                elif(sym=='s' or sym=='S'):
                    self.draw_S(image, pos_x, pos_y)
                elif(sym=='t' or sym=='T'):
                    self.draw_T(image, pos_x, pos_y)
                elif(sym=='u' or sym=='U'):
                    self.draw_U(image, pos_x, pos_y)
                elif(sym=='v' or sym=='V'):
                    self.draw_V(image, pos_x, pos_y)
                elif(sym=='w' or sym=='W'):
                    self.draw_W(image, pos_x, pos_y)
                elif(sym=='x' or sym=='X'):
                    self.draw_X(image, pos_x, pos_y)
                elif(sym=='y' or sym=='Y'):
                    self.draw_Y(image, pos_x, pos_y)
                elif(sym=='z' or sym=='Z'):
                    self.draw_Z(image, pos_x, pos_y)
                
                elif(sym=='0'):
                    self.draw_0(image, pos_x, pos_y)
                elif(sym=='1'):
                    self.draw_1(image, pos_x, pos_y)
                elif(sym=='2'):
                    self.draw_2(image, pos_x, pos_y)
                elif(sym=='3'):
                    self.draw_3(image, pos_x, pos_y)
                elif(sym=='4'):
                    self.draw_4(image, pos_x, pos_y)
                elif(sym=='5'):
                    self.draw_5(image, pos_x, pos_y)
                elif(sym=='6'):
                    self.draw_6(image, pos_x, pos_y)
                elif(sym=='7'):
                    self.draw_7(image, pos_x, pos_y)
                elif(sym=='8'):
                    self.draw_8(image, pos_x, pos_y)
                elif(sym=='9'):
                    self.draw_9(image, pos_x, pos_y)
                
                else:
                    if(self.message):
                        print("WARNING : Entered 'symbol' string is not recognized as a valid writing symbol. Symbol drawing canceled.")
            else:
                if(self.message):
                    print("WARNING : Entered 'symbol' string contains no char. Impossible to draw void symbol. Symbol drawing canceled.")
        else:
            if(self.message):
                print("WARNING : Wrong object type for 'symbol' parameter in '__draw_symbol()' function. Symbol drawing canceled.")
    
    
    ### SECONDARY METHODS OF THE 'WRITER' CLASS - NOT PRIVATE HERE
    
    # Current contrasted colors regarding image, focused pixel and self 'writer' object properties
    def get_calculated_contrasted_colors(self, image, pixel=None):
        return image_calculator.calculate_contrasted_colors(image=image, color_values=self.color_values, main_contrast_exponent=self.main_contrast_exponent, color_contrast_proportion=self.color_contrast_proportion, focused_pixel=pixel, pixel_importance_proportion=self.pixel_color_study_proportion, message=self.message)
    
    # Drawing pixel at position (pos_x,pos_y) on 2D or 3D image !Not private method!
    def draw_pixel(self, image, pos_x, pos_y):
        is_2D = np.shape(np.shape(image))[0]==2
        try:
            if(self.pixel_color_study_proportion==0 and self.color_already_calculated):
                current_colors = self.saved_contrasted_colors
            else:
                current_colors = self.get_calculated_contrasted_colors(image=image, pixel=np.array([pos_x,pos_y]))
            
            if(is_2D):
                image[pos_x,pos_y] = int( image[pos_x,pos_y]*(1-self.transparency) + 255*current_colors*self.transparency )
            else:
                image[pos_x,pos_y,0] = int( image[pos_x,pos_y,0]*(1-self.transparency) + 255*current_colors[0]*self.transparency )
                image[pos_x,pos_y,1] = int( image[pos_x,pos_y,1]*(1-self.transparency) + 255*current_colors[1]*self.transparency )
                image[pos_x,pos_y,2] = int( image[pos_x,pos_y,2]*(1-self.transparency) + 255*current_colors[2]*self.transparency )
        except:
            if(self.message):
                if(is_2D):
                    print("WARNING : Impossible to change 2D image pixel value at ({},{})!".format(pos_x, pos_y))
                else:
                    print("WARNING : Impossible to change 3D image pixel values at ({},{})!".format(pos_x, pos_y))





# DRAWER class to draw figures or shapes on ndarray-formatted images
class drawer :
    
    
    ### INITIALIZATION OF THE 'DRAWER' OBJECT
    
    # DESCRIPTION OF REQUIRED STATIC PARAMETERS
    """
    # color_values : an object for the chosen color. It can be a float/int (-> NOT colorized, ie Black&White) or a list/ndarray of floats (-> colorized)
    # main_contrast_exponent : a positive float/int for the global contrast exponent of the chosen color regarding the image colors MEANS. ==1 -> Neutral ; <1 -> less contrasted ; >1 -> more contrasted
    # color_contrast_proportion : a float/int between 0 and 1 included for the proportion of the contrast between the three colors (BGR) of the chosen colors. ==0.5 -> Neutral ; <0.5 -> less contrasted ; >0.5 -> more contrasted
    # pixel_color_study_proportion : a float/int between 0 and 1 included for the proportion of the weight of the currently studied pixel colors taken into account. ==0 <-> Pixel not taken into account (faster!!)
    # transparency : a float/int between 0 and 1 included for the transparency of the drawings on the considered 2D or 3D images
    # message : a boolean to allow or not the display of warning messages
    """
    
    # Initialization of the static parameters
    def __init__(self, color_values = 'inverted_mean_proportion', main_contrast_exponent = 1.0, color_contrast_proportion = 0.5, pixel_color_study_proportion = 0.0, transparency = 1.0, message = False):
        self.set_message_allowed(message)
        self.set_pixel_color_study_proportion(pixel_color_study_proportion)
        self.set_main_contrast_exponent(main_contrast_exponent)
        self.set_color_contrast_proportion(color_contrast_proportion)
        self.set_color_values(color_values)
        self.set_transparency(transparency)
        self.color_already_calculated = False # Dynamic parameter
    
    
    ### GETTERS AND SETTERS OF THE 'DRAWER' PARAMETERS
    
    # Getting current color values
    def get_color_values(self):
        return self.color_values
    
    # Setting current color values
    def set_color_values(self, color_values):
        if((type(color_values) is str and color_values=='inverted_mean_proportion') or color_values is None):
            self.color_values = 'inverted_mean_proportion'
        elif(type(color_values) is np.ndarray or type(color_values) is list or type(color_values) is tuple): # 'color_values' is a list/ndarray <=> image is colorized (3 dim)
            if(type(color_values) is list or type(color_values) is tuple):
                color_values = np.array(color_values)
            number_of_dimensions = np.shape(np.shape(color_values))[0]
            if(number_of_dimensions==1):
                if(color_values.dtype == np.float_ or color_values.dtype == np.int_):
                    number_of_floats = np.shape(color_values)[0]
                    if(number_of_floats!=3):
                        if(number_of_floats<=0):
                            self.color_values = np.array([0.5,0.5,0.5])
                        elif(number_of_floats==1):
                            self.color_values = np.array([float(color_values[0]),float(color_values[0]),float(color_values[0])])
                        elif(number_of_floats==2):
                            self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[1])])
                        else: # Too many floats!
                            self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[2])])
                        if(self.message):
                            print("WARNING : Wrong number of floats in 'color_values' list/ndarray! Must be 3 if image is colorized, or a float if not. Found:",number_of_floats,". Array has now been adapted.")
                    else:
                        self.color_values = np.array([float(color_values[0]),float(color_values[1]),float(color_values[2])])
                else:
                    self.color_values = 'inverted_mean_proportion'
                    if(self.message):
                        print("WARNING : Wrong object format inside 'color_values' list/ndarray! Must be only floats. Array has been adapted to 'inverted_mean_proportion'.")
            else:
                self.color_values = 'inverted_mean_proportion'
                if(self.message):
                    print("WARNING : Wrong number of dimensions in 'color_values' list/ndarray! Must be only 1 if image is colorized, or a float if not. Found:",number_of_dimensions,". Array has now been adapted to 'inverted_mean_proportion'.")
        elif(type(color_values) is float or type(color_values) is int): # 'color_values' is a float/int <=> image is not colorized (2 dim)
            self.color_values = float(color_values)
        else:
            self.color_values = 'inverted_mean_proportion'
            if(self.message):
                print("WARNING : Wrong object format for 'color_values'! Must be a float/int if image is not colorized (2D), or a list/ndarray of 3 floats if colorized (3D). Value of 'color_values' has been adapted to 'inverted_mean_proportion'.")
    
    # Getting current main_contrast_exponent
    def get_main_contrast_exponent(self):
        return self.main_contrast_exponent
    
    # Setting current main_contrast_exponent
    def set_main_contrast_exponent(self, main_contrast_exponent): # 'main_contrast_exponent' is float >=0
        if(type(main_contrast_exponent) is float or type(main_contrast_exponent) is int):
            if(main_contrast_exponent>=0):
                self.main_contrast_exponent = main_contrast_exponent
            else:
                self.drawmain_contrast_exponenting_size = 0.0
                if(self.message):
                    print("WARNING : Value of 'main_contrast_exponent' must be >=0. This value has been adapted to 0.0.")
        else:
            self.main_contrast_exponent = 1.0
            if(self.message):
                print("WARNING : Wrong object format for 'main_contrast_exponent'! Must be an int or a float. Value of 'main_contrast_exponent' has been adapted to 1.0.")
    
    # Getting current color_contrast_proportion
    def get_color_contrast_proportion(self):
        return self.color_contrast_proportion
    
    # Setting current color_contrast_proportion
    def set_color_contrast_proportion(self, color_contrast_proportion):
        if(type(color_contrast_proportion) is float or type(color_contrast_proportion) is int):
            if(color_contrast_proportion<=1 and color_contrast_proportion>=0):
                self.color_contrast_proportion = float(color_contrast_proportion)
            else:
                self.color_contrast_proportion = 0.5
                if(self.message):
                    print("WARNING : Value of 'color_contrast_proportion' must be between 0 and 1 included. This value has been adapted to 0.5.")
        else:
            self.color_contrast_proportion = 0.5
            if(self.message):
                print("WARNING : Wrong object format for 'color_contrast_proportion'! Must be a float or an int, between 0 and 1 included. Value of 'color_contrast_proportion' has been adapted to 0.5.")
    
    # Getting current pixel_color_study_proportion
    def get_pixel_color_study_proportion(self):
        return self.pixel_color_study_proportion
    
    # Setting current pixel_color_study_proportion
    def set_pixel_color_study_proportion(self, pixel_color_study_proportion):
        if(type(pixel_color_study_proportion) is float or type(pixel_color_study_proportion) is int):
            if(pixel_color_study_proportion<=1 and pixel_color_study_proportion>=0):
                self.pixel_color_study_proportion = float(pixel_color_study_proportion)
            else:
                self.pixel_color_study_proportion = 0.0
                if(self.message):
                    print("WARNING : Value of 'pixel_color_study_proportion' must be between 0 and 1 included. This value has been adapted to 0.0.")
        else:
            self.pixel_color_study_proportion = 0.0
            if(self.message):
                print("WARNING : Wrong object format for 'pixel_color_study_proportion'! Must be a float or an int, between 0 and 1 included. Value of 'pixel_color_study_proportion' has been adapted to 0.0.")
    
    # Getting current transparency
    def get_transparency(self):
        return self.transparency
    
    # Setting current transparency
    def set_transparency(self, transparency):
        if(type(transparency) is float or type(transparency) is int):
            if(transparency<=1 and transparency>=0):
                self.transparency = float(transparency)
            else:
                self.transparency = 1.0
                if(self.message):
                    print("WARNING : Value of 'transparency' must be between 0 and 1 included. This value has been adapted to 1.0.")
        else:
            self.transparency = 1.0
            if(self.message):
                print("WARNING : Wrong object format for 'transparency'! Must be a float or an int, between 0 and 1 included. Value of 'transparency' has been adapted to 1.0.")
    
    # Getting current message
    def get_message_allowed(self):
        return self.message
    
    # Setting current message
    def set_message_allowed(self, message):
        if(type(message) is bool):
            self.message = message
        else:
            self.message = False
            if(message):
                print("WARNING : Wrong object format for 'message'! Must be a bool. Position of 'message' has been adapted to False. No more warnings will be displayed.")
    
    
    ### MAIN SPECIFIC METHODS OF THE 'WRITER' CLASS
    
    # Drawing a specific grid on image with drawig and writing properties
    def draw_grid(self, image, number_squares = 15, pixels_write = 1, pixels_space = 1, line_width = 1, min_mode = False, writing_size = 'compute_writing_size', writing_proportion = 1.0, adapt_writing_proportion = False) : # Add grid of minimum/maximum number of squares number_squares*number_squares with letters and numbers on image
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                original_color_values = self.color_values
                if(number_of_dimensions==2 and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(number_of_dimensions==3 and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                height,width = np.shape(image)[:2]
                
                if(min_mode):
                    max_length = min(height,width)
                else:
                    max_length = max(height,width)
                
                square_length = float(max_length)/number_squares
                
                prop = 0.8
                
                if((type(writing_size) is str and  writing_size == 'compute_writing_size') or writing_size is None):
                    square_size = square_length*prop/2 # Divided by 2 to leave enough space for 2 digits
                else:
                    square_size = writing_size
                
                # Letters writer building
                write = writer(drawing_size = square_size, proportion = writing_proportion, adapt_proportion = adapt_writing_proportion, color_values = self.color_values, main_contrast_exponent = self.main_contrast_exponent, color_contrast_proportion = self.color_contrast_proportion, pixel_color_study_proportion = self.pixel_color_study_proportion, transparency = self.transparency, message = self.message)
                
                #####
                
                ## Vertical lines
                
                for k in range(1,int( number_squares*width/(max_length+int(line_width/2)+1) )+1):
                    column = int(square_length*k)
                    i=0
                    while(i<height):
                        for i in range(i,i+pixels_write):
                            if(i<height):
                                for j in range(column-int(line_width/2),column+int((line_width-1)/2)+1):
                                    self.draw_pixel(image, i, j)
                            else:
                                break
                        i += pixels_space+1
                
                ## Horizontal lines
                
                for k in range(1,int( number_squares*height/(max_length+int(line_width/2)+1) )+1):
                    line = int(square_length*k)
                    i=0
                    while(i<width):
                        for i in range(i,i+pixels_write):
                            if(i<width):
                                for j in range(line-int(line_width/2),line+int((line_width-1)/2)+1):
                                    self.draw_pixel(image, j, i)
                            else:
                                break
                        i += pixels_space+1
                
                ## Letters and numbers
                
                marge_left = square_length*(1-prop)/2 + 1.000001
                marge_up = square_length/4+marge_left
                
                for k in range(0, int( number_squares*width/(max_length+int(line_width/2)+1) )+1):
                    write.draw_word(image, marge_up/4, marge_left + square_length*k, k)
                
                for k in range(0, int( number_squares*height/(max_length+int(line_width/2)+1) )+1):
                    write.draw_number(image, marge_up*7/5 + square_length*k, marge_left, k+1)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Grid drawing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Grid drawing canceled.")
        if(self.message):
            print("\nCURRENT IMAGE :\n",image,"\n")
    
    # Drawing keypoints : a disk & a word or a number
    def draw_keypoint(self, image, pos_x, pos_y, disk_radius = 'compute_disk_radius', word = '', writing_size = 'compute_writing_size', writing_proportion = 1.0, adapt_writing_proportion = False):
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2 or number_of_dimensions==3):
                
                original_color_values = self.color_values
                if(number_of_dimensions==2 and type(self.color_values) is np.ndarray):
                    self.color_values = float((self.color_values[0]+self.color_values[1]+self.color_values[2])/3)
                    if(self.message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is ndarray. Writing color value had been put to the average of the three 'color_values' array values.")
                elif(number_of_dimensions==3 and type(self.color_values) is float):
                    self.color_values = np.array([self.color_values,self.color_values,self.color_values])
                    if(self.message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float. Writing color object had been put to a ndarray with three of the 'color_values' float value.")
                has_already_been_calculated = self.color_already_calculated
                if(self.pixel_color_study_proportion==0):
                    if(not(has_already_been_calculated)):
                        self.saved_contrasted_colors = self.get_calculated_contrasted_colors(image)
                        self.color_already_calculated = True
                
                #####
                
                height,width = np.shape(image)[:2]
                
                max_length = max(height,width)
                
                if((type(writing_size) is str and  writing_size == 'compute_writing_size') or writing_size is None):
                    square_size = max_length/100 # Max length divided by 100
                else:
                    square_size = writing_size
                
                # Letters writer building
                write = writer(drawing_size = square_size, proportion = writing_proportion, adapt_proportion = adapt_writing_proportion, color_values = self.color_values, main_contrast_exponent = self.main_contrast_exponent, color_contrast_proportion = self.color_contrast_proportion, pixel_color_study_proportion = self.pixel_color_study_proportion, transparency = self.transparency, message = self.message)
                
                if((type(disk_radius) is str and  disk_radius == 'compute_disk_radius') or disk_radius is None):
                    radius = max_length/400 # Max length divided by 400
                else:
                    radius = disk_radius
                
                #####
                
                ## Disk drawing
                
                for i in range(int(pos_x-radius), int(np.ceil(pos_x+radius))+1):
                    for j in range(int(pos_y-radius), int(np.ceil(pos_y+radius))+1):
                        if( (i-pos_x)**2 + (j-pos_y)**2 <= radius**2 ):
                            self.draw_pixel(image, i, j)
                
                ## Word drawing
                
                x_word_pos = pos_x - radius - square_size
                y_word_pos = pos_y + radius
                write.draw_string(image, x_word_pos, y_word_pos, word)
                
                #####
                
                if(not(type(self.color_values) is type(original_color_values))):
                    self.color_values = original_color_values
                if(not(has_already_been_calculated)):
                    self.color_already_calculated = False
                
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! Grid drawing canceled.")
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Grid drawing canceled.")
        if(self.message):
            print("\nCURRENT IMAGE :\n",image,"\n")
    
    
    ### SECONDARY METHODS OF THE 'WRITER' CLASS - NOT PRIVATE HERE
    
    # Current contrasted colors regarding image, focused pixel and self 'writer' object properties
    def get_calculated_contrasted_colors(self, image, pixel=None):
        return image_calculator.calculate_contrasted_colors(image=image, color_values=self.color_values, main_contrast_exponent=self.main_contrast_exponent, color_contrast_proportion=self.color_contrast_proportion, focused_pixel=pixel, pixel_importance_proportion=self.pixel_color_study_proportion, message=self.message)
    
    # Drawing pixel at position (pos_x,pos_y) on 2D or 3D image !Not private method!
    def draw_pixel(self, image, pos_x, pos_y):
        is_2D = np.shape(np.shape(image))[0]==2
        try:
            if(self.pixel_color_study_proportion==0 and self.color_already_calculated):
                current_colors = self.saved_contrasted_colors
            else:
                current_colors = self.get_calculated_contrasted_colors(image=image, pixel=np.array([pos_x,pos_y]))
            
            if(is_2D):
                image[pos_x,pos_y] = int( image[pos_x,pos_y]*(1-self.transparency) + 255*current_colors*self.transparency )
            else:
                image[pos_x,pos_y,0] = int( image[pos_x,pos_y,0]*(1-self.transparency) + 255*current_colors[0]*self.transparency )
                image[pos_x,pos_y,1] = int( image[pos_x,pos_y,1]*(1-self.transparency) + 255*current_colors[1]*self.transparency )
                image[pos_x,pos_y,2] = int( image[pos_x,pos_y,2]*(1-self.transparency) + 255*current_colors[2]*self.transparency )
        except:
            if(self.message):
                if(is_2D):
                    print("WARNING : Impossible to change 2D image pixel value at ({},{})!".format(pos_x, pos_y))
                else:
                    print("WARNING : Impossible to change 3D image pixel values at ({},{})!".format(pos_x, pos_y))





# IMAGE_CAlCULATOR class to gather some image calculation methods
class image_calculator :
    
    # Returning image colors mean regarding the studdied image properties
    def calculate_image_mean(image): # From 0 to 255 included (int)
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2):
                return np.mean(image)
            elif(number_of_dimensions==3):
                return np.array([np.mean(image[:,:,0]),np.mean(image[:,:,1]),np.mean(image[:,:,2])])
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! 0 returned.")
                return 0
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". 0 returned.")
            return 0
    
    # Contrasted chosen colors regarding image colors averages and focused pixel colors
    def calculate_contrasted_colors(image, color_values='inverted_mean_proportion', main_contrast_exponent=1.0, color_contrast_proportion=0.5, focused_pixel=None, pixel_importance_proportion=0.0, message=False): # From 0.0 to 1.0 included (float) - 'main_contrast_exponent' is float >=0 - 'color_contrast_proportion' is float between 0.0 and 1.0 included. 0.5 is for no change, 1.0 for full contrasted, 0.0 for b&w
        if(type(image) is np.ndarray):
            number_of_dimensions = np.shape(np.shape(image))[0]
            if(number_of_dimensions==2):
                
                if((type(focused_pixel) is list or type(focused_pixel) is np.ndarray or type(focused_pixel) is tuple) and np.shape(np.shape(focused_pixel))[0]==1 and np.shape(focused_pixel)[0]>=2):
                    pixel = np.array([focused_pixel[0],focused_pixel[1]])
                    importance = pixel_importance_proportion
                    if(np.shape(focused_pixel)[0]>2 and message):
                        print("WARNING : Entered 'focused_pixel' parameter contains more than two coordinates. Only the first two have been considered to build focused pixel.")
                elif(focused_pixel is None):
                    pixel = np.array([0,0])
                    importance = 0
                    if(pixel_importance_proportion>0 and message):
                        print("WARNING : No 'focused_pixel' parameter entered, but 'pixel_importance_proportion' entered parameter is >0. No pixel values computation.")
                else:
                    pixel = np.array([0,0])
                    importance = 0
                    if(message):
                        print("WARNING : Wrong object format for 'focused_pixel'! Must be a one dimensional ndarray, list or tuple of two coordinates on the considered image. No pixel values computation.")
                
                image_mean = image_calculator.calculate_image_mean(image) * (1-importance) + image[pixel[0],pixel[1]] * importance
                
                if((type(color_values) is str and color_values=='inverted_mean_proportion') or color_values is None):
                    original = float(1.0-image_mean/255)
                elif(type(color_values) is float or type(color_values) is int):
                    original = float(color_values)
                elif(type(color_values) is list or type(color_values) is np.ndarray or type(color_values) is tuple):
                    original = float(np.mean(color_values))
                    if(message):
                        print("WARNING : Current image is monocolor (2D) and 'color_values' type is list or ndarray. Returned contrasted 'color_values' float value had been put to the average of all the 'color_values' array values.")
                else:
                    original = float(1.0-image_mean/255)
                    if(message):
                        print("WARNING : Wrong object format for 'color_values'! Must be a float/int if image is not colorised (2D), or a list/ndarray of 3 floats if colorised (3D). Image here is 2D. Value of inverted_mean_proportion single float returned.")
                
                if(original<0.0):
                    original = 0.0
                elif(original>1.0):
                    original = 1.0
                
                if(original<=image_mean/255):
                    contrasted = original**main_contrast_exponent
                else:
                    contrasted = 1-(1-original)**main_contrast_exponent
                if(contrasted<0.0):
                    contrasted = 0.0
                elif(contrasted>1.0):
                    contrasted = 1.0
                
                return contrasted
            
            elif(number_of_dimensions==3):
                
                if((type(focused_pixel) is list or type(focused_pixel) is np.ndarray or type(focused_pixel) is tuple) and np.shape(np.shape(focused_pixel))[0]==1 and np.shape(focused_pixel)[0]>=2):
                    pixel = np.array([focused_pixel[0],focused_pixel[1]])
                    importance = pixel_importance_proportion
                    if(np.shape(focused_pixel)[0]>2 and message):
                        print("WARNING : Entered 'focused_pixel' parameter contains more than two coordinates. Only the first two have been considered to build focused pixel.")
                elif(focused_pixel is None):
                    pixel = np.array([0,0])
                    importance = 0
                    if(pixel_importance_proportion>0 and message):
                        print("WARNING : No 'focused_pixel' parameter entered, but 'pixel_importance_proportion' entered parameter is >0. No pixel values computation.")
                else:
                    pixel = np.array([0,0])
                    importance = 0
                    if(message):
                        print("WARNING : Wrong object format for 'focused_pixel'! Must be a one dimensional ndarray, list or tuple of two coordinates on the considered image. No pixel values computation.")
                
                based_image_mean = image_calculator.calculate_image_mean(image)
                based_focused_pixel = image[pixel[0],pixel[1]]
                image_mean = np.array([based_image_mean[0]*(1-importance)+based_focused_pixel[0]*importance, based_image_mean[1]*(1-importance)+based_focused_pixel[1]*importance, based_image_mean[2]*(1-importance)+based_focused_pixel[2]*importance])
                
                if((type(color_values) is str and color_values=='inverted_mean_proportion') or color_values is None):
                    originals = [float(1.0-image_mean[0]/255), float(1.0-image_mean[1]/255), float(1.0-image_mean[2]/255)]
                elif((type(color_values) is list or type(color_values) is np.ndarray or type(color_values) is tuple) and np.shape(np.shape(color_values))[0]==1 and np.shape(color_values)[0]>=3):
                    originals = [float(color_values[0]), float(color_values[1]), float(color_values[2])]
                elif(type(color_values) is float or type(color_values) is int):
                    originals = [float(color_values), float(color_values), float(color_values)]
                    if(message):
                        print("WARNING : Current image is tricolor (3D) and 'color_values' type is float or int. Returned contrasted 'color_values' ndarray of three floats had been put to a ndarray with three of the 'color_values' float value.")
                else:
                    originals = [float(1.0-image_mean[0]/255), float(1.0-image_mean[1]/255), float(1.0-image_mean[2]/255)]
                    if(message):
                        print("WARNING : Wrong object format for 'color_values'! Must be a float/int if image is not colorised (2D), or a list/ndarray of 3 floats if colorised (3D). Image here is 3D. Values of inverted_mean_proportion ndarray returned.")
                
                original_a_idx = np.argmin(originals)
                original_c_idx = np.argmax(originals)
                if(original_a_idx!=0 and original_c_idx!=0):
                    original_b_idx = 0
                elif(original_a_idx!=1 and original_c_idx!=1):
                    original_b_idx = 1
                else:
                    original_b_idx = 2
                
                original_a = originals[original_a_idx]
                original_b = originals[original_b_idx]
                original_c = originals[original_c_idx]
                
                if(np.abs(original_c-original_a)<=0.000001):
                    original_1 = original_a
                    original_2 = original_b
                    original_3 = original_c
                else:
                    original_mean = (original_a + original_b + original_c)/3
                    
                    original_a_p = ( 2*original_mean - 4*original_a )*color_contrast_proportion**2 + ( 4*original_a - 3*original_mean )*color_contrast_proportion + original_mean
                    original_c_p = ( 2*original_mean - 4*original_c + 2 )*color_contrast_proportion**2 + ( 4*original_c - 3*original_mean - 1 )*color_contrast_proportion + original_mean
                    original_b_p = ( (original_b-original_a)*original_c_p - (original_b-original_c)*original_a_p )/( original_c - original_a )
                    
                    if(original_a_idx==0):
                        original_1 = original_a_p
                        if(original_b_idx==1):
                            original_2 = original_b_p
                            original_3 = original_c_p
                        else:
                            original_3 = original_b_p
                            original_2 = original_c_p
                    elif(original_a_idx==1):
                        original_2 = original_a_p
                        if(original_b_idx==0):
                            original_1 = original_b_p
                            original_3 = original_c_p
                        else:
                            original_3 = original_b_p
                            original_1 = original_c_p
                    else:
                        original_3 = original_a_p
                        if(original_b_idx==0):
                            original_1 = original_b_p
                            original_2 = original_c_p
                        else:
                            original_2 = original_b_p
                            original_1 = original_c_p
                
                if(original_1<0.0):
                    original_1 = 0.0
                elif(original_1>1.0):
                    original_1 = 1.0
                if(original_2<0.0):
                    original_2 = 0.0
                elif(original_2>1.0):
                    original_2 = 1.0
                if(original_3<0.0):
                    original_3 = 0.0
                elif(original_3>1.0):
                    original_3 = 1.0
                
                if(original_1<=image_mean[0]/255):
                    contrasted_1 = original_1**main_contrast_exponent
                else:
                    contrasted_1 = 1-(1-original_1)**main_contrast_exponent
                if(contrasted_1<0.0):
                    contrasted_1 = 0.0
                elif(contrasted_1>1.0):
                    contrasted_1 = 1.0
                
                if(original_2<=image_mean[1]/255):
                    contrasted_2 = original_2**main_contrast_exponent
                else:
                    contrasted_2 = 1-(1-original_2)**main_contrast_exponent
                if(contrasted_2<0.0):
                    contrasted_2 = 0.0
                elif(contrasted_2>1.0):
                    contrasted_2 = 1.0
                
                if(original_3<=image_mean[2]/255):
                    contrasted_3 = original_3**main_contrast_exponent
                else:
                    contrasted_3 = 1-(1-original_3)**main_contrast_exponent
                if(contrasted_3<0.0):
                    contrasted_3 = 0.0
                elif(contrasted_3>1.0):
                    contrasted_3 = 1.0
                
                return np.array([contrasted_1,contrasted_2,contrasted_3])
            
            else:
                print("ERROR :",number_of_dimensions,"dimensional image can't be processed! 1.0 returned.")
                return 1.0
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". 1.0 returned.")
            return 1.0
    
    # To convert a 2D image to its 3D one
    def from_2D_to_3D_image(image):
        if(type(image) is np.ndarray):
            if(np.shape(np.shape(image))[0]==2):
                height,width = np.shape(image)[:2]
                new_image = np.empty([height,width,3], dtype='int32')
                for i in range(height):
                    for j in range(width):
                        new_image[i,j] = [int(image[i,j]),int(image[i,j]),int(image[i,j])]
                return new_image
            else:
                print("ERROR :",np.shape(np.shape(image))[0],"dimensional image can't be processed! Must be 2D. Original image returned.")
                return image
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Original image returned.")
            return image
    
    # To convert a 3D image to its 2D one
    def from_3D_to_2D_image(image):
        if(type(image) is np.ndarray):
            if(np.shape(np.shape(image))[0]==3):
                if(np.shape(image)[2]==3):
                    height,width = np.shape(image)[:2]
                    new_image = np.empty([height,width], dtype='int32')
                    for i in range(height):
                        for j in range(width):
                            new_image[i,j] = int((image[i,j,0]+image[i,j,1]+image[i,j,2])/3)
                    return new_image
                else:
                    print("ERROR : There are",np.shape(image)[2],"arguments in the third dimension of image! There must be exactly 3. Original image returned.")
                    return image
            else:
                print("ERROR :",np.shape(np.shape(image))[0],"dimensional image can't be processed! Must be 3D. Original image returned.")
                return image
        else:
            print("ERROR : Image must be a ndarray! Current image type:",type(image),". Original image returned.")
            return image
    
