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
    systemctl stop rpmled
    systemctl disable rpmled
else
    cp rpmled.service /lib/systemd/system/rpmled.service
    cp rpmled.py /usr/local/bin/rpmled.py
    chmod +x /usr/local/bin/rpmled.py
    systemctl enable rpmled
    systemctl restart rpmled
fi
