#!/bin/bash -v

#########################################################
#
# Install script for network-appliance VM 
# called thru cloud-init
#
#########################################################

echo "Starting setup of network appliance ..." >> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "Installing iperf ..." >> /var/log/heat_setup.txt
apt-get -y install iperf >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "Installing python-pip ..." >> /var/log/heat_setup.txt
apt-get -y install gcc python-dev python-pip >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "Installing psutil ..." >> /var/log/heat_setup.txt
pip install psutil >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt


# Create sym links to standard location for cfn tools in an aws environment
echo >> /var/log/heat_setup.txt
echo "Setting up symlinks" >> /var/log/heat_setup.txt
cfn-create-aws-symlinks --source /usr/bin >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

# invoke cfn-init which will extract the cloudformation metadata from the userdata
echo >> /var/log/heat_setup.txt
echo "Setting up cfn-init " >> /var/log/heat_setup.txt
/usr/bin/cfn-init >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "Installing Guest SDK ..." >> /var/log/heat_setup.txt
git clone https://github.com/Wind-River/titanium-cloud.git >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
cat >  /lib/systemd/system/guest-agent.service << EOF
[Unit]
Description=Guest Agent
After=cloud-init.service

[Service]
ExecStart=/usr/sbin/guest_agent
Type=simple
Restart=always
RestartSec=0

[Install]
WantedBy=guest-scale-agent.service
WantedBy=multi-user.target

EOF
cd titanium-cloud/guest-API-SDK/17.06/
apt-get -y install build-essential libjson0 libjson0-dev >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
cd wrs-server-group-2.0.4/
mkdir obj bin lib
make >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
cp bin/* /usr/sbin
cp lib/libguesthostmsg.so.2.0.4 lib/libservergroup.so.2.0.4 /usr/lib/
ldconfig
cd ../wrs-guest-scale-2.0.4/
mkdir obj bin lib
make >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
cp bin/guest_scale_agent /usr/sbin
cd scripts/
cp app_scale_helper offline_cpus /usr/sbin
chmod 755 init_offline_cpus offline_cpus
cp init_offline_cpus /etc/init.d
cp guest-scale-agent.service offline-cpus.service /lib/systemd/system/
systemctl enable guest-agent.service
systemctl enable guest-scale-agent.service
systemctl enable offline-cpus.service
systemctl start guest-agent.service
systemctl start guest-scale-agent.service


echo >> /var/log/heat_setup.txt
echo "Starting collectd and grafana install ..." >> /var/log/heat_setup.txt

apt-get -y update >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-get -y dist-upgrade >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-get -y install openssh-server >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
echo >> /var/log/heat_setup.txt
echo "Setup gpg keys ..." >> /var/log/heat_setup.txt
gpg --recv-keys 3994D24FB8543576 >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
gpg --recv-keys 3994D24FB8543576 >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
gpg --recv-keys 3994D24FB8543576 >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
sh -c 'gpg --export -a 3994D24FB8543576 | apt-key add -' >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
sh -c 'gpg --export -a 3994D24FB8543576 | apt-key add -' >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
sh -c 'gpg --export -a 3994D24FB8543576 | apt-key add -' >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
echo >> /var/log/heat_setup.txt
echo "Get influxdb key and packagecloud key ..." >> /var/log/heat_setup.txt
# don't use latest influxdb yet, it has bugs
# sh -c 'curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -' >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
sh -c 'curl https://packagecloud.io/gpg.key | apt-key add -' >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
echo >> /var/log/heat_setup.txt
echo "Setup collectd, influxdb and grafana .list files ..." >> /var/log/heat_setup.txt
echo "deb http://pkg.ci.collectd.org/deb xenial collectd-5.8" > /etc/apt/sources.list.d/collectd.list
# don't use latest influxdb yet, it has bugs
# echo "deb https://repos.influxdata.com/debian xenial stable" > /etc/apt/sources.list.d/influxdb.list
echo "deb https://packagecloud.io/grafana/stable/debian/ jessie main" > /etc/apt/sources.list.d/grafana.list
 
echo >> /var/log/heat_setup.txt
echo "apt-get update ..." >> /var/log/heat_setup.txt
apt-get -y update >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
echo >> /var/log/heat_setup.txt
echo "apt-cache ..." >> /var/log/heat_setup.txt
apt-cache madison collectd >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-cache madison influxdb >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-cache madison influxdb-client >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-cache madison grafana >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "apt-get install collectd ..." >> /var/log/heat_setup.txt
apt-get -y install collectd >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "apt-get install influxdb ..." >> /var/log/heat_setup.txt
apt-get -y install influxdb >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "apt-get install influxdb-client ..." >> /var/log/heat_setup.txt
apt-get -y install influxdb-client >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "apt-get install grafana ..." >> /var/log/heat_setup.txt
apt-get -y install grafana >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
echo >> /var/log/heat_setup.txt
echo "apt-get cleanup ..." >> /var/log/heat_setup.txt
apt-get -y update >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-get -y dist-upgrade >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-get -y autoclean >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
apt-get -y autoremove >> /var/log/heat_setup.txt 2>> /var/log/heat_setup.txt
 
mv /etc/collectd/collectd.conf /etc/collectd/collectd.conf.ORIG
cat >>  /etc/collectd/collectd.conf << EOF

LoadPlugin network
<Plugin "network">
Server "127.0.0.1" "25826"
</Plugin>

<Plugin cpu>
ReportByCpu true
ReportByState false
ValuesPercentage false
ReportNumCpu true
</Plugin>

EOF

 
cp /etc/influxdb/influxdb.conf /etc/influxdb/influxdb.conf.ORIG
sed -i -e '/^\[collectd\].*/,/enabled = false/d' /etc/influxdb/influxdb.conf
cat >>  /etc/influxdb/influxdb.conf << EOF

[collectd]
  enabled = true
  bind-address = ":25826"
  database = "collectd"
  typesdb = "/usr/share/collectd/types.db"
EOF
 
echo >> /var/log/heat_setup.txt
echo "start grafana-server ..." >> /var/log/heat_setup.txt
systemctl start grafana-server
 
echo >> /var/log/heat_setup.txt
echo "start influxdb ..." >> /var/log/heat_setup.txt
systemctl start influxdb
 
echo >> /var/log/heat_setup.txt
echo "start collectd ..." >> /var/log/heat_setup.txt
systemctl start collectd
 
echo >> /var/log/heat_setup.txt
echo "enable grafana-server ..." >> /var/log/heat_setup.txt
systemctl enable grafana-server.service

echo >> /var/log/heat_setup.txt
echo "enable influxdb.service ..." >> /var/log/heat_setup.txt
systemctl enable influxdb.service

echo >> /var/log/heat_setup.txt
echo "enable collectd.service ..." >> /var/log/heat_setup.txt
systemctl enable collectd.service


echo >> /var/log/heat_setup.txt
echo "Starting network appliance server service ..." >> /var/log/heat_setup.txt
update-rc.d iperf-server-service defaults 97 03 >> /var/log/heat_setup.txt
service iperf-server-service start >> /var/log/heat_setup.txt

echo >> /var/log/heat_setup.txt
echo "Starting gen-add-load service ..." >> /var/log/heat_setup.txt
update-rc.d gen-add-load-service defaults 97 03 >> /var/log/heat_setup.txt
service gen-add-load-service start >> /var/log/heat_setup.txt

sleep 5
echo >> /var/log/heat_setup.txt
echo "restart collectd ..." >> /var/log/heat_setup.txt
systemctl restart collectd

sleep 5
echo >> /var/log/heat_setup.txt
echo "restart influxdb ..." >> /var/log/heat_setup.txt
systemctl restart influxdb

echo "Finished user data setup" >> /var/log/heat_setup.txt
