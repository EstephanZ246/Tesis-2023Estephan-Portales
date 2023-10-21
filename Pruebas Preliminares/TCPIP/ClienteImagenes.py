import socket
import numpy as np
import cv2
import time
import datetime
import base64
import sys

class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0
        self.connectServer()

    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print('Client socket is connected with Server socket [ TCP_SERVER_IP: {}, TCP_SERVER_PORT: {} ]'.format(self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            self.connectCount = 0
            self.sendImages()
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print('Connect fail {} times. Exiting program'.format(self.connectCount))
                sys.exit()
            print('{} times try to connect with server'.format(self.connectCount))
            self.connectServer()

    def sendImages(self):
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 315)
        try:
            while capture.isOpened():
                ret, frame = capture.read()
                resize_frame = cv2.resize(frame, dsize=(480, 315), interpolation=cv2.INTER_AREA)
                now = time.localtime()
                stime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
                result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
                data = np.array(imgencode)
                stringData = base64.b64encode(data)
                print(stringData)
                length = str(len(stringData))
                self.sock.sendall(length.encode('utf-8').ljust(64))
                self.sock.send(stringData)
                self.sock.send(stime.encode('utf-8').ljust(64))
                print('Send images')
                time.sleep(0.095)
        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

def main():
    TCP_IP = 'localhost'
    TCP_PORT = 8080
    client = ClientSocket(TCP_IP, TCP_PORT)

if __name__ == "__main__":
    main()