#!/bin/bash -v

#########################################################
#
# Install script for traffic-generator VM 
# called thru cloud-init
#
#########################################################

echo "Starting setup of traffic generator ..." >> /var/log/heat_setup.txt

echo "Installing iperf ..." >> /var/log/heat_setup.txt
apt-get -y install iperf >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

# Create sym links to standard location for cfn tools in an aws environment
echo "Setting up symlinks" >> /var/log/heat_setup.txt
cfn-create-aws-symlinks --source /usr/bin

# invoke cfn-init which will extract the cloudformation metadata from the userdata
echo "Setting up cfn-init " >> /var/log/heat_setup.txt
/usr/bin/cfn-init >> /var/log/heat_setup.txt

echo "Starting gen-traffic service ..." >> /var/log/heat_setup.txt
update-rc.d gen-traffic-service defaults 97 03 >> /var/log/heat_setup.txt
service gen-traffic-service start >> /var/log/heat_setup.txt

echo "Finished setup of traffic generator." >> /var/log/heat_setup.txt
