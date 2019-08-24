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

PWM_FREQ =      50 # Hz
TEMPFILE_STR =  "/sys/class/thermal/thermal_zone0/temp"
LOGFILE_STR =   "/var/log/fancy.log"
CONF_FILE_STR = "/etc/fancy.conf"

tempSteps =     [40, 42, 45, 50, 55, 60]   # °C
speedSteps =  [0, 20, 40, 70, 80, 90, 100] # %

def log(verboselevel, message):
    if verboselevel <= LOGLEVEL:
        with open(LOGFILE_STR, "a+") as logfile:
            logfile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + message)

def endProg(error = 0):
    log(1, "Fancy will end now, cleaning up.\n")
    GPIO.cleanup()
    sys.exit(error)

conf = configparser.ConfigParser()
conf.read(CONF_FILE_STR)
default = conf["Default"]
LOGLEVEL=int(default["LOGLEVEL"].split('#')[0])
WAIT_TIME=int(default["WAIT_TIME"].split('#')[0])
FAN_GPIO=int(default["FAN_GPIO"].split('#')[0])

signal.signal(signal.SIGTERM, endProg)
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_GPIO, GPIO.OUT, initial = GPIO.LOW)

fan = GPIO.PWM(FAN_GPIO, PWM_FREQ)
fan.start(0);

log(1, "Starting up fancy.\n")
log(1, "Log level: " + str(LOGLEVEL) + ", GPIO: " + str(FAN_GPIO) + ", Interval: " + str(WAIT_TIME) + "\n")
lastspeed = 0

if (len(speedSteps) != len(tempSteps) + 1):
    log(0, "There should be one more speedstep than tempstep\n")
    endProg(1)

try:
    speed = 0
    while(1):
        with open(TEMPFILE_STR, "r") as temperatureFile:
            temp = float(temperatureFile.read()) / 1000

        if temp < tempSteps[0]:
            speed = speedSteps[0]
        elif temp >= tempSteps[len(tempSteps) -1]:
            speed = speedSteps[len(speedSteps) -1]
        for i in range(0, len(tempSteps) - 1):
            if temp >= tempSteps[i] and temp < tempSteps[i + 1]:
                speed = speedSteps[i + 1]

        if speed != lastspeed:
            log(2, "Temp: " + str(temp) + "°C, Fanspeed: " + str(speed) + "%\n")
        else:
            log(3, "Temp: " + str(temp) + "°C, Fanspeed: " + str(speed) + "%\n")
        lastspeed = speed

        fan.ChangeDutyCycle(speed)
        time.sleep(WAIT_TIME)
finally:
    endProg()

