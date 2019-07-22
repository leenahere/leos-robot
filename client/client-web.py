#!/usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from pynput import keyboard
from threading import Thread, Lock

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

'''
TODO:
check if the conection to server is failing
'''

# ip of Roboter
serverIp = '192.168.100.220'

# port to connect to
serverPort = 50007

# currently pressed Keys
pressedKeys = []

# Keys allowed to press
allowedKeys = ['a','w','s','d']

# array which will be sent
arrayToSend = [0,0,0,0]

# funktion to lock area before it is used from thread
lock = Lock()

keep_running = True

def running():
    return keep_running


# array of bools to encode string
def toBinary(numList):
    bin = ''
    # get every item from array and connect it to string
    for i in numList:
        bin = bin + str(i)
    # return encode string
    return bin.encode()

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global keep_running
        if self.path[8] == '1':
            keep_running = False
        else:
            if self.path[0:3] == '/?c':
                global arrayToSend
                lock.acquire()
                arrayToSend = [self.path[4],self.path[5],self.path[6],self.path[7]]
                lock.release()
            else:
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                f = open("index.html", "r")
                self.wfile.write(str(f.read()))
        return


def webServer():
    server = HTTPServer(('', 8080), myHandler)
    while running():
        server.handle_request()

    return


# connect to server and send control signals
def connectToServer():
    # connect to the server
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((serverIp, serverPort))

    # set reference array to compare that the client only sends by changes
    global arrayToSend
    lastSend = arrayToSend[:]

    while threadKeys.isAlive():
        # lock before entering area
        lock.acquire()
        # check for changes
        if not arrayToSend == lastSend:
            # send to server
            s.send(toBinary(arrayToSend))
            # copy input of array to reference array
            lastSend = arrayToSend[:]
        # release area
        lock.release()

    # close connecton to server
    s.close()

# init threads for key listener and sender
threadKeys = Thread(target = webServer)
threadServer = Thread(target = connectToServer)

if __name__ == "__main__":
    # start threads
    threadKeys.start()
    threadServer.start()
