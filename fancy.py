#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
import signal
import configparser


LOGLEVEL =      1  # 0: silent, 1: important msgs, 2: verbose, 3: very verbose
FAN_GPIO =      14 # Pin 8, Pin 4 = +5V, Pin 6 = Gnd
WAIT_TIME =     10 # s
MIN_TEMP =      40 # °C
MAX_TEMP =      50 # °C

THRESHOLD =     5  # °C
PWM_FREQ =      50 # Hz
TEMPFILE_STR =  "/sys/class/thermal/thermal_zone0/temp"
LOGFILE_STR =   "/var/log/fancy.log"
CONF_FILE_STR = "/etc/fancy.conf"

def log(verboselevel, message):
    if verboselevel <= LOGLEVEL:
        with open(LOGFILE_STR, "a+") as logfile:
            logfile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + message)

def endProg(error = 0):
    log(1, "Fancy will end now, cleaning up.\n")
    GPIO.cleanup()
    sys.exit(error)

parser = configparser.ConfigParser()
parser.read(CONF_FILE_STR)
default = parser["Default"]

try:
    LOGLEVEL=int(default["LOGLEVEL"].split('#')[0])
except:
    pass

try:
    WAIT_TIME=int(default["WAIT_TIME"].split('#')[0])
except:
    pass

try:
    FAN_GPIO=int(default["FAN_GPIO"].split('#')[0])
except:
    pass

try:
    MIN_TEMP=int(default["MIN_TEMP"].split('#')[0])
except:
    pass

try:
    MAX_TEMP=int(default["MAX_TEMP"].split('#')[0])
except:
    pass

signal.signal(signal.SIGTERM, endProg)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_GPIO, GPIO.OUT, initial = GPIO.LOW)

fan = GPIO.PWM(FAN_GPIO, PWM_FREQ)
fan.start(0);

log(1, "Starting up fancy.\n")
log(1, "Log level: " + str(LOGLEVEL) + ", GPIO: " + str(FAN_GPIO) + ", Interval: " + str(WAIT_TIME) + "\n")
log(1, "Min temperature: " + str(MIN_TEMP) + "°C, Max temperature: " + str(MAX_TEMP) + "°C\n")
lastspeed = 0

if (MIN_TEMP >= MAX_TEMP):
    log(0, "Min temperature should be smaller than max temperature!\n")
    endProg(1)

try:
    speed = 0
    lastspeed = 1
    while(1):
        with open(TEMPFILE_STR, "r") as temperatureFile:
            temp = float(temperatureFile.read()) / 1000

        if temp <= MIN_TEMP:
            speed = 0
        elif temp >= MAX_TEMP:
            speed = 100
        else:
            speed = int((100 / (MAX_TEMP - MIN_TEMP)) * (temp - MIN_TEMP))

        if (speed > lastspeed + THRESHOLD) or \
           (speed < lastspeed - THRESHOLD) or \
           (speed == 100 and lastspeed < 100) or \
           (speed == 0 and lastspeed > 0):
            log(2, "Temp: " + str(temp) + "°C, Fanspeed: " + str(speed) + "%\n")
            lastspeed = speed
        else:
            log(3, "Temp: " + str(temp) + "°C, Fanspeed: " + str(speed) + "%\n")

        fan.ChangeDutyCycle(speed)
        time.sleep(WAIT_TIME)
finally:
    endProg()

