#!/usr/bin/env bash

if [[ "$EUID" -ne "0" ]]
then
	echo "$0 must be run as root" 1>&2
	exit 1
fi

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

cp rpm.py /usr/local/bin/rpm
chmod +x /usr/local/bin/rpm
