#! /usr/bin/env python3

from ev3dev.ev3 import *
import csv
from time import sleep

right = Motor('outC')
left = Motor('outB')

def millis():
    return int(round(time.time() * 1000))

def controlEngine(instructions):
    if instructions == '0100':
        right.run_forever(speed_sp=200)
        left.run_forever(speed_sp=200)
    elif instructions == '1000':
        right.run_forever(speed_sp=200)
        left.run_forever(speed_sp=0)
    elif instructions == '0001':
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=200)
    elif instructions == '1100':
        right.run_forever(speed_sp=200)
        left.run_forever(speed_sp=30)
    elif instructions == '0101':
        right.run_forever(speed_sp=30)
        left.run_forever(speed_sp=200)
    elif instructions == '0010':
        right.run_forever(speed_sp=-200)
        left.run_forever(speed_sp=-200)
    else:
        right.run_forever(speed_sp=0)
        left.run_forever(speed_sp=0)

'''
csv.register_dialect('instructions',delimiter =';',skipinitialspace=True)
with open('drive-a.csv', 'r') as csvFile:
    reader = csv.reader(csvFile, dialect='instructions')
    t = 0
    for row in reader:
        time.sleep(float(row[0])-t)
        t = float(row[0])
        controlEngine(row[1])

csv.register_dialect('instructions',delimiter =';',skipinitialspace=True)
with open('drive.csv', 'r') as csvFile:
    reader = csv.reader(csvFile, dialect='instructions')
    next(reader)

    timeBefore = 0
    for row in reader:
        timeToRun = float(row[5])-timeBefore
        startTime = time.time()

        right.run_forever(speed_sp=row[1])
        left.run_forever(speed_sp=row[0])

        restTime = timeToRun-(time.time()-startTime)
        if restTime > 0:
            time.sleep(restTime)

        timeBefore = float(row[5])

csvFile.close()



'''

csv.register_dialect('instructions',delimiter =';',skipinitialspace=True)
with open('drive.csv', 'r') as csvFile:
    reader = csv.reader(csvFile, dialect='instructions')
    next(reader)

    startATime = time.time()
    loopCount = 1
    for row in reader:

        right.run_forever(speed_sp=row[1])
        left.run_forever(speed_sp=row[0])

        timeGap = (startATime+0.045*loopCount)-time.time()
        time.sleep(timeGap if timeGap > 0 else 0)

        loopCount += 1



csvFile.close()

right.run_forever(speed_sp=0)
left.run_forever(speed_sp=0)
