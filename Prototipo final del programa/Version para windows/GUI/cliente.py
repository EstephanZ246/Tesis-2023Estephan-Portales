# Esta programación es una clase creada para poder mandar las capturas de pantalla realizadas en la GUI
# A diferencia de la progra que está en "Pruebas Independiente de programacion/TCPIP", esta es usada en el documento Functions


import socket
import numpy
import cv2
import time
import datetime
import base64
import sys

datetime.datetime.utcnow()


class ClientSocket:
    # Funcion para inicializar la conexión con servidor según la ip y puerto que se ponga en la interfaz
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()
    # Conectar al servidor, en este caso si ocurre un problema, solo ya no intenta conectar hasta que se le oprime otra vez conectar en la GUI
    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
        except Exception as e:
            print(e)
    # Mandar la imágenes al servidor, en este caso son capturas de pantalla las que se enviarán
    def sendImages(self,imagen):

        try:
            # Agarrar Screenshot tomado antes, hacer un resize y codificar la foto para poder mandarla
            image = cv2.imread(imagen)
            resize_frame = cv2.resize(image,(image.shape[1],image.shape[0]),interpolation=cv2.INTER_AREA)
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
            result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
            data = numpy.array(imgencode)
            stringData = base64.b64encode(data)# Codificacion de la imagen
            length = str(len(stringData)) # Cantidad de datos que se van a mandar, se le manda antes al server para que sepa

            self.sock.sendall(length.encode('utf-8').ljust(64)) # Se manda cantidad de datos de la imagen
            self.sock.send(stringData) # Se manda la foto
        
            #self.sock.send(stime.encode('utf-8').ljust(64))
            
            Text_joints = (self.sock.recv(64)).decode('utf-8')
            
            # Lo que se hace aquí es que se manda la foto al servidor, este reconoce el texto y manda de regreso el número al cliente,
            # Según el Joint se recibe
            # 1. Joint1 "JAxx"
            # 2. Joint2 "JBxx,xx"  ----> la xx es el número, este puede ser negativo, positivo y con decimales. Del joint 2 se reciben 2 números, por eso la ",".
            # 3. Joint3 "JCxx"
        
        

            JA1 = ""
            JB1 = ""
            JB2 = ""
            JC1 = ""

            if Text_joints.find('JA') >= 0:
                JA1 = Text_joints[2:len(Text_joints)]
                
            if Text_joints.find('JB') >= 0:
                JB1 = Text_joints[2:Text_joints.find(",")]
                JB2 = Text_joints[Text_joints.find(",")+1:len(Text_joints)]

                pass

            if Text_joints.find('JC') >= 0:
                JC1 = Text_joints[2:len(Text_joints)]
 
                
            return JA1,JB1,JB2,JC1
            time.sleep(0.095)

            #self.sock.close()
            
        # En caso no se puede mandar las fotos, solo se reconecta al servidor y manda otra vez
        except Exception as e:

            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

    def desconectar_server(self):
        self.sock.close()



    
