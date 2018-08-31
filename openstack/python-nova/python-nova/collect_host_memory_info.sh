#!/bin/bash
#
# Copyright (c) 2013-2018 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
# This script is intended to collect host memory information and append
# that info to collect_host_memory_info.log in /var/log/nova

logfile="/var/log/nova/collect_host_memory_info.log"

touch ${logfile}
echo "`date '+%F %T'`: Collect of host memory info" >> ${logfile}

echo "process listing" >> ${logfile}
echo "---------------" >> ${logfile}
ps -eLf >> ${logfile} 2>> ${logfile}

echo "lsof huge mounts" >> ${logfile}
echo "----------------" >> ${logfile}
lsof -n +c 15 | awk '($3 !~ /^[0-9]+$/ && /\/mnt\/huge/) || NR==1 {print $0;}' >> ${logfile} 2>> ${logfile}

echo "numa maps" >> ${logfile}
echo "---------" >> ${logfile}
grep huge /proc/*/numa_maps >> ${logfile} 2>> ${logfile}

tail -vn +1 /proc/meminfo >> ${logfile} 2>> ${logfile}
tail -vn +1 /sys/devices/system/node/node?/meminfo >> ${logfile} 2>> ${logfile}
tail -vn +1 /sys/devices/system/node/node?/hugepages/hugepages-*/*_hugepages >> ${logfile} 2>> ${logfile}

echo "find /mnt/huge-2048kB|xargs ls -ld" >> ${logfile}
echo "----------------------------------" >> ${logfile}
find /mnt/huge-2048kB|xargs ls -ld >> ${logfile} 2>> ${logfile}

echo "find /mnt/huge-1048576kB/|xargs ls -ld" >> ${logfile}
echo "--------------------------------------" >> ${logfile}
find /mnt/huge-1048576kB/|xargs ls -ld >> ${logfile} 2>> ${logfile}

echo "Locked smaps" >> ${logfile}
echo "------------" >> ${logfile}
grep Locked: /proc/*/smaps 2>/dev/null | awk '($2 > 0) {a[$1]+=$2} END {for (i in a) print i,a[i]/1024.0, "MiB";}' >> ${logfile} 2>> ${logfile}

date '+%F %T' >> ${logfile} 2>> ${logfile}

exit 0
