# Aquí se tienen muchas de las funciones que se usan directamente con la GUI, pero tiene conexiones también con cliente y servidor.
# prácticamente desde aquí se llama a todas las funciones auxiliares que se requiere y también se tienen las más básicas usadas en la GUI
# por ejemplo hacer screenshots, hacer la funcion de esconder la pantalla al momento de tomar screenshot (Lo pueden comprobar al usar la GUI)


import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import pyautogui
from PIL import ImageTk, Image
import PIL.Image
import time
import serial.tools.list_ports
from cliente import *
import cv2
import numpy as np
import pytesseract


# Estas variables son globales, se guardan algunos datos que se usan en más de una función de la GUI, lo encontré práctico, sin embargo, se puede mejorar usando alguna clase
clienteTCPIP = 0
Captura = ""
JA1 = ""
JB1 = ""
JB2 = ""
JC1 = ""
COM_PORT = ""


# Funcion para esconder ventana
def HideWindow(window):
    window.withdraw()

# Funcion para reaparecer ventana
def ShowWindow(window):
    window.deiconify()

# Tomar screenshot
def TakeScreenshot(window,image_label):

    x0 = 703
    y0 = 351
    ancho = x0 + 521
    alto = y0 + 403

    global Captura

    HideWindow(window)
    time.sleep(0.5)
    myscreen = pyautogui.screenshot()
    #myscreen.crop(box=None)

    image = myscreen.crop((x0,y0,ancho,alto))
    image.save('myscreen.png')
    time.sleep(0.5)
    ShowWindow(window)

    

    fp = open("myscreen.png","rb")
    image = PIL.Image.open(fp)
    
    Captura = "myscreen.png"
    new_size = (300, 200)  # Specify the desired dimensions (width, height)
    resized_image = image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    image_label.configure(image=photo)
    image_label.image = photo
    

# Search COM Ports
def Search_COMPorts(combobox):
    puertos = serial.tools.list_ports.comports()
    combobox['values'] = puertos


# Conectar a puerto COM
def Conectar_COM(Puerto_COM):
    global COM_PORT

    baudrate = 115200
    COM = Puerto_COM[0:Puerto_COM.find('-')-1]

    try:
        COM_PORT = serial.Serial(COM,115200)
    except:
        print("No se pudo conectar al puerto Serial")

# Esta función es la que mandará la estructura de datos hacia el sistema robótico
def Mandar_Robot():
    global COM_PORT
    JA1 = ""
    JB1 = ""
    JB2 = ""
    JC1 = ""
    Cadena_datos = ""
    if (JA1 and JB1 and JB2 and JC1):
        Cadena_datos = "JA" + JA1 + "JB" + JB1 + "," + JB2 + "JC" + JC1
    pass
    
    

# Conectar con servidor TCP/IP
def ConectarTCPIP(IP,Puerto):
    global clienteTCPIP
    
    try:
        DIP = IP.get()
        DPort = int(Puerto.get())

        Cliente = ClientSocket(DIP,DPort)
        clienteTCPIP = Cliente

    except:

        pass

# Esta se encarga de mandar mandar la captura de pantalla y al recibir los datos, se colocan en los labels que tiene la GUI.
# Aquí pueden ver que se hace uso de las variables globales, porque cuando se mandan los datos al robot, se van a usar nuevamente.
def MandarCaptura(Label_Joint1_Value,Label_Joint2_Value,Label_Joint2_1_Value,Label_Joint3_Value):
    global JA1
    global JB1
    global JB2
    global JC1

    global clienteTCPIP
    global Captura
    datos = ClientSocket.sendImages(clienteTCPIP,Captura)
    if datos[0]:
        JA1 = datos[0]
        #print(datos[0])
        Label_Joint1_Value['text'] = (JA1)
    
    if  datos[1]:
        JB1 = datos[1]
        #print(datos[1])
        Label_Joint2_Value['text'] = (JB1)

    
    if datos[2]:
        JB2 = datos[2]
        #print(datos[2])
        Label_Joint2_1_Value['text'] = (JB2)
    

    if  datos[3]:
        JC1 = datos[3]
        #print(datos[3])
        Label_Joint3_Value['text'] = (JC1)
    

# Esta sirve para desconectar manualmente del servidor, con el botón "desconectar" en la GUI
def desconectar_TCP():
    global clienteTCPIP
    ClientSocket.desconectar_server(clienteTCPIP)
    
# Esta función es usada por el servidor para poder procesar la imagen, el prototipo se encuentra en la carpeta de pruebas independientes de programaciones
def Process_number(image):

    #image = cv2.imread(image_path)

    scale_percent = 2000 
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Gaussian denoising
    denoised_image = cv2.GaussianBlur(blurred_image, (5, 5), 0)
    
    #kernel = np.ones((3, 3), np.uint8)
    #cleaned_image = cv2.morphologyEx(gray_image, cv2.MORPH_CLOSE, kernel)

    #threshold_value = 113
    #_, thresholded_image = cv2.threshold(gray_image, threshold_value, 255, cv2.THRESH_BINARY)
    #inverted_image = cv2.bitwise_not(thresholded_image)
    cv2.imwrite("AnguloJoint1.jpg",denoised_image)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    whitelist = '0123456789.°-+'
    Texto_joint = pytesseract.image_to_string(denoised_image, config=f'--psm 6 -c tessedit_char_whitelist={whitelist}')
    Texto_joint = float(Texto_joint)
    
    return Texto_joint
