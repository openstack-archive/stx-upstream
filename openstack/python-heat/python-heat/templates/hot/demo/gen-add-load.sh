#!/bin/sh

#
# 'gen-add-load.sh'
# -----------------
#
# Monitors incoming packets on ens3 interface with 'pkt-capture.sh' 
#
# When incoming traffic goes above threshold of 1000 pkts/2seconds,
# starts a DD command to add more load than just handling the traffic.
# (i.e. mimicking doing some work on the traffic)
#
# When incoming traffic goes below threshold of 1000 pkts/2seconds,
# stops the DD command.
# 

command="dd if=/dev/zero of=/dev/null"
pid=0

addLoadRunning=false

while true 
do
	nbPcks=`/usr/bin/pkt-capture.sh ens3 2`
	echo $nbPcks

	if test $nbPcks -gt 1000
	then
		if ( ! $addLoadRunning )
		then
			echo "Starting DD command."
			$command &
			pid=$!
		fi
		echo "TRAFFIC RUNNING"
		addLoadRunning=true
	else
		if ( $addLoadRunning )
		then
			echo "Stopping DD command."
			kill $pid
		fi
		echo "No Traffic"
		addLoadRunning=false
	fi
	echo
done

