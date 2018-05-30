#!/bin/sh

#########################################################
#
# pkt-capture.sh <interface> <interval>
#
# Measures the received packets on specified interface
# for specified interval (in seconds). 
#
#########################################################

pcksFile="/sys/class/net/$1/statistics/rx_packets"
nbPcks=`cat $pcksFile`
sleep $2
echo $(expr `cat $pcksFile` - $nbPcks)
