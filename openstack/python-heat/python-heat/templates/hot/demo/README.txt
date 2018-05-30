##############################################################################
# 
# CPU Scaling UP / DOWN Demo
#
#
# Creates two VMs:
#
#    1. traffic-generator 
#          - iperf client sending traffic to network-appliance
#          - pause / unpause this VM to control load on network-appliance VM
#          - NOTE use ubuntu-cfntools.img 
#                 (ubuntu 16.04 with cloud-init and cfn-tools installed)
#          - NOTE cloud-init and cfn-init used to create required config files, and
#                 install required tools (i.e. iperf).
#
#    2. network-appliance
#          - iperf server receiving and sending back traffic to iperf client
#          - also starts 'dd ...' when traffic starts, to cause more load on system
#          - this VM auto-scales cpu up and down based on cpu load cfn-pushed to Titanium
#          - NOTE use ubuntu-cfntools.img
#                 (ubuntu 16.04 with cloud-init and cfn-tools installed)
#          - NOTE cloud-init and cfn-init used to create required config files, and
#                 install required tools.
#                 ( i.e. iperf, Titanium Guest Scaling SDK Module, collectd, 
#                        influxdb and grafana )
# 

openstack stack create -t scaleUpDown.yaml demo

watch "ceilometer sample-list -m net_appl_cpu_load -l 10; ceilometer alarm-list | fgrep net_appl"

http://<network-appliance-FLOATING-IP>:3000

openstack stack delete demo

