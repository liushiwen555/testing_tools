#!/bin/bash

if [ $EUID != 0 ]; then
    echo "This Script Must Run as Root, use \"sudo ./$0\""
    exit 1
fi

if [ $# != 5 ]; then
    echo "usage: sudo $0 <interface> <pps> <loop> <limit> <pcap_file>"
    echo "eg: sudo $0 enp1s0 100 1000 1000 s7comm.pcap"
    exit 1
fi

tcpreplay -i $1 -p $2 -l $3 -L $4 $5
