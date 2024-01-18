import socket
import cv2 as cv
import numpy as np
import time
from camera_detection import VisionProcessing
import os

jointCommand1 = np.array([33,33,3], dtype=np.uint16)
jointCommand2 = np.array([55,55,0], dtype=np.uint16)
jointCommand3 = np.array([66,66,0], dtype=np.uint16)
jointInfo1 = []
jointInfo2 = []
jointInfo3 = []


def cameraFeed(socket):
    packet = b''
    while (len(packet) < 1228800):
        partByte = socket.recv(1228800 - len(packet))
        if(partByte != b''):
            packet += bytearray(partByte)
        else:
            print("negative")
            break

    if(len(packet) > 1228800):
        packet = b''    
    elif(len(packet) == 1228800):
        array = np.frombuffer(packet, dtype=np.uint8)
        numpy_array = np.reshape(array, (480, 640, 4))
        rgbImage = cv.cvtColor(numpy_array, cv.COLOR_RGBA2BGR)

        return rgbImage

def jointSend(jointOne, jointTwo, jointThree, socketSelected):
  if (socketSelected.recv(1)).decode() == "1":
    size1 = bytes([len(bytearray(jointOne))])
    socketSelected.send(size1)
    if (socketSelected.recv(1)).decode() == "R":
      socketSelected.sendall(bytearray(jointOne))
  if (socketSelected.recv(1)).decode() == "2":
    size2 = bytes([len(bytearray(jointTwo))])
    socketSelected.send(size2)
    if (socketSelected.recv(1)).decode() == "R":
      socketSelected.sendall(bytearray(jointTwo))
  if (socketSelected.recv(1)).decode() == "3":
    size3 = bytes([len(bytearray(jointThree))])
    socketSelected.send(size3)
    if (socketSelected.recv(1)).decode() == "R":
      socketSelected.sendall(bytearray(jointThree))

def jointFeed(socket):
    totalArray = []
    for i in range(1, 4):
        socket.send(str(i).encode())
        packet = b''
        byt = socket.recv(1024)
        totalSize = int.from_bytes(byt, byteorder='big')
        socket.send("R".encode())
        while (len(packet) < totalSize):
            partByte = socket.recv(totalSize - len(packet))
            if(partByte != b''):
                packet += bytearray(partByte)
            else:
                print("negative")
                break
        if(len(packet) > totalSize):
            packet = b''    
        elif(len(packet) == totalSize):
            array = np.frombuffer(packet, dtype=np.uint16)
            totalArray.append(list(array))
    return totalArray

def printJointInfo():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Joint 1:", end =" ")
        print(jointInfo1, end =" ")
        print("Joint 2:", end =" ")
        print(jointInfo1, end =" ")
        print("Joint 3:", end =" ")
        print(jointInfo1)
   

ROBOTHOSTNAME = "snake.local"
connection = False

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cameraPort = 12345
receivePort = 12346
sendPort = 12347  


Address = ROBOTHOSTNAME
while connection == False:
    try:
        s.connect((Address, cameraPort))
        print("Camera connected")
        s.send("Start".encode())

        s2.connect((Address, receivePort))
        print("Receive connected")

        s3.connect((Address, sendPort))
        print("Send connected")

        connection = True
        print("connected")
    except:
        print("Snake is not availble")
        print("Enter IP or hostname to try again")
        Address = input("IP or Hostname:")
        connection = False
   

while(connection == True):
        frame = cameraFeed(s)
        dataReceived = jointFeed(s3)
        jointSend(jointCommand1, jointCommand2, jointCommand3, s2)
        jointInfo1 = dataReceived[0]
        jointInfo2 = dataReceived[1]
        jointInfo3 = dataReceived[2]
        printJointInfo()
        jointCommand1[0] += 1
        jointCommand2[0] += 1
        jointCommand3[0] += 1

        vp = VisionProcessing()
        vp.camera_processing(frame)
        cv.imshow("capture", frame)
        if cv.waitKey(25) & 0xFF == ord('q'):
            # s.close()
            cv.destroyAllWindows()
            # break