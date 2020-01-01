#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys

DEBUG = False
TACHO_GPIO =     15
RED_LED_GPIO =   23
GREEN_LED_GPIO = 24
BLUE_LED_GPIO =  25

def endProg(error = 0):
    print("rpm will end now, cleaning up.")
    GPIO.cleanup()
    sys.exit(error)

signal.signal(signal.SIGTERM, endProg)

t = time.time()
dt = 0

def falling_cb(channel):
    global t
    global dt
    dt = time.time() - t
    t = time.time()

def setLeds(rpm):
    mm = 2500
    if rpm > mm * 2:
        rpm = mm * 2
    if (rpm < mm):
        red_led.ChangeDutyCycle(100)
        green_led.ChangeDutyCycle(100 - rpm / mm * 100)
        blue_led.ChangeDutyCycle(rpm / mm * 100)
    else:
        red_led.ChangeDutyCycle(100 - ((rpm - mm) / mm) * 100)
        green_led.ChangeDutyCycle(((rpm - mm) / mm) * 100)
        blue_led.ChangeDutyCycle(100)

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TACHO_GPIO, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(TACHO_GPIO, GPIO.FALLING, callback = falling_cb)
    GPIO.setup(RED_LED_GPIO, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(GREEN_LED_GPIO, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(BLUE_LED_GPIO, GPIO.OUT, initial = GPIO.HIGH)
    red_led = GPIO.PWM(RED_LED_GPIO, 100)
    green_led = GPIO.PWM(GREEN_LED_GPIO, 100)
    blue_led = GPIO.PWM(BLUE_LED_GPIO, 100)
    red_led.start(0)
    green_led.start(0)
    blue_led.start(0)
    while True:
        time.sleep(1)
        if time.time() - t > 1:
            if DEBUG:
                print("RPM = 0")
            setLeds(0)
        else:
            freq = 1 / dt
            rpm = freq * 60 / 2
            if DEBUG:
                print("RPM = {:.0f}".format(rpm))
            setLeds(rpm)

finally:
    endProg(0)


