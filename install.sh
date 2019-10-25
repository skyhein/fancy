#!/usr/bin/env bash

if [[ "$EUID" -ne "0" ]]
then
	echo "$0 must be run as root" 1>&2
	exit 1
fi

echo "Install with LED support? [Y|n]"
read answer

if [ -f /etc/fancy.conf ]
then
	mv /etc/fancy.conf /etc/fancy.conf.old
fi
cp fancy.conf /etc/fancy.conf
cp fancy.service /lib/systemd/system/fancy.service
cp fancy.py /usr/local/bin/fancy.py
chmod +x /usr/local/bin/fancy.py

systemctl enable fancy
systemctl restart fancy

if [ "$answer" == "n" -o "$answer" == "N" ] 
then
    echo "disabling rpm service"
    systemctl stop rpm
    systemctl disable rpm
else
    cp rpm.service /lib/systemd/system/rpm.service
    cp rpm.py /usr/local/bin/rpm.py
    chmod +x /usr/local/bin/rpm.py
    systemctl enable rpm
    systemctl restart rpm
fi
