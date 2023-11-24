import socket
import numpy
import threading
import cv2
import time
import datetime
import base64
import pytesseract
import numpy as np
from Fuctions import *



class ServerSocket:

    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()

    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1) # Cuántos se pueden conectar a la red
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):

        try:
            while True:

                length = self.recvall(self.conn, 64)
                length = length.decode('utf-8')
                stringData = self.recvall(self.conn, int(length))
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
                decimg = cv2.imdecode(data, 1)
                cv2.imwrite("Captura Recibida.jpg",decimg)# Guardamos captura recibida

                # Primer recorte para reconocer el joint 
                AjuRecorJoint = [47,52,47+40,52+207] # x,y,ancho,alto
                Recorte_Joint = decimg[AjuRecorJoint[0]:AjuRecorJoint[2],AjuRecorJoint[1]:AjuRecorJoint[3]]
                cv2.imwrite("Joint Recibido.jpg",Recorte_Joint)

                # Reconocer el Joint (La linea de abajo solo es en windows)
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                Texto_joint = pytesseract.image_to_string(Recorte_Joint, config=f'--psm 6')

                #whitelist = '0123456789.°-+'
                #Texto_joint = pytesseract.image_to_string(Recorte_Joint, config=f'--psm 6 -c tessedit_char_whitelist={whitelist}')
                

                if Texto_joint.find('1') >= 0:
                    # Se procesan los ángulos y se mandan de regreso
                    
                    AjuRecorAng = [293,611,293+38,611+46] # x,y,ancho,alto
                    Recorte_Ang = decimg[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
                    Texto = Process_number(Recorte_Ang)
                    cv2.imwrite('JointPrueba.jpg',Recorte_Ang)
                    #print(Texto)
                    texto = "JA"+ str(Texto)
                    self.conn.send(texto.encode('utf-8').ljust(64))
                    
                elif Texto_joint.find('2') >= 0:
                    # Se procesan los ángulos y se mandan de regreso

                    AjuRecorAng = [171,365,171+28,365+28] # x,y,ancho,alto
                    Recorte_Ang = decimg[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
                    #cv2.imwrite("AnguloJoint2.jpg",Recorte_Ang)
                    Texto1 = Process_number(Recorte_Ang)

                    AjuRecorAng = [87,373,87+28,373+28] # x,y,ancho,alto
                    Recorte_Ang = decimg[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
                    #cv2.imwrite("AnguloJoint2_1.jpg",Recorte_Ang)
                    Texto2 = Process_number(Recorte_Ang)

                    print(Texto2)
                    texto = "JB"+ str(Texto2)+ ","+ str(Texto1)
                    self.conn.send(texto.encode('utf-8').ljust(64))
                    
      
                elif Texto_joint.find('3') >= 0:
                    # Se procesan los ángulos y se mandan de regreso

                    AjuRecorAng = [168,372,168+28,372+28] # x,y,ancho,alto
                    Recorte_Ang = decimg[AjuRecorAng[0]:AjuRecorAng[2],AjuRecorAng[1]:AjuRecorAng[3]]
                    cv2.imwrite("AnguloJoint3.jpg",Recorte_Ang)
                    Texto = Process_number(Recorte_Ang)

                    texto = "JC"+ str(Texto)
                    self.conn.send(texto.encode('utf-8').ljust(64))
                    
                  

        except Exception as e:

            print(e)
            self.socketClose()
            cv2.destroyAllWindows()
            self.socketOpen()
            self.receiveThread = threading.Thread(target=self.receiveImages)
            self.receiveThread.start()

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


def main():
    hostname=socket.gethostname()  
    IPAddr=socket.gethostbyname(hostname)  
    print(IPAddr)
    server = ServerSocket(IPAddr, 8080)

if __name__ == "__main__":
    main()

