# fancy
Raspberry Pi PWM Fan Control Service

Hardware prerequisites: Rspberry PI and 5V-fan with pwm pin.
Software prerequisites: Debian Buster, Python 3, bash

For installation type:

sudo bash ./install.sh

Configuration goes to /etc/fancy.conf.

Fan installation (Pin 8 is GPIO 14):

____________________     
|                  |      Fan
|  Raspi       1 2 |
|              2 4-|----  +5V
|              5 6-|----- GND
|              7 8-|----- PWM
|                  |
