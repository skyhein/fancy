#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import signal
import sys
from datetime import datetime
import configparser

TACHO_GPIO    = 15
CONF_FILE_STR = "/etc/fancy.conf"

def endProg(error = 0):
    GPIO.cleanup()
    sys.exit(error)

parser = configparser.ConfigParser()
parser.read(CONF_FILE_STR)
default = parser["Default"]

try:
    TACHO_GPIO = int(default["TACHO_GPIO"].split('#')[0])
except:
    print("Parse error in fancy.conf")

signal.signal(signal.SIGTERM, endProg)

t = time.time()
dt = 0

def falling_cb(channel):
    global t
    global dt
    dt = time.time() - t
    t = time.time()

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TACHO_GPIO, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(TACHO_GPIO, GPIO.FALLING, callback = falling_cb)
    while True:
        time.sleep(1)
        if time.time() - t > 1:
            print("RPM = 0")
        else:
            freq = 1 / dt
            rpm = freq * 60 / 2
            print("RPM = {:.0f}".format(rpm))

finally:
    endProg(0)
