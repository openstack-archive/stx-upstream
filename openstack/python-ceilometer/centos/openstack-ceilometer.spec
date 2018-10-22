%global _without_doc 1
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name ceilometer
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:             openstack-ceilometer
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          9.0.1
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          OpenStack measurement collection service

Group:            Applications/System
License:          ASL 2.0
URL:              https://wiki.openstack.org/wiki/Ceilometer
Source0:          %{pypi_name}-%{upstream_version}.tar.gz
Source1:          %{pypi_name}-dist.conf
Source4:          ceilometer-rootwrap-sudoers

Source7:          ceilometer-expirer-active
Source8:          ceilometer-polling
Source9:          ceilometer-polling.conf

Source10:         %{name}-api.service
Source11:         %{name}-collector.service

%if 0%{?with_compute}
Source12:         %{name}-compute.service
%endif
%if 0%{?with_central}
Source13:         %{name}-central.service
%endif

Source16:         %{name}-notification.service
Source17:         %{name}-ipmi.service
Source18:         %{name}-polling.service

Source20:         ceilometer-polling.conf.pmon.centos
Source21:         ceilometer-polling-compute.conf.pmon.centos


BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    openstack-macros
BuildRequires:    python-cotyledon
BuildRequires:    python-sphinx
BuildRequires:    python-setuptools
BuildRequires:    python2-pip
BuildRequires:    python2-wheel
BuildRequires:    python-pbr >= 1.10.0
BuildRequires:    git
BuildRequires:    python-d2to1
BuildRequires:    python2-devel
# Required to compile translation files
BuildRequires:    python-babel
BuildRequires:    systemd-devel
BuildRequires:    systemd
BuildRequires:    systemd-units

%description
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.


%package -n       python-ceilometer
Summary:          OpenStack ceilometer python libraries
Group:            Applications/System

Requires:         python-babel
Requires:         python-cachetools >= 1.1.0
Requires:         python-debtcollector >= 1.2.0
Requires:         python-eventlet
Requires:         python-futurist >= 0.11.0
Requires:         python-cotyledon
Requires:         python-dateutil
Requires:         python-greenlet
Requires:         python-iso8601
Requires:         python-keystoneauth1 >= 2.1.0
Requires:         python-lxml
Requires:         python-anyjson
Requires:         python-jsonpath-rw
Requires:         python-jsonpath-rw-ext
Requires:         python-stevedore >= 1.9.0
Requires:         python-msgpack >= 0.4.0
Requires:         python-pbr
Requires:         python-six >= 1.9.0
Requires:         python-tenacity >= 3.2.1

Requires:         python-sqlalchemy
Requires:         python-alembic
Requires:         python-migrate

Requires:         python-webob
Requires:         python-oslo-config >= 2:3.22.0
Requires:         PyYAML
Requires:         python-netaddr
Requires:         python-oslo-rootwrap
Requires:         python-oslo-vmware >= 0.6.0
Requires:         python-requests >= 2.8.1

Requires:         pysnmp
Requires:         pytz
Requires:         python-croniter

Requires:         python-retrying
Requires:         python-jsonschema
Requires:         python-werkzeug

Requires:         python-oslo-context
Requires:         python-oslo-concurrency >= 3.5.0
Requires:         python-oslo-i18n  >= 2.1.0
Requires:         python-oslo-log  >= 1.14.0
Requires:         python-oslo-middleware >= 3.0.0
Requires:         python-oslo-policy >= 0.5.0
Requires:         python-oslo-reports >= 0.6.0
Requires:         python-monotonic
Requires:         python-futures

%description -n   python-ceilometer
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer python library.


%package common
Summary:          Components common to all OpenStack ceilometer services
Group:            Applications/System

Requires:         python-ceilometer = %{epoch}:%{version}-%{release}
Requires:         python-oslo-messaging >= 5.12.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.5.0
Requires:         python-pecan >= 1.0.0
Requires:         python-posix_ipc
Requires:         python-gnocchiclient
Requires:         python-wsme >= 0.8
Requires:         python-os-xenapi >= 0.1.1

Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires(pre):    shadow-utils

# Config file generation
BuildRequires:    python-os-xenapi
BuildRequires:    python-oslo-config >= 2:3.7.0
BuildRequires:    python-oslo-concurrency
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-log
BuildRequires:    python-oslo-messaging
BuildRequires:    python-oslo-policy
BuildRequires:    python-oslo-reports
BuildRequires:    python-oslo-vmware >= 0.6.0
BuildRequires:    python-glanceclient >= 1:2.0.0
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-neutronclient
BuildRequires:    python-novaclient  >= 1:2.29.0
BuildRequires:    python-swiftclient
BuildRequires:    python-croniter
BuildRequires:    python-jsonpath-rw
BuildRequires:    python-jsonpath-rw-ext
BuildRequires:    python-lxml
BuildRequires:    python-pecan >= 1.0.0
BuildRequires:    python-tooz
BuildRequires:    python-werkzeug
BuildRequires:    python-wsme >= 0.7
BuildRequires:    python-gnocchiclient
BuildRequires:    python-cinderclient >= 1.7.1


%description common
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains components common to all OpenStack
ceilometer services.


%if 0%{?with_compute}
%package compute
Summary:          OpenStack ceilometer compute agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

Requires:         python-novaclient >= 1:2.29.0
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-tooz
Requires:         libvirt-python

%description compute
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer agent for
running on OpenStack compute nodes.

%endif

%if 0%{?with_central}
%package central
Summary:          OpenStack ceilometer central agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

Requires:         python-novaclient >= 1:2.29.0
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-glanceclient >= 1:2.0.0
Requires:         python-swiftclient
Requires:         python-neutronclient >= 4.2.0
Requires:         python-tooz

%description central
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the central ceilometer agent.

%endif

%package collector
Summary:          OpenStack ceilometer collector
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

# For compat with older provisioning tools.
# Remove when all reference the notification package explicitly
Requires:         %{name}-notification

Requires:         python-oslo-db
Requires:         python-pymongo

%description collector
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer collector service
which collects metrics from the various agents.


%package notification
Summary:          OpenStack ceilometer notification agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

%description notification
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer notification agent
which pushes metrics to the collector service from the
various OpenStack services.


%package api
Summary:          OpenStack ceilometer API service
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

Requires:         python-keystonemiddleware >= 4.0.0
Requires:         python-oslo-db >= 4.1.0
Requires:         python-pymongo
Requires:         python-paste-deploy
Requires:         python-tooz

%description api
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ceilometer API service.


%package ipmi
Summary:          OpenStack ceilometer ipmi agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}
Requires:         %{name}-polling = %{epoch}:%{version}-%{release}

Requires:         python-novaclient >= 1:2.29.0
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-neutronclient >= 4.2.0
Requires:         python-tooz
Requires:         python-oslo-rootwrap >= 2.0.0
Requires:         ipmitool

%description ipmi
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the ipmi agent to be run on OpenStack
nodes from which IPMI sensor data is to be collected directly,
by-passing Ironic's management of baremetal.


%package polling
Summary:          OpenStack ceilometer polling agent
Group:            Applications/System

Requires:         %{name}-common = %{epoch}:%{version}-%{release}

Requires:         python-cinderclient >= 1.7.1
Requires:         python-novaclient >= 1:2.29.0
Requires:         python-keystoneclient >= 1:1.6.0
Requires:         python-glanceclient >= 1:2.0.0
Requires:         python-swiftclient >= 2.2.0
Requires:         libvirt-python
Requires:         python-neutronclient
Requires:         python-tooz
Requires:         /usr/bin/systemctl


%description polling
Ceilometer aims to deliver a unique point of contact for billing systems to
acquire all counters they need to establish customer billing, across all
current and future OpenStack components. The delivery of counters must
be tracable and auditable, the counters must be easily extensible to support
new projects, and agents doing data collections should be
independent of the overall system.

This package contains the polling service.

%package -n python-ceilometer-tests
Summary:        Ceilometer tests
Requires:       python-ceilometer = %{epoch}:%{version}-%{release}
Requires:       python-gabbi >= 1.30.0

%description -n python-ceilometer-tests
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains the Ceilometer test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack ceilometer
Group:            Documentation

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
BuildRequires:    python-openstackdocstheme
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate, python-iso8601

%description      doc
OpenStack ceilometer provides services to measure and
collect metrics from OpenStack components.

This package contains documentation files for ceilometer.
%endif

%prep
%autosetup -n ceilometer-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find ceilometer -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# TODO: Have the following handle multi line entries
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=etc/ceilometer/ceilometer-config-generator.conf

export PBR_VERSION=%{version}
%{__python2} setup.py build

# Generate i18n files
export PBR_VERSION=%{version}
%{__python2} setup.py compile_catalog -d build/lib/%{pypi_name}/locale

# Programmatically update defaults in sample config
# which is installed at /etc/ceilometer/ceilometer.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" etc/ceilometer/ceilometer.conf
done < %{SOURCE1}

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Install sql migration cfg and sql files that were not installed by setup.py
install -m 644 ceilometer/storage/sqlalchemy/migrate_repo/migrate.cfg %{buildroot}%{python_sitelib}/ceilometer/storage/sqlalchemy/migrate_repo/migrate.cfg
install -m 644 ceilometer/storage/sqlalchemy/migrate_repo/versions/*.sql %{buildroot}%{python_sitelib}/ceilometer/storage/sqlalchemy/migrate_repo/versions/.

# Install non python files that were not installed by setup.py
install -m 755 -d %{buildroot}%{python_sitelib}/ceilometer/hardware/pollsters/data
install -m 644 ceilometer/hardware/pollsters/data/snmp.yaml %{buildroot}%{python_sitelib}/ceilometer/hardware/pollsters/data/snmp.yaml


# Create fake egg-info for the tempest plugin
# TODO switch to %{service} everywhere as in openstack-example.spec
%global service ceilometer
%py2_entrypoint %{service} %{service}

# docs generation requires everything to be installed first

pushd doc

%if 0%{?with_doc}
export PBR_VERSION=%{version}
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

popd

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer
install -d -m 755 %{buildroot}%{_sharedstatedir}/ceilometer/tmp
install -d -m 750 %{buildroot}%{_localstatedir}/log/ceilometer

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sudoers.d
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -d -m 755 %{buildroot}%{_sysconfdir}/ceilometer/meters.d
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/ceilometer/ceilometer-dist.conf
install -p -D -m 440 %{SOURCE4} %{buildroot}%{_sysconfdir}/sudoers.d/ceilometer
install -p -D -m 640 etc/ceilometer/ceilometer.conf %{buildroot}%{_sysconfdir}/ceilometer/ceilometer.conf
install -p -D -m 640 etc/ceilometer/policy.json %{buildroot}%{_sysconfdir}/ceilometer/policy.json
install -p -D -m 640 ceilometer/pipeline/data/pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/pipeline.yaml
install -p -D -m 640 etc/ceilometer/polling.yaml %{buildroot}%{_sysconfdir}/ceilometer/polling.yaml
install -p -D -m 640 ceilometer/pipeline/data/event_pipeline.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_pipeline.yaml
install -p -D -m 640 ceilometer/pipeline/data/event_definitions.yaml %{buildroot}%{_sysconfdir}/ceilometer/event_definitions.yaml
install -p -D -m 640 etc/ceilometer/api_paste.ini %{buildroot}%{_sysconfdir}/ceilometer/api_paste.ini
install -p -D -m 640 etc/ceilometer/rootwrap.conf %{buildroot}%{_sysconfdir}/ceilometer/rootwrap.conf
install -p -D -m 640 etc/ceilometer/rootwrap.d/ipmi.filters %{buildroot}/%{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters
install -p -D -m 640 ceilometer/publisher/data/gnocchi_resources.yaml %{buildroot}%{_sysconfdir}/ceilometer/gnocchi_resources.yaml
install -p -D -m 640 ceilometer/data/meters.d/meters.yaml %{buildroot}%{_sysconfdir}/ceilometer/meters.d/meters.yaml
install -p -D -m 640 ceilometer/api/ceilometer-api.py %{buildroot}%{_datadir}/ceilometer/ceilometer-api.py



# Install initscripts for services
%if 0%{?rhel} && 0%{?rhel} <= 6
install -p -D -m 755 %{SOURCE10} %{buildroot}%{_initrddir}/%{name}-api
install -p -D -m 755 %{SOURCE11} %{buildroot}%{_initrddir}/%{name}-collector
%if 0%{?with_compute}
install -p -D -m 755 %{SOURCE12} %{buildroot}%{_initrddir}/%{name}-compute
%endif
%if 0%{?with_central}
install -p -D -m 755 %{SOURCE13} %{buildroot}%{_initrddir}/%{name}-central
%endif
install -p -D -m 755 %{SOURCE16} %{buildroot}%{_initrddir}/%{name}-notification
install -p -D -m 755 %{SOURCE17} %{buildroot}%{_initrddir}/%{name}-ipmi
install -p -D -m 755 %{SOURCE18} %{buildroot}%{_initrddir}/%{name}-polling

# Install upstart jobs examples
install -d -m 755 %{buildroot}%{_datadir}/ceilometer
install -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE110} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE120} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE130} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE140} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE150} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE160} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE170} %{buildroot}%{_datadir}/ceilometer/
install -p -m 644 %{SOURCE180} %{buildroot}%{_datadir}/ceilometer/
%else
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-collector.service
%if 0%{?with_compute}
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-compute.service
%endif
%if 0%{?with_central}
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/%{name}-central.service
%endif
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/%{name}-notification.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/%{name}-ipmi.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/%{name}-polling.service
%endif

install -p -D -m 755 %{SOURCE7} %{buildroot}%{_bindir}/ceilometer-expirer-active
install -p -D -m 755 %{SOURCE8} %{buildroot}%{_initrddir}/openstack-ceilometer-polling

mkdir -p %{buildroot}/%{_sysconfdir}/ceilometer
install -p -D -m 644 %{SOURCE9}  %{buildroot}%{_sysconfdir}/ceilometer/ceilometer-polling.conf
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/ceilometer/ceilometer-polling.conf.pmon
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/ceilometer/ceilometer-polling-compute.conf.pmon

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*/LC_*/%{pypi_name}*po
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{pypi_name}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{pypi_name} --all-name

# Remove unneeded in production stuff
rm -f %{buildroot}/usr/share/doc/ceilometer/README*

# Remove unused files
rm -fr %{buildroot}/usr/etc

%pre common
getent group ceilometer >/dev/null || groupadd -r ceilometer --gid 166
if ! getent passwd ceilometer >/dev/null; then
  # Id reservation request: https://bugzilla.redhat.com/923891
  useradd -u 166 -r -g ceilometer -G ceilometer,nobody -d %{_sharedstatedir}/ceilometer -s /sbin/nologin -c "OpenStack ceilometer Daemons" ceilometer
fi
exit 0


%if 0%{?with_compute}
%post compute
%systemd_post %{name}-compute.service
%endif

%post collector
%systemd_post %{name}-collector.service

%post notification
%systemd_post %{name}-notification.service

%post api
%systemd_post %{name}-api.service

%if 0%{?with_central}
%post central
%systemd_post %{name}-central.service
%endif

%post ipmi
%systemd_post %{name}-alarm-ipmi.service

%post polling
/usr/bin/systemctl disable %{name}-polling.service

%if 0%{?with_compute}
%preun compute
%systemd_preun %{name}-compute.service
%endif

%preun collector
%systemd_preun %{name}-collector.service

%preun notification
%systemd_preun %{name}-notification.service

%preun api
%systemd_preun %{name}-api.service

%if 0%{?with_central}
%preun central
%systemd_preun %{name}-central.service
%endif

%preun ipmi
%systemd_preun %{name}-ipmi.service

%preun polling
%systemd_preun %{name}-polling.service

%if 0%{?with_compute}
%postun compute
%systemd_postun_with_restart %{name}-compute.service
%endif

%postun collector
%systemd_postun_with_restart %{name}-collector.service

%postun notification
%systemd_postun_with_restart %{name}-notification.service

%postun api
%systemd_postun_with_restart %{name}-api.service

%if 0%{?with_central}
%postun central
%systemd_postun_with_restart %{name}-central.service
%endif

%postun ipmi
%systemd_postun_with_restart %{name}-ipmi.service


%postun polling
/usr/bin/systemctl disable %{name}-polling.service


%files common -f %{pypi_name}.lang
%license LICENSE
%dir %{_sysconfdir}/ceilometer
%{_datadir}/ceilometer/ceilometer-api.*
%attr(-, root, ceilometer) %{_datadir}/ceilometer/ceilometer-dist.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/ceilometer.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/policy.json
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/polling.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/api_paste.ini
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/gnocchi_resources.yaml

%dir %attr(0750, ceilometer, root) %{_localstatedir}/log/ceilometer

%{_bindir}/ceilometer-db-legacy-clean
%{_bindir}/ceilometer-expirer
%{_bindir}/ceilometer-send-sample
%{_bindir}/ceilometer-upgrade

%defattr(-, ceilometer, ceilometer, -)
%dir %{_sharedstatedir}/ceilometer
%dir %{_sharedstatedir}/ceilometer/tmp


%files -n python-ceilometer
%{python2_sitelib}/ceilometer
%{python2_sitelib}/ceilometer-*.egg-info
%exclude %{python2_sitelib}/ceilometer/tests

%files -n python-ceilometer-tests
%license LICENSE
%{python2_sitelib}/ceilometer/tests
%{python2_sitelib}/%{service}_tests.egg-info

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%if 0%{?with_compute}
%files compute
%{_unitdir}/%{name}-compute.service
%endif


%files collector
%{_bindir}/ceilometer-collector*
%{_bindir}/ceilometer-expirer-active
%{_unitdir}/%{name}-collector.service


%files notification
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_pipeline.yaml
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/event_definitions.yaml
%dir %{_sysconfdir}/ceilometer/meters.d
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/meters.d/meters.yaml
%{_bindir}/ceilometer-agent-notification
%{_unitdir}/%{name}-notification.service


%files api
%{_bindir}/ceilometer-api
%{_unitdir}/%{name}-api.service


%if 0%{?with_central}
%files central
%{_unitdir}/%{name}-central.service
%endif


%files ipmi
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.conf
%config(noreplace) %attr(-, root, ceilometer) %{_sysconfdir}/ceilometer/rootwrap.d/ipmi.filters
%{_bindir}/ceilometer-rootwrap
%{_sysconfdir}/sudoers.d/ceilometer
%{_unitdir}/%{name}-ipmi.service

%files polling
%{_bindir}/ceilometer-polling
%{_initrddir}/openstack-ceilometer-polling
%{_sysconfdir}/ceilometer/ceilometer-polling.conf
%{_sysconfdir}/ceilometer/ceilometer-polling.conf.pmon
%{_sysconfdir}/ceilometer/ceilometer-polling-compute.conf.pmon
%{_unitdir}/%{name}-polling.service

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Tue Sep 12 2017 rdo-trunk <javier.pena@redhat.com> 1:9.0.1-1
- Update to 9.0.1

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 1:9.0.0-1
- Update to 9.0.0

