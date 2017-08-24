import io
import os
import socket
import struct
import cv2
import time
import numpy as np
import pygame
from PIL import Image
from pygameControl import CV2PYGAME, RCControl

server_socket = socket.socket()

#data collected from stream and pygame controls will be save to:
train_data = []
file_name = 'training_ether_final.npy'
if os.path.isfile(file_name):
    print("file exists, opening file...")
    train_data = list(np.load(file_name))
else: print("file does not exists, create new")

#pygame object to directly control the car
pygameControl = RCControl()

#The image contains a lot of redundant info. So we are going to filter through it
#and find what we really need
##def processImage(img):
##    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##    return img[140:,:]
def startListening():
    server_socket.bind(('0.0.0.0', 6116))
    server_socket.listen(0)
    connection = server_socket.accept()[0].makefile('rb')
    command_key = 6
    startGatheringData = False # can be use as a pause
    try:
        count = 0
        clock = pygame.time.Clock()
        while(True):
            #start = time.time()
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

            #if the client sends image len of 0, exit
            if ((pygameControl.QUIT) | (not image_len) | (cv2.waitKey(5) & 0xFF == 'q') ):
                #stop RC car and exit after 100 data points or the streaming stop
                pygameControl.simpleControl(6)
                pygameControl.quit()
                cv2.destroyAllWindows()
                break
            
            #convert back into image
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            image_stream.seek(0)

            data = np.fromstring(image_stream.getvalue(), dtype = np.uint8)
            image = cv2.imdecode(data,1)
            #The original image is just too big to store, and i don't feel like the neuronet need such a large pixel image to detect features
            gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            imageResized = cv2.resize(gray, (480,360))

            pygameControl.setScreen(CV2PYGAME(cv2.flip(image, 1)))
            #getKeys() return True if there are changes in the pressed arrow
            if(pygameControl.getKeys()):
                command_key = pygameControl.getCommand()
                pygameControl.simpleControl(command_key) #.001s
                #if there are charnges, signal start gathering data

            #Pause the data collection process by pressing key 'p'
            #start the data collection process by pressing key 's'
            pressed = pygameControl.P()
            if(pressed[0]):
                print("pause gathering data")
                startGatheringData = False
            if(pressed[1]):
                print("start gathering data")
                startGatheringData = True         
            if(startGatheringData):
                count+=1
                train_data.append([imageResized, command_key])
                if(count%200 == 0):
                    print("have collected {} data points".format(count))
                     
            clock.tick(60)            
            #end = time.time()
            #print("time per loop:",end-start)
    finally:
        connection.close()
        server_socket.close()
        
startListening()
np.save(file_name,train_data)
