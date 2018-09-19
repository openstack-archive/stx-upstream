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

%description
OpenStack Resource Agents from Madkiss

%prep
%autosetup -p 1 

%install
%make_install
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-agent-central
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-alarm-evaluator
rm -rf ${RPM_BUILD_ROOT}/usr/lib/ocf/resource.d/openstack/ceilometer-alarm-notifier

%files
%defattr(-,root,root,-)
%dir "/usr/lib/ocf/resource.d/openstack"
"/usr/lib/ocf/resource.d/openstack/glance-registry"
"/usr/lib/ocf/resource.d/openstack/nova-network"
"/usr/lib/ocf/resource.d/openstack/keystone"
"/usr/lib/ocf/resource.d/openstack/heat-engine"
"/usr/lib/ocf/resource.d/openstack/nova-novnc"
"/usr/lib/ocf/resource.d/openstack/cinder-api"
"/usr/lib/ocf/resource.d/openstack/neutron-agent-dhcp"
"/usr/lib/ocf/resource.d/openstack/cinder-volume"
"/usr/lib/ocf/resource.d/openstack/neutron-agent-l3"
"/usr/lib/ocf/resource.d/openstack/cinder-schedule"
"/usr/lib/ocf/resource.d/openstack/nova-consoleauth"
"/usr/lib/ocf/resource.d/openstack/ceilometer-api"
"/usr/lib/ocf/resource.d/openstack/nova-scheduler"
"/usr/lib/ocf/resource.d/openstack/neutron-server"
"/usr/lib/ocf/resource.d/openstack/glance-api"
"/usr/lib/ocf/resource.d/openstack/nova-api"
"/usr/lib/ocf/resource.d/openstack/neutron-metadata-agent"
"/usr/lib/ocf/resource.d/openstack/ceilometer-collector"
