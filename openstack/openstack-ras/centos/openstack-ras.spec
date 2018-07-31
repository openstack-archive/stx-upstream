%define local_dir /usr/local

Summary: openstack-ras
Name: openstack-ras
Version: 1.0.0
Release: 0%{?_tis_dist}.%{tis_patch_ver}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: https://github.com/madkiss/openstack-resource-agents/tree/stable-grizzly
# Note: when upgrading, new upstream URL will be:
# https://git.openstack.org/cgit/openstack/openstack-resource-agents

Requires: /usr/bin/env
Requires: /bin/sh

Source0:  %{name}-%{version}.tar.gz
Source1:  dcorch-identity-api-proxy

%description
OpenStack Resource Agents from Madkiss

%prep
%autosetup -p 1 

%install
%make_install
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-agent-central
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-alarm-evaluator
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-alarm-notifier
install -p -D -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/dcorch-identity-api-proxy

%files
%defattr(-,root,root,-)
%dir "/usr/lib/ocf/resource.d/openstack"
"/usr/lib/ocf/resource.d/openstack/aodh-api"
"/usr/lib/ocf/resource.d/openstack/aodh-evaluator"
"/usr/lib/ocf/resource.d/openstack/aodh-listener"
"/usr/lib/ocf/resource.d/openstack/aodh-notifier"
"/usr/lib/ocf/resource.d/openstack/murano-engine"
"/usr/lib/ocf/resource.d/openstack/murano-api"
"/usr/lib/ocf/resource.d/openstack/magnum-conductor"
"/usr/lib/ocf/resource.d/openstack/magnum-api"
"/usr/lib/ocf/resource.d/openstack/ironic-conductor"
"/usr/lib/ocf/resource.d/openstack/ironic-api"
"/usr/lib/ocf/resource.d/openstack/nova-compute"
"/usr/lib/ocf/resource.d/openstack/heat-api"
"/usr/lib/ocf/resource.d/openstack/glance-registry"
"/usr/lib/ocf/resource.d/openstack/nova-network"
"/usr/lib/ocf/resource.d/openstack/keystone"
"/usr/lib/ocf/resource.d/openstack/heat-engine"
"/usr/lib/ocf/resource.d/openstack/nova-novnc"
"/usr/lib/ocf/resource.d/openstack/nova-serialproxy"
"/usr/lib/ocf/resource.d/openstack/heat-api-cfn"
"/usr/lib/ocf/resource.d/openstack/cinder-api"
"/usr/lib/ocf/resource.d/openstack/neutron-agent-dhcp"
"/usr/lib/ocf/resource.d/openstack/cinder-volume"
"/usr/lib/ocf/resource.d/openstack/neutron-agent-l3"
"/usr/lib/ocf/resource.d/openstack/cinder-schedule"
"/usr/lib/ocf/resource.d/openstack/nova-consoleauth"
"/usr/lib/ocf/resource.d/openstack/ceilometer-api"
"/usr/lib/ocf/resource.d/openstack/nova-scheduler"
"/usr/lib/ocf/resource.d/openstack/nova-conductor"
"/usr/lib/ocf/resource.d/openstack/neutron-server"
"/usr/lib/ocf/resource.d/openstack/validation"
"/usr/lib/ocf/resource.d/openstack/heat-api-cloudwatch"
"/usr/lib/ocf/resource.d/openstack/ceilometer-agent-notification"
"/usr/lib/ocf/resource.d/openstack/glance-api"
"/usr/lib/ocf/resource.d/openstack/nova-api"
"/usr/lib/ocf/resource.d/openstack/neutron-metadata-agent"
"/usr/lib/ocf/resource.d/openstack/ceilometer-collector"
"/usr/lib/ocf/resource.d/openstack/panko-api"
"/usr/lib/ocf/resource.d/openstack/nova-placement-api"
"/usr/lib/ocf/resource.d/openstack/dcorch-snmp"
"/usr/lib/ocf/resource.d/openstack/dcmanager-manager"
"/usr/lib/ocf/resource.d/openstack/dcorch-nova-api-proxy"
"/usr/lib/ocf/resource.d/openstack/dcorch-sysinv-api-proxy"
"/usr/lib/ocf/resource.d/openstack/dcmanager-api"
"/usr/lib/ocf/resource.d/openstack/dcorch-engine"
"/usr/lib/ocf/resource.d/openstack/dcorch-neutron-api-proxy"
"/usr/lib/ocf/resource.d/openstack/dcorch-cinder-api-proxy"
"/usr/lib/ocf/resource.d/openstack/dcorch-patch-api-proxy"
"/usr/lib/ocf/resource.d/openstack/dcorch-identity-api-proxy"
