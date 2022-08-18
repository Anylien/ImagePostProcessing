#  08/28/2019
#
#  imageTools.py
#
#  Bastien HARMAND <bastien.harmand@mines-ales.org>
#
#  This file contains elementary tools to manage simple operations on images.

from configparser import SafeConfigParser
import numpy as np
import cv2

''' GENERAL PARAMETERS '''
params = SafeConfigParser()
params.read('setup.ini')

# Colors for each layer of the overview
color_master = [float(params.get('MasterColorDisplay','B')),float(params.get('MasterColorDisplay','G')),float(params.get('MasterColorDisplay','R'))]
color_slave1 = [float(params.get('Slave1ColorDisplay','B')),float(params.get('Slave1ColorDisplay','G')),float(params.get('Slave1ColorDisplay','R'))]
color_slave2 = [float(params.get('Slave2ColorDisplay','B')),float(params.get('Slave2ColorDisplay','G')),float(params.get('Slave2ColorDisplay','R'))]

def replace_color(image,value_to_replace,new_value) : # Replace a value in a greyscale image
    image[image==value_to_replace] = new_value

def MSE(master,slave) : # Return the sum of the squared difference between two images (images must be the same size)
    return np.sum((master-slave)**2)

def apply_transform(image,tx,ty,targetHeight,targetWidth) : # Apply an affine transformation to an image
    M = np.float32([[1,0,tx],[0,1,ty]])
    img_out = cv2.warpAffine(image,M,(targetHeight,targetWidth),borderMode=cv2.BORDER_REPLICATE)
    return img_out

def structural_error(master,slave,horizontal, vertical) : # Return two structural contour images
    width,height = np.shape(master)
    slave_contour = cv2.Canny(slave,80,220)
    master_contour = cv2.Canny(master,80,220)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) # Morphologic operation to smooth the contours :
    N = 3
    slave_relief = (1/(N+1))*(cv2.dilate(slave_contour/255, kernel, iterations=0))
    master_relief = (1/(N+1))*(cv2.dilate(master_contour/255, kernel, iterations=0))
    for k in range(N) :
        slave_relief += 0.5*(1/(N+1))*cv2.dilate(slave_contour/255, kernel, iterations=k+1)
        master_relief += 0.5*(1/(N+1))*cv2.dilate(master_contour/255, kernel, iterations=k+1)
    slave_relief = apply_transform(slave_relief,0,0,height,width) # (to make the two images the same size)
    width,height = np.shape(master_relief) 
    master_relief_faded = master_relief.copy()
    return master_relief,slave_relief

def compare_img(master,slave1,slave2,background = [0,0,0]) :  # Return an overlapped image with custom colors for each layer (master, slave1 and slave2 (optionnal)) displayed as Canny edges
    width,height = np.shape(master)
    comparaison = np.zeros((width,height,3), np.uint8)
    master_relief,slave_relief1 = cv2.Canny(master,80,220),cv2.Canny(slave1,80,220)
    comparaison[:,:,0] += ((master_relief)*float(color_master[0])).astype(np.uint8) # Blue Canal Master
    comparaison[:,:,1] += ((master_relief)*float(color_master[1])).astype(np.uint8) # Red Canal Master
    comparaison[:,:,2] += ((master_relief)*float(color_master[2])).astype(np.uint8) # Green Canal Master
    comparaison[:,:,0] += ((slave_relief1)*float(color_slave1[0])).astype(np.uint8) # Blue Canal Slave1
    comparaison[:,:,1] += ((slave_relief1)*float(color_slave1[1])).astype(np.uint8) # Red Canal Slave1
    comparaison[:,:,2] += ((slave_relief1)*float(color_slave1[2])).astype(np.uint8) # Green Canal Slave1
    slave_relief2 = cv2.Canny(slave2,80,220)
    comparaison[:,:,0] += ((slave_relief2)*float(color_slave2[0])).astype(np.uint8) # Blue Canal Slave2
    comparaison[:,:,1] += ((slave_relief2)*float(color_slave2[1])).astype(np.uint8) # Red Canal Slave2
    comparaison[:,:,2] += ((slave_relief2)*float(color_slave2[2])).astype(np.uint8) # green Canal Slave2
    comparaison[(comparaison[:,:,0]==0)*(comparaison[:,:,1]==0)*(comparaison[:,:,2]==0)] = background
    return comparaison.astype(master.dtype)
