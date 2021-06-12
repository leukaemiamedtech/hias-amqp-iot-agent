#!/bin/bash

FMSG="- HIAS AMQP IoT Agent installation terminated"

read -p "? This script will install the HIAS AMQP IoT Agent on your device. Are you ready (y/n)? " cmsg

if [ "$cmsg" = "Y" -o "$cmsg" = "y" ]; then
    echo "- Installing HIAS AMQP IoT Agent"
	pip3 install --user flask
	pip3 install --user requests
	pip3 install --user web3
    echo "- HIAS AMQP IoT Agent installed!"
else
    echo $FMSG;
    exit
fi