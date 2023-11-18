
import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
import pyautogui
from PIL import ImageTk, Image
import PIL.Image
import time
import serial.tools.list_ports
import cv2
import numpy as np
import pytesseract


Captura = ""
JA1 = ""
JB1 = ""
JB2 = ""
JC1 = ""
COM_PORT = ""
imagencapturada = 0


# Funcion para esconder ventana
def HideWindow(window):
    window.withdraw()

# Funcion para reaparecer ventana
def ShowWindow(window):
    window.deiconify()

# Tomar screenshot
def TakeScreenshot(window,image_label):

    x0 = 532
    y0 = 190
    ancho = x0 + 859
    alto = y0 + 667

    global Captura
    global imagencapturada

    HideWindow(window)
    time.sleep(0.5)
    myscreen = pyautogui.screenshot()
    #myscreen.crop(box=None)
    image = myscreen.crop((x0,y0,ancho,alto))
    # PROTOTIPO PARA vectorizal la imagen


    #--------------------------------------
    image.save('myscreen.png')
    imagencapturada = image
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
    

def MandarCaptura(Label_Joint1_Value,Label_Joint2_Value,Label_Joint2_1_Value,Label_Joint3_Value):
    global JA1
    global JB1
    global JB2
    global JC1
    global Captura


    imagencapture = cv2.imread(Captura)

    # Primer recorte para reconocer el joint 
    AjuRecorJoint = [47,52,47+40,52+207] # x,y,ancho,alto
    Recorte_Joint = imagencapture[AjuRecorJoint[0]:AjuRecorJoint[2],AjuRecorJoint[1]:AjuRecorJoint[3]]
    cv2.imwrite("Joint Recibido.jpg",Recorte_Joint)

    # Reconocer el Joint (La linea de abajo solo es en windows)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    Texto_joint = pytesseract.image_to_string(Recorte_Joint, config=f'--psm 6')

    if Texto_joint.find('1') >= 0:
        # Se procesan los ángulos y se mandan de regreso
                    
        AjuRecorAng = [293,611,293+38,611+46] # x,y,ancho,alto
        Recorte_Ang = imagencapture[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
        Texto = Process_number(Recorte_Ang)
        cv2.imwrite('JointPrueba.jpg',Recorte_Ang)
        JA1 = str(Texto)
        Label_Joint1_Value['text'] = (JA1 + "°")
                    
    elif Texto_joint.find('2') >= 0:
        # Se procesan los ángulos y se mandan de regreso

        AjuRecorAng = [171,365,171+28,365+28] # x,y,ancho,alto
        Recorte_Ang = imagencapture[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
        Texto1 = Process_number(Recorte_Ang)
        JB1 = str(Texto1)
        Label_Joint2_Value['text'] = (JB1 + "°")    

        #Procesamiento del segundo dato de la junta 2
        AjuRecorAng = [87,373,87+28,373+28] # x,y,ancho,alto
        Recorte_Ang = imagencapture[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
        Texto2 = Process_number(Recorte_Ang) 
        JB2 = str(Texto2)
        Label_Joint2_1_Value['text'] = (JB2 + "mm")      
      
    elif Texto_joint.find('3') >= 0:

        # Se procesan los ángulos y se mandan de regreso
        AjuRecorAng = [168,372,168+28,372+28] # x,y,ancho,alto
        Recorte_Ang = imagencapture[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
        cv2.imwrite("AnguloJoint3.jpg",Recorte_Ang)
        Texto = Process_number(Recorte_Ang)
        JC1 = str(Texto)
        Label_Joint3_Value['text'] = (JC1 + "°")
    

def Process_number(image):

    #image = cv2.imread(image_path)

    scale_percent = 2000 
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_CUBIC)
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Gaussian denoising
    denoised_image = cv2.GaussianBlur(blurred_image, (3, 3), 0)
    cv2.imwrite("AnguloJoint1.jpg",denoised_image)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    whitelist = '0123456789.°-+'
    Texto_joint = pytesseract.image_to_string(denoised_image, config=f'--psm 6 -c tessedit_char_whitelist={whitelist}')
    Texto_joint = float(Texto_joint)
    
    return Texto_joint
