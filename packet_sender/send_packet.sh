#!/bin/bash

if [ $EUID != 0 ]; then
    echo "This Script Must Run as Root, use \"sudo ./$0\""
    exit 1
fi

if [ $# != 5 ]; then
    echo "usage: sudo $0 <interface> <pps> <loop> <limit> <protocol>"
    echo "eg: sudo $0 enp1s0 100 1000 1000 s7comm"
    exit 1
fi

PCAP_PATH="/usr/local/lib/python3.6/dist-packages/bolean_replay/pcap/"

if [ $5 != 'all' ]; then
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/$5/$5.pcap
    # echo pcaps/$5.pcap
else
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/ICS/s7/s7_all.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/ICS/modbous/modbous.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/http/http.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/ftp/ftp.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/telnet/telnet.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/ssh/ssh.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/smtp/smtp.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/pop/pop.pcap
    tcpreplay -i $1 -p $2 -l $3 -L $4 pcaps/icmp/icmp.pcap
    # echo pcaps/s7comm.pcap
    # echo pcaps/modbous.pcap
fi


echo "Done"

