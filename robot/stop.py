#! /usr/bin/env python3

from ev3dev.ev3 import *

right = Motor('outC')
left = Motor('outB')

right.run_forever(speed_sp=0)
left.run_forever(speed_sp=0)
