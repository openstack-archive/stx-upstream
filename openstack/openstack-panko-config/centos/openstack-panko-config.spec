Summary: openstack-panko-config
Name: openstack-panko-config
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: openstack
Packager: StarlingX
URL: unknown
BuildArch: noarch
Source: %name-%version.tar.gz

Requires: openstack-panko-common
Requires: openstack-panko-api

Summary: package StarlingX configuration files of openstack-panko to system folder.

%description
package StarlingX configuration files of openstack-panko to system folder.

%prep
%setup

%build

%install
%{__install} -d %{buildroot}%{_bindir}
%{__install} -m 0755  panko-expirer-active   %{buildroot}%{_bindir}/panko-expirer-active

%post
if test -s %{_sysconfdir}/logrotate.d/openstack-panko ; then
    echo '#See /etc/logrotate.d/syslog for panko rules' > %{_sysconfdir}/logrotate.d/openstack-panko
fi

%files
%{_bindir}/panko-expirer-active
