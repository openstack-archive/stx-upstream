# List of packages to be included/installed in ISO
# If these have dependencies, they will be pulled in automatically
#

# ceph
ceph
ceph-common
ceph-fuse
ceph-radosgw
libcephfs1
python-cephfs
python-ceph-compat

# ceph-manager
ceph-manager

# openstack-murano
openstack-murano-common
openstack-murano-engine
openstack-murano-api
openstack-murano-cf-api
openstack-murano-doc

# python-muranoclient
python2-muranoclient
python-muranoclient-doc

# openstack-murano-ui
openstack-murano-ui
openstack-murano-ui-doc

# openstack-ironic
openstack-ironic-common
openstack-ironic-api
openstack-ironic-conductor

# python-ironicclient
python2-ironicclient

# python-magnumclient
python2-magnumclient
python-magnumclient-doc
# python-magnumclient-tests

# openstack-magnum
python-magnum
openstack-magnum-common
openstack-magnum-conductor
openstack-magnum-api
openstack-magnum-doc
python-magnum-tests

# openstack-magnum-ui
openstack-magnum-ui

# openstack-ras
openstack-ras

# openstack-ceilometer
python-ceilometer
openstack-ceilometer-common
openstack-ceilometer-notification
openstack-ceilometer-ipmi
openstack-ceilometer-polling
# ceilometerclient is needed by horizon temporarily
python2-ceilometerclient

# openstack-cinder
openstack-cinder

# openstack-glance
openstack-glance

# gnocchi
python-gnocchi
gnocchi-api
gnocchi-common
gnocchi-metricd
gnocchi-statsd

# python-gnocchiclient
python2-gnocchiclient

# openstack-heat
openstack-heat-common
openstack-heat-engine
openstack-heat-api
openstack-heat-api-cfn
openstack-heat-api-cloudwatch

# wrs-heat-templates
wrs-heat-templates

# python-django-horizon
python-django-horizon
openstack-dashboard

# stx-dashboard
starlingx-dashboard

# openstack-keystone
openstack-keystone

# python-networking-bgpvpn
python2-networking-bgpvpn
python-networking-bgpvpn-dashboard
python-networking-bgpvpn-heat

# python-networking-sfc
python2-networking-sfc

# python-networking-odl
python-networking-odl

# openstack-neutron
openstack-neutron
python-neutron
openstack-neutron-common
openstack-neutron-ml2
openstack-neutron-openvswitch
openstack-neutron-sriov-nic-agent

# python-neutron-dynamic-routing
python2-neutron-dynamic-routing

# openstack-nova
openstack-nova-common
openstack-nova-compute
openstack-nova-network
openstack-nova-scheduler
openstack-nova-api
openstack-nova-conductor
openstack-nova-console
openstack-nova-cells
openstack-nova-cert
openstack-nova-novncproxy
openstack-nova-spicehtml5proxy
openstack-nova-serialproxy
openstack-nova-placement-api
python-nova

# python-novaclient
python2-novaclient

# distributedcloud
distributedcloud-dcmanager
distributedcloud-dcorch

# distributedcloud-client
distributedcloud-client-dcmanagerclient

# openstack-panko
python-panko
openstack-panko-api
openstack-panko-common
openstack-panko-config

# rabbitmq-server
rabbitmq-server
rabbitmq-server-config

# python-openstackclient
python2-openstackclient

# python-django-openstack-auth
python2-django-openstack-auth

# python-wsme
python2-wsme

# openstack-swift
openstack-swift-object
openstack-swift-account
openstack-swift-container
openstack-swift-proxy

# stx-ocf-scripts
stx-ocf-scripts

# openstack-barbican
openstack-barbican
openstack-barbican-api
openstack-barbican-common
openstack-barbican-keystone-listener
openstack-barbican-worker
puppet-barbican
python-barbican
python2-barbicanclient
python-ldap3
