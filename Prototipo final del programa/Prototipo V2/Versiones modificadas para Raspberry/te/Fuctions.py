
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import pyautogui
from PIL import ImageTk, Image
import PIL.Image
import time
import cv2
import numpy as np
import pytesseract



clienteTCPIP = 0
Captura = ""
JA1 = ""
JB1 = ""
JB2 = ""
JC1 = ""
COM_PORT = ""

    

def Process_number(image):

    #image = cv2.imread(image_path)

    scale_percent = 350# 1500 funciona maomeno
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
    
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Gaussian denoising
    denoised_image = cv2.GaussianBlur(blurred_image, (3, 3), 0)
    
    cv2.imwrite("Anguloprocesado.jpg",denoised_image)
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    whitelist = '0123456789.°-+'
    Texto_joint = pytesseract.image_to_string(denoised_image, config=f'--psm 6 -c tessedit_char_whitelist={whitelist}')
    try:
        Texto_joint = float(Texto_joint)
        
    except Exception as error:
        print("No se pudo reconocer ángulo: ")
        print(error)
     
    
    return Texto_joint
