Summary: openstack-aodh-config
Name: openstack-aodh-config
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: openstack
Packager: StarlingX
URL: unknown
BuildArch: noarch
Source: %name-%version.tar.gz

Requires: openstack-aodh-common
Requires: openstack-aodh-api
Requires: openstack-aodh-evaluator
Requires: openstack-aodh-notifier
Requires: openstack-aodh-expirer
Requires: openstack-aodh-listener

Summary: package StarlingX configuration files of openstack-aodh to system folder.

%description
package StarlingX configuration files of openstack-aodh to system folder.

%prep
%setup

%build

%install
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system
%{__install} -d %{buildroot}%{_bindir}

%{__install} -m 0644 openstack-aodh-api.service        %{buildroot}%{_sysconfdir}/systemd/system/openstack-aodh-api.service
%{__install} -m 0644 openstack-aodh-evaluator.service  %{buildroot}%{_sysconfdir}/systemd/system/openstack-aodh-evaluator.service
%{__install} -m 0644 openstack-aodh-expirer.service    %{buildroot}%{_sysconfdir}/systemd/system/openstack-aodh-expirer.service
%{__install} -m 0644 openstack-aodh-listener.service   %{buildroot}%{_sysconfdir}/systemd/system/openstack-aodh-listener.service
%{__install} -m 0644 openstack-aodh-notifier.service   %{buildroot}%{_sysconfdir}/systemd/system/openstack-aodh-notifier.service
%{__install} -m 0750 aodh-expirer-active               %{buildroot}%{_bindir}/aodh-expirer-active

%post
if test -s %{_sysconfdir}/logrotate.d/openstack-aodh ; then
    echo '#See /etc/logrotate.d/syslog for aodh rules' > %{_sysconfdir}/logrotate.d/openstack-aodh
fi

%files
%{_sysconfdir}/systemd/system/openstack-aodh-api.service
%{_sysconfdir}/systemd/system/openstack-aodh-evaluator.service
%{_sysconfdir}/systemd/system/openstack-aodh-expirer.service
%{_sysconfdir}/systemd/system/openstack-aodh-listener.service
%{_sysconfdir}/systemd/system/openstack-aodh-notifier.service
%{_bindir}/aodh-expirer-active
