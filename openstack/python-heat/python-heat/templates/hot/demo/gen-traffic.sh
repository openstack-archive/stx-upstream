#!/bin/sh

#
# 'gen-traffic.sh'
# -----------------
#
# in a forever loop:
#      call iperf client, sending to 10.10.10.50 (fixed ip of iperf server, network-appliance)
#      for 600 seconds.
#      ( iperf -c ... seems to sometimes get hung if using a longer time interval )
#

while true
do
    date
    echo "Starting traffic ..."
    /usr/bin/iperf -c 10.10.10.50 -t 600
    date
    echo "Traffic stopped."
    echo
done
