%global full_release ironic-%{version}

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-ironic
# Liberty semver reset
# https://review.openstack.org/#/q/I1a161b2c1d1e27268065b6b4be24c8f7a5315afb,n,z
Epoch:          1
Summary:        OpenStack Baremetal Hypervisor API (ironic)
Version:        9.1.2
Release:        0%{?_tis_dist}.%{tis_patch_ver}
License:        ASL 2.0
URL:            http://www.openstack.org
Source0:        https://tarballs.openstack.org/ironic/ironic-%{version}.tar.gz

Source1:        openstack-ironic-api.service
Source2:        openstack-ironic-conductor.service
Source3:        ironic-rootwrap-sudoers
Source4:        ironic-dist.conf

BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  python-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  openssl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  gmp-devel
BuildRequires:  python-sphinx
BuildRequires:  systemd
# Required to compile translation files
BuildRequires:  python-babel
# Required to run unit tests
BuildRequires:  pysendfile
BuildRequires:  python-alembic
BuildRequires:  python-automaton
BuildRequires:  python-cinderclient
BuildRequires:  python-dracclient
BuildRequires:  python-eventlet
BuildRequires:  python-futurist
BuildRequires:  python-glanceclient
BuildRequires:  python-ironic-inspector-client
BuildRequires:  python-ironic-lib
BuildRequires:  python-jinja2
BuildRequires:  python-jsonpatch
BuildRequires:  python-jsonschema
BuildRequires:  python-keystoneauth1
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-mock
BuildRequires:  python-neutronclient
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-context
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-db-tests
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-reports
BuildRequires:  python-oslo-rootwrap
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  python-oslotest
BuildRequires:  python-osprofiler
BuildRequires:  python-os-testr
BuildRequires:  python-pbr
BuildRequires:  python-pecan
BuildRequires:  python-proliantutils
BuildRequires:  python-psutil
BuildRequires:  python-requests
BuildRequires:  python-retrying
BuildRequires:  python-scciclient
BuildRequires:  python-six
BuildRequires:  python-sqlalchemy
BuildRequires:  python-stevedore
BuildRequires:  python-sushy
BuildRequires:  python-swiftclient
BuildRequires:  python-testresources
BuildRequires:  python-tooz
BuildRequires:  python-UcsSdk
BuildRequires:  python-webob
BuildRequires:  python-wsme
BuildRequires:  pysnmp
BuildRequires:  pytz

%prep
%setup -q -n ironic-%{upstream_version}
rm requirements.txt test-requirements.txt

%build
export PBR_VERSION=%{version}
%{__python2} setup.py build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/ironic/locale
%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create fake egg-info for the tempest plugin
# TODO switch to %{service} everywhere as in openstack-example.spec
%global service ironic
%py2_entrypoint %{service} %{service}


# install systemd scripts
mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}

# install sudoers file
mkdir -p %{buildroot}%{_sysconfdir}/sudoers.d
install -p -D -m 440 %{SOURCE3} %{buildroot}%{_sysconfdir}/sudoers.d/ironic

mkdir -p %{buildroot}%{_sharedstatedir}/ironic/
mkdir -p %{buildroot}%{_localstatedir}/log/ironic/
mkdir -p %{buildroot}%{_sysconfdir}/ironic/rootwrap.d

#Populate the conf dir
install -p -D -m 640 etc/ironic/ironic.conf.sample %{buildroot}/%{_sysconfdir}/ironic/ironic.conf
install -p -D -m 640 etc/ironic/policy.json %{buildroot}/%{_sysconfdir}/ironic/policy.json
install -p -D -m 640 etc/ironic/rootwrap.conf %{buildroot}/%{_sysconfdir}/ironic/rootwrap.conf
install -p -D -m 640 etc/ironic/rootwrap.d/* %{buildroot}/%{_sysconfdir}/ironic/rootwrap.d/

# Install distribution config
install -p -D -m 640 %{SOURCE4} %{buildroot}/%{_datadir}/ironic/ironic-dist.conf

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/ironic/locale/*/LC_*/ironic*po
rm -f %{buildroot}%{python2_sitelib}/ironic/locale/*pot
mv %{buildroot}%{python2_sitelib}/ironic/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang ironic --all-name


%description
Ironic provides an API for management and provisioning of physical machines

%package common
Summary: Ironic common

Requires:   ipmitool
Requires:   pysendfile
Requires:   python-alembic
Requires:   python-automaton >= 0.5.0
Requires:   python-cinderclient >= 3.1.0
Requires:   python-dracclient >= 1.3.0
Requires:   python-eventlet
Requires:   python-futurist >= 0.11.0
Requires:   python-glanceclient >= 1:2.7.0
Requires:   python-ironic-inspector-client >= 1.5.0
Requires:   python-ironic-lib >= 2.5.0
Requires:   python-jinja2
Requires:   python-jsonpatch
Requires:   python-jsonschema
Requires:   python-keystoneauth1 >= 3.1.0
Requires:   python-keystonemiddleware >= 4.12.0
Requires:   python-neutronclient >= 6.3.0
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-context >= 2.14.0
Requires:   python-oslo-db >= 4.24.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-messaging >= 5.24.2
Requires:   python-oslo-middleware >= 3.27.0
Requires:   python-oslo-policy >= 1.23.0
Requires:   python-oslo-reports >= 0.6.0
Requires:   python-oslo-rootwrap >= 5.0.0
Requires:   python-oslo-serialization >= 1.10.0
Requires:   python-oslo-service >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-oslo-versionedobjects >= 1.17.0
Requires:   python-osprofiler >= 1.4.0
Requires:   python-pbr
Requires:   python-pecan
Requires:   python-proliantutils >= 2.4.0
Requires:   python-psutil
Requires:   python-requests
Requires:   python-retrying
Requires:   python-rfc3986 >= 0.3.1
Requires:   python-scciclient >= 0.5.0
Requires:   python-six
Requires:   python-sqlalchemy
Requires:   python-stevedore >= 1.20.0
Requires:   python-sushy
Requires:   python-swiftclient >= 3.2.0
Requires:   python-tooz >= 1.47.0
Requires:   python-UcsSdk >= 0.8.2.2
Requires:   python-webob >= 1.7.1
Requires:   python-wsme
Requires:   pysnmp
Requires:   pytz


Requires(pre):  shadow-utils

%description common
Components common to all OpenStack Ironic services


%files common -f ironic.lang
%doc README.rst
%license LICENSE
%{_bindir}/ironic-dbsync
%{_bindir}/ironic-rootwrap
%{python2_sitelib}/ironic
%{python2_sitelib}/ironic-*.egg-info
%exclude %{python2_sitelib}/ironic/tests
%exclude %{python2_sitelib}/ironic_tempest_plugin
%{_sysconfdir}/sudoers.d/ironic
%config(noreplace) %attr(-,root,ironic) %{_sysconfdir}/ironic
%attr(-,ironic,ironic) %{_sharedstatedir}/ironic
%attr(0755,ironic,ironic) %{_localstatedir}/log/ironic
%attr(-, root, ironic) %{_datadir}/ironic/ironic-dist.conf
%exclude %{python2_sitelib}/ironic_tests.egg_info

%package api
Summary: The Ironic API

Requires: %{name}-common = %{epoch}:%{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description api
Ironic API for management and provisioning of physical machines


%files api
%{_bindir}/ironic-api
%{_unitdir}/openstack-ironic-api.service

%package conductor
Summary: The Ironic Conductor

Requires: %{name}-common = %{epoch}:%{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description conductor
Ironic Conductor for management and provisioning of physical machines

%files conductor
%{_bindir}/ironic-conductor
%{_unitdir}/openstack-ironic-conductor.service


%package -n python-ironic-tests
Summary:        Ironic tests
Requires:       %{name}-common = %{epoch}:%{version}-%{release}
Requires:       python-mock
Requires:       python-oslotest
Requires:       python-os-testr
Requires:       python-testresources

%description -n python-ironic-tests
This package contains the Ironic test files.

%files -n python-ironic-tests
%{python2_sitelib}/ironic/tests
%{python2_sitelib}/ironic_tempest_plugin
%{python2_sitelib}/%{service}_tests.egg-info

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Fri Nov 03 2017 RDO <dev@lists.rdoproject.org> 1:9.1.2-1
- Update to 9.1.2

* Mon Sep 25 2017 rdo-trunk <javier.pena@redhat.com> 1:9.1.1-1
- Update to 9.1.1

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 1:9.1.0-1
- Update to 9.1.0
