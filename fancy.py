#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
import signal
import configparser


LOGLEVEL =      1  # 0: silent, 1: important msgs, 2: verbose, 3: very verbose
PWM_GPIO =      14 # Pin 8, Pin 4 = +5V, Pin 6 = Gnd
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
            logfile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S ") + message + "\n")

def endProg(error = 0):
    log(1, "Fancy will end now, cleaning up.")
    GPIO.cleanup()
    sys.exit(error)

parser = configparser.ConfigParser()
parser.read(CONF_FILE_STR)
default = parser["Default"]

try:
    LOGLEVEL = int(default["LOGLEVEL"].split('#')[0])
    WAIT_TIME = int(default["WAIT_TIME"].split('#')[0])
    PWM_GPIO = int(default["PWM_GPIO"].split('#')[0])
    MIN_TEMP = int(default["MIN_TEMP"].split('#')[0])
    MAX_TEMP = int(default["MAX_TEMP"].split('#')[0])
except:
    log(0, "Parse error in fancy.conf.")
    sys.exit(1)

signal.signal(signal.SIGTERM, endProg)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_GPIO, GPIO.OUT, initial = GPIO.LOW)

fan = GPIO.PWM(PWM_GPIO, PWM_FREQ)
fan.start(0);

log(1, "Starting up fancy.")
log(1, "Log level: {:d}, GPIO: {:d}, Interval: {:d} ".format(LOGLEVEL, PWM_GPIO, WAIT_TIME))
log(1, "Min temperature: {:d}°C, Max temperature: {:d}°C".format(MIN_TEMP, MAX_TEMP))
lastspeed = 0

if (MIN_TEMP >= MAX_TEMP):
    log(0, "Min temperature should be smaller than max temperature!")
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
            log(2, "Temp: {:4.1f}°C, Fanspeed: {:3d}%".format(temp, speed))
            lastspeed = speed
        else:
            log(3, "Temp: {:4.1f}°C, Fanspeed: {:3d}%".format(temp, speed))

        fan.ChangeDutyCycle(speed)
        time.sleep(WAIT_TIME)
finally:
    endProg()

