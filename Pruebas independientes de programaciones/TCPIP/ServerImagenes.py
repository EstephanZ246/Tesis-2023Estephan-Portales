# En ente archivo se tiene el prototipo de servidor de un protocolo TCP/IP,
# Lo que hace es que cuando ya se conectó al cliente, recibe constantemente las imágenes y las coloca en pantalla.


import socket
import numpy
import threading
import cv2
import time
import datetime
import base64

# Esta es la clase que pertenece al servidos, se tiene métodos que abren el socket, lo cierran y recibe imágenes
class ServerSocket:


    def __init__(self, ip, port):
        # Se inicia el servidor y se coloca en un threading, esto para crear un hilo y no interfiera al momento de implementarlo y tener otros procesos
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()

    def socketClose(self):
        # Esta función cierra el socket
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        #Esta funcion se encarga de abrir el socket según la ip y puerto que se coloque en la función main de abajo
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1) # Cuántos se pueden conectar a la red
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):
            # Esta función recibe las imágenes y las muestra en pantalla, en la forma que se está usando es como que mandaramos un video en tiempo real.
        try:
            while True:
                length = self.recvall(self.conn, 64)
                length1 = length.decode('utf-8')
                stringData = self.recvall(self.conn, int(length1))
                stime = self.recvall(self.conn, 64)
                print('send time: ' + stime.decode('utf-8'))
                now = time.localtime()
                print('receive time: ' + datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f'))
                data = numpy.frombuffer(base64.b64decode(stringData), numpy.uint8)
                decimg = cv2.imdecode(data, 1)
                cv2.imshow("image", decimg)
                cv2.waitKey(1)

        except Exception as e:
            # En caso hay un error, se cierra el socket, se cierran las ventanas de las imágenes y se cierra el thread o hilo.
            print(e)
            self.socketClose()
            cv2.destroyAllWindows()
            self.socketOpen()
            self.receiveThread = threading.Thread(target=self.receiveImages)
            self.receiveThread.start()

    def recvall(self, sock, count):
        # Esta función es para recibir los datos 
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


def main():
    # Aquí inicializamos el servidor, en este caso está como localhost, esto quiere decir que el servidor será local
    server = ServerSocket('localhost', 8080)

if __name__ == "__main__":
    main()
