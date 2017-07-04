"""
capture stream video images as well as the input images and send it over the network
the input data is then recieved by the laptop     
"""
#I need a way to record the photo and the distance at the same time
#a photo can be reshape into a matrix of tuple
import time
import socket
import struct
import datetime
import io
import RPi.GPIO as GPIO
import picamera.PiCamera

#pins for the distance sensors
TRIG1 = 4
ECHO1 = 18
#set up camera and GPIO pins
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 24
camera.start_preview() #warm up
time.sleep(2)

GPIO.setMode(GPIO.BCM)
GPIO.setup(TRIG1, GPIO.OUT)
GPIO.setup(ECHO1, GPIO.IN)


def getDistance1():
    #gather inputs from GPIO
    GPIO.output(TRIG1,True)
    time.sleep(0.00001)
    GPIO.output(TRIG1,False)
    while GPIO.input(ECHO1) == False:
        start = time.time()
    while(GPIO.input(ECHO1) == True):
        end = time.time()
    distance = (end-start)/.000058
    return distance

def sendInputs():
    #prepare the client socket
    client_socket = socket.socket()
    client_socket.connect(('192.168.2.9', 6116))
    connection = client_socket.makefile('wb')
    try:
        start = time.time()
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, 'jpeg'):
            connection.write(struct.pack('<L', stream.tell(),distance))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            #connection.write(str(datetime.datetime.now()))
            #connection.write(getDistance1())
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
        #Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:
        connection.close()
        client_socket.close()
def readInputs():    
    while(True):
        #inputs from the GPIO sensor
        GPIO.output(TRIG1,True)
        time.sleep(0.00001)
        GPIO.output(TRIG1,False)
        while GPIO.input(ECHO1) == False:
            start = time.time()
        while(GPIO.input(ECHO1) == True):
            end = time.time()

        distance = (end-start)/.000058 #in cm

        #input image from picamera
        time = str(datetime.datetime.now());
        camera.capture        
        
def main():
    pass
if __name__ == '__main__':
    main()

