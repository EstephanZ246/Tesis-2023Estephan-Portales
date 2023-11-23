
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
import json 
import requests

url = "https://ocr.asprise.com/api/v1/receipt"


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
    # PROTOTIPO PARA vectorizal la imagen


    #--------------------------------------
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
        COM_PORT = 0

# Para cerrar el puerto COM
def Desconectar_COM():
    global COM_PORT
    COM_PORT.close()
    COM_PORT = 0
    pass

def Mandar_Robot():
    global COM_PORT

    Cadena_datos = ""
    if (JA1 and JB1 and JB2 and JC1):

        Cadena_datos = "JA" + JA1 + "JB" + JB1 + "," + JB2 + "JC" + JC1 + ";"
        try:
            COM_PORT.write(Cadena_datos.encode())
            Recibido = COM_PORT.readline().decode()
            TempA = (Recibido[Recibido.index("JA")+2:Recibido.index("JB")])
            TempB = (Recibido[Recibido.index("JB")+2:Recibido.index(",")])
            TempC = (Recibido[Recibido.index(",")+1:Recibido.index("JC")])
            TempD = (Recibido[Recibido.index("JC")+2:Recibido.index(";")])
            
            if ((float(TempA) == float(JA1))and(float(TempB) == float(JB1))and(float(TempC) == float(JB2))and(float(TempD) == float(JC1))):
                print("Transmisión Exitosa")
            else:
                print("Error en la transmisión de datos")


        except Exception as error:
            print(error)  

    else:
        print("No se tienen los datos completos")
    
     

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
        Label_Joint1_Value['text'] = (JA1 + "°")
    
    if  datos[1]:
        JB1 = datos[1]
        #print(datos[1])
        Label_Joint2_Value['text'] = (JB1 + "°")

    
    if datos[2]:
        JB2 = datos[2]
        #print(datos[2])
        Label_Joint2_1_Value['text'] = (JB2 + "mm")
    

    if  datos[3]:
        JC1 = datos[3]
        #print(datos[3])
        Label_Joint3_Value['text'] = (JC1 + "°")
    

def desconectar_TCP():
    global clienteTCPIP
    ClientSocket.desconectar_server(clienteTCPIP)
    

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
    denoised_image = cv2.GaussianBlur(blurred_image, (3, 3), 0)
    cv2.imwrite("AnguloJoint1.jpg",denoised_image)

    res = requests.post(url,data = {'api_k':'TEST','recognizer':'auto','ref_no':'oct_python_123'},
                    files = {'file': open("AnguloJoint1.jpg",'rb')})
    with open("response1.json","w") as f:
        json.dump(json.loads(res.text),f)
    with open("response1.json","r") as f:
        data = json.load(f)
    Texto_joint = float(data['receipts'][0]['ocr_text'])
    
    return Texto_joint
