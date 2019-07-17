#! /usr/bin/env python3
# -*- encoding: UTF8 -*-

'''
TODO: Gyro Sensor
'''

from socket import *
from ev3dev.ev3 import *
from time import sleep
from sys import exit
from threading import Thread
import csv
import uuid

echoPort = 50007
bufsize = 1024

csL = ColorSensor('in1')
csL.mode='COL-REFLECT'
csM = ColorSensor('in2')
csM.mode='COL-REFLECT'
csR = ColorSensor('in3')
csR.mode='COL-REFLECT'

'''
gsGA = GyroSensor('in4')
gsGA.mode='GYRO-G&A'
'''

right = Motor('outC')
left = Motor('outB')

def millis():
    return int(round(time.time() * 1000))

def controlEngine(instructions):
    if instructions == '0100':
        right.run_forever(speed_sp=180)
        left.run_forever(speed_sp=180)
    elif instructions == '1000':
        right.run_forever(speed_sp=180)
        left.run_forever(speed_sp=0)
    elif instructions == '0001':
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=180)
    elif instructions == '1100':
        right.run_forever(speed_sp=180)
        left.run_forever(speed_sp=30)
    elif instructions == '0101':
        right.run_forever(speed_sp=30)
        left.run_forever(speed_sp=180)
    elif instructions == '0010':
        right.run_forever(speed_sp=-180)
        left.run_forever(speed_sp=-180)
    else:
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=0)


def server():
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(('', echoPort))
    s.listen(1)

    print('server is up')

    conn, (remotehost, remoteport) = s.accept()
    print('connected with '  + str(remotehost) + ':' + str(remoteport))

    '''
    sensorVal = []
    s = time.time()
    '''

    while 1:
        data = conn.recv(bufsize)
        controlEngine(str(data)[-5:-1])
        #sensorVal.append([str(time.time()-s),str(data)[-5:-1]])

        if not data:
            break

    '''
    with open('drive-a.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(sensorVal)
    '''

    print('connection is closed')
    controlEngine('0000')
    s.close()


def getSensorData():
    csvData = [['speedLeft', 'speedRight', 'left', 'middle', 'right','time']]

    while left.speed + right.speed <= 0:
        time.sleep(0.05)

    print('sensors are up')


    startATime = time.time()
    loopCount = 1
    while threadServer.isAlive():

        sensorVal = [str(left.speed), str(right.speed), str(csL.value()), str(csM.value()), str(csR.value()), str(millis()-startATime)]
        csvData.append(sensorVal)

        timeGap = (startATime+0.045*loopCount)-time.time()
        time.sleep(timeGap if timeGap > 0 else 0)

        loopCount += 1

    with open('data-collection-human-drive-' + uuid.uuid4().hex[:6].upper() + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerows(csvData)

    print('CSV file is written')

    csvFile.close()


threadServer = Thread(target = server)
threadSensor = Thread(target = getSensorData)

if __name__ == "__main__":
    threadServer.start()
    threadSensor.start()
