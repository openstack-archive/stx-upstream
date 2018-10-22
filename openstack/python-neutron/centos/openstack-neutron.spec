%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global service neutron

%define cleanup_orphan_rootwrap_daemons() \
for pid in $(ps -f --ppid 1 | awk '/.*neutron-rootwrap-daemon/ { print $2 }'); do \
   kill $(ps --ppid $pid -o pid=) \
done \
%nil

%global common_desc \
Neutron is a virtual network service for Openstack. Just like \
OpenStack Nova provides an API to dynamically request and configure \
virtual servers, Neutron provides an API to dynamically request and \
configure virtual networks. These networks connect "interfaces" from \
other OpenStack services (e.g., virtual NICs from Nova VMs). The \
Neutron API supports extensions to provide advanced network \
capabilities (e.g., QoS, ACLs, network monitoring, etc.)

Name:           openstack-%{service}
Version:        11.0.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Epoch:          1
Summary:        OpenStack Networking Service

License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        %{service}-%{version}.tar.gz
#Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source10:       neutron-server.service
Source11:       neutron-linuxbridge-agent.service
Source12:       neutron-openvswitch-agent.service
Source15:       neutron-dhcp-agent.service
Source16:       neutron-l3-agent.service
Source17:       neutron-metadata-agent.service
Source18:       neutron-ovs-cleanup.service
Source19:       neutron-macvtap-agent.service
Source20:       neutron-metering-agent.service
Source21:       neutron-sriov-nic-agent.service
Source22:       neutron-netns-cleanup.service
Source29:       neutron-rpc-server.service

Source30:       %{service}-dist.conf
Source31:       conf.README
Source32:       neutron-linuxbridge-cleanup.service
#Source33:       neutron-enable-bridge-firewall.sh
#Source34:       neutron-l2-agent-sysctl.conf
# We use the legacy service to load modules because it allows to gracefully
# ignore a missing kernel module (f.e. br_netfilter on earlier kernels). It's
# essentially because .modules files are shell scripts.
#Source35:       neutron-l2-agent.modules

# WRS
Source44:       neutron-dhcp-agent.pmon
Source45:       neutron-metadata-agent.pmon
Source46:       neutron-sriov-nic-agent.pmon
Source49:       neutron-dhcp-agent.init
Source50:       neutron-metadata-agent.init
Source51:       neutron-sriov-nic-agent.init
Source52:       neutron-server.init

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros
BuildRequires:  python2-devel
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python-babel
BuildRequires:  python-d2to1
BuildRequires:  python-keystoneauth1 >= 3.1.0
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-neutron-lib >= 1.9.0
BuildRequires:  python-novaclient
BuildRequires:  python-os-xenapi
BuildRequires:  python-oslo-cache
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-privsep
BuildRequires:  python-oslo-rootwrap
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python-osprofiler >= 1.3.0
BuildRequires:  python-ovsdbapp
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-psutil >= 3.2.2
BuildRequires:  python-pyroute2 >= 0.4.19
BuildRequires:  python-pecan
BuildRequires:  python-tenacity >= 3.2.1
BuildRequires:  python-weakrefmethod >= 1.0.2
BuildRequires:  systemd-units
# WRS
BuildRequires:  systemd
BuildRequires:  tsconfig
BuildRequires:  systemd-devel
BuildRequires:  python-retrying
BuildRequires:  python-networking-sfc

Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}

# dnsmasq is not a hard requirement, but is currently the only option
# when neutron-dhcp-agent is deployed.
Requires:       dnsmasq
Requires:       dnsmasq-utils

# radvd is not a hard requirement, but is currently the only option
# for IPv6 deployments.
Requires:       radvd

# dibbler is not a hard requirement, but is currently the default option
# for IPv6 prefix delegation.
Requires:       dibbler-client

# conntrack is not a hard requirement, but is currently used by L3 agent
# to immediately drop connections after a floating IP is disassociated
Requires:       conntrack-tools

# keepalived is not a hard requirement, but is currently used by DVR L3
# agent
Requires:       keepalived

# haproxy implements metadata proxy process
Requires:       haproxy >= 1.5.0

# Those are not hard requirements, ipset is used by ipset-cleanup in the subpackage,
# and iptables is used by the l3-agent which currently is not in a separate package.
Requires:       ipset
Requires:       iptables

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Obsoletes:      openstack-%{service}-dev-server

%description
%{common_desc}


%package -n python-%{service}
Summary:        Neutron Python libraries
Requires:       python-alembic >= 0.8.7
Requires:       python-debtcollector >= 1.2.0
Requires:       python-designateclient >= 1.5.0
Requires:       python-eventlet >= 0.18.2
Requires:       python-greenlet >= 0.3.2
Requires:       python-httplib2 >= 0.7.5
# Upstream jinja2 set to 2.8 due to Python 3 support.
# CentOS repos currently don't have the packege rebased to 2.8.
Requires:       python-jinja2 >= 2.7
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-keystonemiddleware >= 4.12.0
Requires:       python-netaddr >= 0.7.13
Requires:       python-netifaces >= 0.10.4
Requires:       python-neutronclient >= 6.3.0
Requires:       python-neutron-lib >= 1.9.0
Requires:       python-novaclient >= 9.0.0
Requires:       python-os-xenapi >= 0.2.0
Requires:       python-oslo-cache >= 1.5.0
Requires:       python-oslo-concurrency >= 3.8.0
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-context >= 2.14.0
Requires:       python-oslo-db >= 4.24.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-messaging >= 5.24.2
Requires:       python-oslo-middleware >= 3.27.0
Requires:       python-oslo-policy >= 1.23.0
Requires:       python-oslo-privsep >= 1.9.0
Requires:       python-oslo-reports >= 0.6.0
Requires:       python-oslo-rootwrap >= 5.0.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-oslo-versionedobjects >= 1.17.0
Requires:       python-osprofiler >= 1.4.0
Requires:       python-ovsdbapp
Requires:       python-paste
Requires:       python-paste-deploy >= 1.5.0
Requires:       python-pecan >= 1.0.0
Requires:       python-pbr >= 2.0.0
Requires:       python-psutil >= 3.2.2
Requires:       python-pyroute2 >= 0.4.19
Requires:       python-requests >= 2.10.0
Requires:       python-tenacity >= 3.2.1
Requires:       python-routes >= 2.3.1
Requires:       python-ryu >= 4.14
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-stevedore >= 1.20.0
Requires:       python-weakrefmethod >= 1.0.2
Requires:       python-webob >= 1.7.1



%description -n python-%{service}
%{common_desc}

This package contains the Neutron Python library.


%package -n python-%{service}-tests
Summary:        Neutron tests
Requires:       python-%{service} = %{epoch}:%{version}-%{release}
Requires:       python-ddt >= 1.0.1
Requires:       python-fixtures >= 3.0.0
Requires:       python-mock >= 2.0
Requires:       python-subunit >= 0.0.18
Requires:       python-testrepository >= 0.0.18
Requires:       python-testtools >= 1.4.0
Requires:       python-testresources >= 0.2.4
Requires:       python-testscenarios >= 0.4
Requires:       python-oslotest >= 1.10.0
Requires:       python-oslo-db-tests >= 4.10.0
Requires:       python-os-testr >= 0.7.0
Requires:       python-PyMySQL >= 0.6.2
Requires:       python-tempest >= 12.1.0
Requires:       python-webtest >= 2.0

# pstree is used during functional testing to ensure our internal
# libraries managing processes work correctly.
Requires:       psmisc
# nfs-utils is needed because it creates user with uid 65534 which
# is required by neutron functional tests.
Requires:       nfs-utils


%description -n python-%{service}-tests
%{common_desc}

This package contains Neutron test files.


%package common
Summary:        Neutron common files
Requires(pre): shadow-utils
Requires:       python-%{service} = %{epoch}:%{version}-%{release}
Requires:       sudo


%description common
%{common_desc}

This package contains Neutron common files.


%package linuxbridge
Summary:        Neutron Linuxbridge agent
Requires:       bridge-utils
Requires:       ebtables
Requires:       ipset
Requires:       iptables
# kmod is needed to get access to /usr/sbin/modprobe needed by
# neutron-enable-bridge-firewall.sh triggered by the service unit file
Requires:       kmod
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description linuxbridge
%{common_desc}

This package contains the Neutron agent that implements virtual
networks using VLAN or VXLAN using Linuxbridge technology.


%package macvtap-agent
Summary:        Neutron macvtap agent
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description macvtap-agent
%{common_desc}

This package contains the Neutron agent that implements
macvtap attachments for libvirt qemu/kvm instances.


%package ml2
Summary:        Neutron ML2 plugin
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}
# needed for brocade and cisco drivers
Requires:       python-ncclient


%description ml2
%{common_desc}

This package contains a Neutron plugin that allows the use of drivers
to support separately extensible sets of network types and the mechanisms
for accessing those types.


%package openvswitch
Summary:        Neutron openvswitch plugin
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}
# We require openvswitch when using vsctl to access ovsdb;
# but if we use native access, then we just need python bindings.
# since we don't know what users actually use, we depend on both.
Requires:       ipset
Requires:       iptables
Requires:       openvswitch
Requires:       python-openvswitch >= 2.6.1
# kmod is needed to get access to /usr/sbin/modprobe needed by
# neutron-enable-bridge-firewall.sh triggered by the service unit file
Requires:       kmod


%description openvswitch
%{common_desc}

This package contains the Neutron plugin that implements virtual
networks using Open vSwitch.


%package metering-agent
Summary:        Neutron bandwidth metering agent
Requires:       iptables
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description metering-agent
%{common_desc}

This package contains the Neutron agent responsible for generating bandwidth
utilization notifications.


%package rpc-server
Summary:        Neutron (RPC only) Server
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description rpc-server
%{common_desc}

This package contains an alternative Neutron server that handles AMQP RPC
workload only.


%package sriov-nic-agent
Summary:        Neutron SR-IOV NIC agent
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description sriov-nic-agent
%{common_desc}

This package contains the Neutron agent to support advanced features of
SR-IOV network cards.


%prep
%autosetup -n %{service}-%{upstream_version} -S git

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourseleves
%py_req_cleanup

# Kill egg-info in order to generate new SOURCES.txt
rm -rf neutron.egg-info


%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build
# Generate i18n files
# (amoralej) we can remove '-D neutron' once https://review.openstack.org/#/c/485070/ is merged
#%{__python2} setup.py compile_catalog
pwd
%{__python2} setup.py compile_catalog -d %{service}/locale -D neutron

# Generate configuration files
PYTHONPATH=. tools/generate_config_file_samples.sh
find etc -name *.sample | while read filename
do
    filedir=$(dirname $filename)
    file=$(basename $filename .sample)
    mv ${filename} ${filedir}/${file}
done

# Loop through values in neutron-dist.conf and make sure that the values
# are substituted into the neutron.conf as comments. Some of these values
# will have been uncommented as a way of upstream setting defaults outside
# of the code. For notification_driver, there are commented examples
# above uncommented settings, so this specifically skips those comments
# and instead comments out the actual settings and substitutes the
# correct default values.
while read name eq value; do
  test "$name" && test "$value" || continue
  if [ "$name" = "notification_driver" ]; then
    sed -ri "0,/^$name *=/{s!^$name *=.*!# $name = $value!}" etc/%{service}.conf
  else
    sed -ri "0,/^(#)? *$name *=/{s!^(#)? *$name *=.*!# $name = $value!}" etc/%{service}.conf
  fi
done < %{SOURCE30}

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/bin
rm -rf %{buildroot}%{python2_sitelib}/doc
rm -rf %{buildroot}%{python2_sitelib}/tools

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/%{service}/rootwrap
mv %{buildroot}/usr/etc/%{service}/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/%{service}/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}
# WRS: to do: revisit service files to handle /usr/share rather than /etc/neutron for api-paste.ini
#mv %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini %{buildroot}%{_datadir}/%{service}/api-paste.ini

# The generated config files are not moved automatically by setup.py
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/plugins/ml2

mv etc/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
for agent in dhcp l3 metadata metering
do
  mv etc/${agent}_agent.ini %{buildroot}%{_sysconfdir}/%{service}/${agent}_agent.ini
done
for file in linuxbridge_agent ml2_conf openvswitch_agent sriov_agent
do
  mv etc/%{service}/plugins/ml2/${file}.ini %{buildroot}%{_sysconfdir}/%{service}/plugins/ml2/${file}.ini
done

# Install logrotate
#install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/neutron-server.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/neutron-linuxbridge-agent.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/neutron-openvswitch-agent.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/neutron-dhcp-agent.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/neutron-l3-agent.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/neutron-metadata-agent.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/neutron-ovs-cleanup.service
install -p -D -m 644 %{SOURCE19} %{buildroot}%{_unitdir}/neutron-macvtap-agent.service
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/neutron-metering-agent.service
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/neutron-sriov-nic-agent.service
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_unitdir}/neutron-netns-cleanup.service
install -p -D -m 644 %{SOURCE29} %{buildroot}%{_unitdir}/neutron-rpc-server.service
install -p -D -m 644 %{SOURCE32} %{buildroot}%{_unitdir}/neutron-linuxbridge-cleanup.service

# Install helper scripts
#install -p -D -m 755 %{SOURCE33} %{buildroot}%{_bindir}/neutron-enable-bridge-firewall.sh

# Install sysctl and modprobe config files to enable bridge firewalling
# NOTE(ihrachys) we effectively duplicate same settings for each affected l2
# agent. This can be revisited later.
#install -p -D -m 644 %{SOURCE34} %{buildroot}%{_sysctldir}/99-neutron-openvswitch-agent.conf
#install -p -D -m 644 %{SOURCE34} %{buildroot}%{_sysctldir}/99-neutron-linuxbridge-agent.conf
#install -p -D -m 755 %{SOURCE35} %{buildroot}%{_sysconfdir}/sysconfig/modules/neutron-openvswitch-agent.modules
#install -p -D -m 755 %{SOURCE35} %{buildroot}%{_sysconfdir}/sysconfig/modules/neutron-linuxbridge-agent.modules

# Install README file that describes how to configure services with custom configuration files
install -p -D -m 755 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{service}/conf.d/README

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Install dist conf
install -p -D -m 640 %{SOURCE30} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf

# Create and populate configuration directory for L3 agent that is not accessible for user modification
mkdir -p %{buildroot}%{_datadir}/%{service}/l3_agent
ln -s %{_sysconfdir}/%{service}/l3_agent.ini %{buildroot}%{_datadir}/%{service}/l3_agent/l3_agent.conf

# Create dist configuration directory for neutron-server (may be filled by advanced services)
mkdir -p %{buildroot}%{_datadir}/%{service}/server

# Create configuration directories for all services that can be populated by users with custom *.conf files
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/common
for service in server rpc-server ovs-cleanup netns-cleanup linuxbridge-cleanup macvtap-agent; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service
done
for service in linuxbridge openvswitch dhcp l3 metadata metering sriov-nic; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service-agent
done


# WRS process init scripts
install -d %{buildroot}%{_sysconfdir}/init.d
install -m 755 %{SOURCE49} %{buildroot}%{_sysconfdir}/init.d/neutron-dhcp-agent
install -m 755 %{SOURCE50} %{buildroot}%{_sysconfdir}/init.d/neutron-metadata-agent
install -m 755 %{SOURCE51} %{buildroot}%{_sysconfdir}/init.d/neutron-sriov-nic-agent
install -m 755 %{SOURCE52} %{buildroot}%{_sysconfdir}/init.d/neutron-server

# WRS process monitor configuration files
install -d %{buildroot}%{_sysconfdir}/%{service}/pmon
install -m 755 %{SOURCE44} %{buildroot}%{_sysconfdir}/%{service}/pmon/neutron-dhcp-agent.conf
install -m 755 %{SOURCE45} %{buildroot}%{_sysconfdir}/%{service}/pmon/neutron-metadata-agent.conf
install -m 755 %{SOURCE46} %{buildroot}%{_sysconfdir}/%{service}/pmon/neutron-sriov-nic-agent.conf

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{service}/locale/*/LC_*/%{service}*po
rm -f %{service}/locale/*pot
mv %{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Create fake tempest entrypoint
%py2_entrypoint %{service} %{service}

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Neutron Daemons" %{service}
exit 0


%post
%systemd_post neutron-dhcp-agent.service
%systemd_post neutron-l3-agent.service
%systemd_post neutron-metadata-agent.service
%systemd_post neutron-server.service
%systemd_post neutron-netns-cleanup.service
%systemd_post neutron-ovs-cleanup.service
%systemd_post neutron-linuxbridge-cleanup.service


%preun
%systemd_preun neutron-dhcp-agent.service
%systemd_preun neutron-l3-agent.service
%systemd_preun neutron-metadata-agent.service
%systemd_preun neutron-server.service
%systemd_preun neutron-netns-cleanup.service
%systemd_preun neutron-ovs-cleanup.service
%systemd_preun neutron-linuxbridge-cleanup.service


%postun
%systemd_postun_with_restart neutron-dhcp-agent.service
%systemd_postun_with_restart neutron-l3-agent.service
%systemd_postun_with_restart neutron-metadata-agent.service
%systemd_postun_with_restart neutron-server.service
%cleanup_orphan_rootwrap_daemons


%post macvtap-agent
%systemd_post neutron-macvtap-agent.service


%preun macvtap-agent
%systemd_preun neutron-macvtap-agent.service


%postun macvtap-agent
%systemd_postun_with_restart neutron-macvtap-agent.service
%cleanup_orphan_rootwrap_daemons


%post linuxbridge
%systemd_post neutron-linuxbridge-agent.service


%preun linuxbridge
%systemd_preun neutron-linuxbridge-agent.service


%postun linuxbridge
%systemd_postun_with_restart neutron-linuxbridge-agent.service
%cleanup_orphan_rootwrap_daemons

%post openvswitch
%systemd_post neutron-openvswitch-agent.service

if [ $1 -ge 2 ]; then
    # We're upgrading

    # Detect if the neutron-openvswitch-agent is running
    ovs_agent_running=0
    systemctl status neutron-openvswitch-agent > /dev/null 2>&1 && ovs_agent_running=1 || :

    # If agent is running, stop it
    [ $ovs_agent_running -eq 1 ] && systemctl stop neutron-openvswitch-agent > /dev/null 2>&1 || :

    # Search all orphaned neutron-rootwrap-daemon processes and since all are triggered by sudo,
    # get the actual rootwrap-daemon process.
    %cleanup_orphan_rootwrap_daemons

    # If agent was running, start it back with new code
    [ $ovs_agent_running -eq 1 ] && systemctl start neutron-openvswitch-agent > /dev/null 2>&1 || :
fi


%preun openvswitch
%systemd_preun neutron-openvswitch-agent.service


%post metering-agent
%systemd_post neutron-metering-agent.service


%preun metering-agent
%systemd_preun neutron-metering-agent.service


%postun metering-agent
%systemd_postun_with_restart neutron-metering-agent.service
%cleanup_orphan_rootwrap_daemons


%post sriov-nic-agent
%systemd_post neutron-sriov-nic-agent.service


%preun sriov-nic-agent
%systemd_preun neutron-sriov-nic-agent.service


%postun sriov-nic-agent
%systemd_postun_with_restart neutron-sriov-nic-agent.service
%cleanup_orphan_rootwrap_daemons


%files
%license LICENSE
%{_bindir}/neutron-api
%{_bindir}/neutron-db-manage
%{_bindir}/neutron-debug
%{_bindir}/neutron-dhcp-agent
%{_bindir}/neutron-ipset-cleanup
%{_bindir}/neutron-keepalived-state-change
%{_bindir}/neutron-l3-agent
%{_bindir}/neutron-linuxbridge-cleanup
%{_bindir}/neutron-metadata-agent
%{_bindir}/neutron-netns-cleanup
%{_bindir}/neutron-ovs-cleanup
%{_bindir}/neutron-pd-notify
%{_bindir}/neutron-sanity-check
%{_bindir}/neutron-server
%{_bindir}/neutron-usage-audit
%{_unitdir}/neutron-dhcp-agent.service
%{_unitdir}/neutron-l3-agent.service
%{_unitdir}/neutron-metadata-agent.service
%{_unitdir}/neutron-server.service
%{_unitdir}/neutron-netns-cleanup.service
%{_unitdir}/neutron-ovs-cleanup.service
%{_unitdir}/neutron-linuxbridge-cleanup.service
%attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%dir %{_datadir}/%{service}/l3_agent
%dir %{_datadir}/%{service}/server
%{_datadir}/%{service}/l3_agent/*.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/dhcp_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/l3_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/metadata_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/pmon/neutron-dhcp-agent.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/pmon/neutron-metadata-agent.conf
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-dhcp-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-l3-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-metadata-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-server
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-netns-cleanup
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-ovs-cleanup
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-linuxbridge-cleanup
%{_sysconfdir}/init.d/%{service}-server
%{_sysconfdir}/init.d/%{service}-dhcp-agent
%{_sysconfdir}/init.d/%{service}-metadata-agent


%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests
%{python2_sitelib}/%{service}_tests.egg-info

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common -f %{service}.lang
%license LICENSE
%doc README.rst
# though this script is not exactly needed on all nodes but for ovs and
# linuxbridge agents only, it's probably good enough to put it here
#%{_bindir}/neutron-enable-bridge-firewall.sh
%{_bindir}/neutron-restart
%{_bindir}/neutron-rootwrap
%{_bindir}/neutron-rootwrap-daemon
%{_bindir}/neutron-rootwrap-xen-dom0
%dir %{_sysconfdir}/%{service}
%{_sysconfdir}/%{service}/conf.d/README
%dir %{_sysconfdir}/%{service}/conf.d
%dir %{_sysconfdir}/%{service}/conf.d/common
%dir %{_sysconfdir}/%{service}/plugins
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/%{service}/rootwrap.conf
#%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sudoers.d/%{service}
%dir %attr(0755, %{service}, %{service}) %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, %{service}) %{_localstatedir}/log/%{service}
%dir %{_datarootdir}/%{service}
%dir %{_datarootdir}/%{service}/rootwrap
%{_datarootdir}/%{service}/rootwrap/debug.filters
%{_datarootdir}/%{service}/rootwrap/dhcp.filters
%{_datarootdir}/%{service}/rootwrap/dibbler.filters
%{_datarootdir}/%{service}/rootwrap/ebtables.filters
%{_datarootdir}/%{service}/rootwrap/ipset-firewall.filters
%{_datarootdir}/%{service}/rootwrap/iptables-firewall.filters
%{_datarootdir}/%{service}/rootwrap/l3.filters
%{_datarootdir}/%{service}/rootwrap/netns-cleanup.filters


#%files linuxbridge
#%license LICENSE
%{_bindir}/neutron-linuxbridge-agent
%{_unitdir}/neutron-linuxbridge-agent.service
%{_datarootdir}/%{service}/rootwrap/linuxbridge-plugin.filters
#%dir %{_sysconfdir}/%{service}/plugins/ml2
#%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
#%dir %{_sysconfdir}/%{service}/conf.d/%{service}-linuxbridge-agent
#%{_sysctldir}/99-neutron-linuxbridge-agent.conf
#%{_sysconfdir}/sysconfig/modules/neutron-linuxbridge-agent.modules


%files macvtap-agent
%license LICENSE
%{_bindir}/neutron-macvtap-agent
%{_unitdir}/neutron-macvtap-agent.service
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-macvtap-agent


%files ml2
%license LICENSE
%doc %{service}/plugins/ml2/README
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/*.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/sriov_agent.ini


%files openvswitch
%license LICENSE
%{_bindir}/neutron-openvswitch-agent
%{_unitdir}/neutron-openvswitch-agent.service
%{_datarootdir}/%{service}/rootwrap/openvswitch-plugin.filters
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-openvswitch-agent
#%{_sysctldir}/99-neutron-openvswitch-agent.conf
#%{_sysconfdir}/sysconfig/modules/neutron-openvswitch-agent.modules


%files metering-agent
%license LICENSE
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/metering_agent.ini
%{_unitdir}/neutron-metering-agent.service
%{_bindir}/neutron-metering-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-metering-agent


%files rpc-server
%license LICENSE
%{_bindir}/neutron-rpc-server
%{_unitdir}/neutron-rpc-server.service
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-rpc-server


%files sriov-nic-agent
%license LICENSE
%{_unitdir}/neutron-sriov-nic-agent.service
%{_bindir}/neutron-sriov-nic-agent
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/sriov_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/pmon/neutron-sriov-nic-agent.conf
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-sriov-nic-agent
%{_sysconfdir}/init.d/%{service}-sriov-nic-agent

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*


%changelog
* Mon Sep 25 2017 rdo-trunk <javier.pena@redhat.com> 1:11.0.1-1
- Update to 11.0.1

* Mon Sep  4 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 1:11.0.0-3
- Bump python-pyroute2 (rhbz#1487766)

* Sat Sep 2 2017 Assaf Muller <amuller@redhat.com> 1:11.0.0-2
- Bump python-pyroute2, rhbz 1487766

* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 1:11.0.0-1
- Update to 11.0.0

* Fri Aug 25 2017 rdo-trunk <javier.pena@redhat.com> 1:11.0.0-0.3.0rc3
- Update to 11.0.0.0rc3

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 1:11.0.0-0.2.0rc2
- Update to 11.0.0.0rc2

* Tue Aug 22 2017 Alfredo Moralejo <amoralej@redhat.com> 1:11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

