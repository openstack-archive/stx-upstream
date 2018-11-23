Summary: rabbitmq-server-config
Name: rabbitmq-server-config
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: StarlingX
URL: unknown
BuildArch: noarch
Source: %name-%version.tar.gz

BuildRequires: rabbitmq-server = 3.6.5-1.el7
Requires: %{_bindir}/systemctl
Requires: rabbitmq-server
Summary: package StarlingX configuration files of rabbitmq-server to system folder.

%description
package StarlingX configuration files of rabbitmq-server to system folder.

%prep
%setup

%build

%install
%{__install} -d %{buildroot}%{_datadir}/starlingx
%{__install} -d %{buildroot}%{_sysconfdir}/systemd/system

%{__install} -m 0755 rabbitmq-server.ocf              %{buildroot}%{_datadir}/starlingx/stx.rabbitmq-server
%{__install} -m 0644 rabbitmq-server.service.example  %{buildroot}%{_sysconfdir}/systemd/system/rabbitmq-server.service
%{__install} -m 0755 rabbitmq-script-wrapper          %{buildroot}%{_datadir}/starlingx/stx.rabbitmq-script-wrapper
%{__install} -m 0644 rabbitmq-server.logrotate        %{buildroot}%{_datadir}/starlingx/stx.rabbitmq-server.logrotate 

%post
if [ $1 -eq 1 ] ; then
        # Initial installation
        cp -f %{_datadir}/starlingx/stx.rabbitmq-server           %{_exec_prefix}/lib/ocf/resource.d/rabbitmq/rabbitmq-server 
        cp -f %{_datadir}/starlingx/stx.rabbitmq-script-wrapper   %{_sbindir}/rabbitmqctl
        cp -f %{_datadir}/starlingx/stx.rabbitmq-script-wrapper   %{_sbindir}/rabbitmq-server
        cp -f %{_datadir}/starlingx/stx.rabbitmq-script-wrapper   %{_sbindir}/rabbitmq-plugins
        cp -f %{_datadir}/starlingx/stx.rabbitmq-server.logrotate %{_sysconfdir}/logrotate.d/rabbitmq-server
fi
%{_bindir}/systemctl disable rabbitmq-server.service  > /dev/null 2>&1 || :

%files
%{_datadir}/starlingx/stx.rabbitmq-server
%{_sysconfdir}/systemd/system/rabbitmq-server.service
%{_datadir}/starlingx/stx.rabbitmq-script-wrapper
%{_datadir}/starlingx/stx.rabbitmq-server.logrotate
