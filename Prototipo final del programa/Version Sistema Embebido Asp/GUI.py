import tkinter as tk
from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
import PIL.Image
from Fuctions import *

def Crear_Interfaz():
    window =ThemedTk(theme="arc")# tk.Tk()
    window.geometry("800x500")
    window.maxsize(800,500)
    window.minsize(800,500)

    Titulo = tk.Label(window, text = "Ángulo Configuración",font = ('Times 25'))
    Titulo.pack()

    Boton_Buscar_Puertos = tk.Button(window,text ="Buscar Puertos",font=("Arial",12), command= lambda: Search_COMPorts(Combo_ports))
    Boton_Buscar_Puertos.place(x=10,y=70)

    Combo_ports = ttk.Combobox(width=12,height=20,font=("Arial",14))
    Combo_ports.place(x=150,y=71)

    Label_Puerto = tk.Label(window, text = "Puerto: ",font = ('Times 9'),width=7)
    Label_Puerto.place(x= 10,y=110)

    Entry_Puerto = tk.Entry(window, text = "8080",font = ('Times 9'),width=7,bg='white')
    Entry_Puerto.place(x= 60,y=110)
    Entry_Puerto.insert(0, "8080")

    Label_IP = tk.Label(window, text = " Dirección IP: ",font = ('Times 9'),width= 9)
    Label_IP.place(x= 120,y=110)

    Entry_IP = tk.Entry(window, text = "127.0.0.1",font = ('Times 9'),width=14,bg='white')
    Entry_IP.place(x= 200,y=110)
    Entry_IP.insert(0, "127.0.0.1")

    #Boton_Verif_conexion = tk.Button(window,text ="Verificar Conexion",font=("Arial",10))
    #Boton_Verif_conexion.place(x=10,y=140)

    Boton_Conectar = tk.Button(window,text ="Conectar",font=("Arial",10), command= lambda: ConectarTCPIP(Entry_IP,Entry_Puerto))
    Boton_Conectar.place(x=20,y=140)

    Boton_Desconectar = tk.Button(window,text ="Desconectar",font=("Arial",10),command=desconectar_TCP)#, command=desconectar_TCP
    Boton_Desconectar.place(x=90,y=140)

#    """

    fp = open("WhiteScreen.jpg","rb")
    image = PIL.Image.open(fp)
    #image = Image.open("Foto2.jpg")
    new_size = (300, 200)  # Specify the desired dimensions (width, height)
    resized_image = image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(window, image=photo)
    image_label.place(x=30,y= 180)
#"""
    
    Boton_HacerScreen = tk.Button(window,text ="Hacer Screen",font=("Arial",10),command= lambda : TakeScreenshot(window,image_label))
    Boton_HacerScreen.place(x=30,y=400)

    #Boton_EditarImag = tk.Button(window,text ="Editar Imagen",font=("Arial",10))
    #Boton_EditarImag.place(x=130,y=400)

    Boton_Procesar = tk.Button(window,text ="Procesar Imagen",font=("Arial",10), command= lambda: MandarCaptura(Label_Joint1_Value,Label_Joint2_Value,Label_Joint2_1_Value,Label_Joint3_Value))
    Boton_Procesar.place(x=230,y=400)

    Label_AngulosConf = tk.Label(window, text = "Ángulos de Configuración",font = ('Times 25'))
    Label_AngulosConf.place(x= 400,y=71)

    Label_Joint1 = tk.Label(window, text = "Joint 1= ",font = ('Times 20'))
    Label_Joint1.place(x= 400,y=150)

    Label_Joint2 = tk.Label(window, text = "Joint 2= ",font = ('Times 20'))
    Label_Joint2.place(x= 400,y=200)

    Label_Joint3 = tk.Label(window, text = "Joint 3= ",font = ('Times 20'))
    Label_Joint3.place(x= 400,y=250)

    Label_Joint1_Value = tk.Label(window, text = "",font = ('Times 20'))
    Label_Joint1_Value.place(x= 520,y=150)

    Label_Joint2_Value = tk.Label(window, text = "",font = ('Times 20'))
    Label_Joint2_Value.place(x= 520,y=200)

    Label_Joint2_1_Value = tk.Label(window, text = "",font = ('Times 20'))
    Label_Joint2_1_Value.place(x= 600,y=200)

    Label_Joint3_Value = tk.Label(window, text = "",font = ('Times 20'))
    Label_Joint3_Value.place(x= 520,y=250)

    Boton_ConectarRobot = tk.Button(window,text ="Conectar Robot",font=("Arial",12),command= lambda : Conectar_COM(Combo_ports.get()))
    Boton_ConectarRobot.place(x=420,y=320)

    Boton_MandarRobot = tk.Button(window,text ="Mandar a Robot",font=("Arial",13), command = Mandar_Robot)
    Boton_MandarRobot.place(x=580,y=320)

    Boton_Salir = tk.Button(window,text ="Salir",font=("Arial",15),width=10)
    Boton_Salir.place(x=600,y=400)


    window.mainloop()

   
Crear_Interfaz()

