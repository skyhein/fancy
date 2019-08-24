# fancy
Raspberry Pi PWM Fan Control Service

For installation type:

sudo ./install.sh

Configuration goes to /etc/fancy.conf.

Hardware needed: 5V fan with pwm pin.

Fan installation (Pin 8 is GPIO 14):

____________________     
|                  |      Fan
|  Raspi       1 2 |
|              2 4-|----  +5V
|              5 6-|----- GND
|              7 8-|----- PWM
|                  |
