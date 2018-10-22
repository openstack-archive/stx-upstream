%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service magnum

Name:		openstack-%{service}
Summary:	Container Management project for OpenStack
Version:	5.0.1
Release:	1%{?_tis_dist}.%{tis_patch_ver}
License:	ASL 2.0
URL:		https://github.com/openstack/magnum.git

Source0:	https://tarballs.openstack.org/%{service}/%{service}-%{version}.tar.gz

Source2:	%{name}-api.service
Source3:	%{name}-conductor.service

BuildArch: noarch

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-pbr
BuildRequires: python-setuptools
BuildRequires: python2-pip
BuildRequires: python2-wheel
BuildRequires: python-werkzeug
BuildRequires: systemd-units
# Required for config file generation
BuildRequires: python-pycadf
BuildRequires: python-osprofiler

Requires: %{name}-common = %{version}-%{release}
Requires: %{name}-conductor = %{version}-%{release}
Requires: %{name}-api = %{version}-%{release}

%description
Magnum is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%package -n python-%{service}
Summary: Magnum Python libraries

Requires: python-pbr
Requires: python-babel
Requires: PyYAML
Requires: python-sqlalchemy
Requires: python-wsme
Requires: python-webob
Requires: python-alembic
Requires: python-decorator
Requires: python-docker >= 2.0.0
Requires: python-enum34
Requires: python-eventlet
Requires: python-iso8601
Requires: python-jsonpatch
Requires: python-keystonemiddleware >= 4.12.0
Requires: python-netaddr

Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-context >= 2.14.0
Requires: python-oslo-db >= 4.24.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-log >= 3.22.0
Requires: python-oslo-messaging >= 5.24.2
Requires: python-oslo-middleware >= 3.27.0
Requires: python-oslo-policy >= 1.23.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-oslo-versionedobjects >= 1.17.0
Requires: python-oslo-reports >= 0.6.0
Requires: python-osprofiler

Requires: python-pycadf
Requires: python-pecan

Requires: python-barbicanclient >= 4.0.0
Requires: python-glanceclient >= 1:2.8.0
Requires: python-heatclient >= 1.6.1
Requires: python-neutronclient >= 6.3.0
Requires: python-novaclient >= 1:9.0.0
Requires: python-kubernetes
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-keystoneauth1 >= 3.1.0

Requires: python-cliff >= 2.8.0
Requires: python-requests
Requires: python-six
Requires: python-stevedore >= 1.20.0
Requires: python-taskflow
Requires: python-cryptography
Requires: python-werkzeug
Requires: python-marathon


%description -n python-%{service}
Magnum is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%package common
Summary: Magnum common

Requires: python-%{service} = %{version}-%{release}

Requires(pre): shadow-utils

%description common
Components common to all OpenStack Magnum services

%package conductor
Summary: The Magnum conductor

Requires: %{name}-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description conductor
OpenStack Magnum Conductor

%package api
Summary: The Magnum API

Requires: %{name}-common = %{version}-%{release}

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description api
OpenStack-native ReST API to the Magnum Engine

%if 0%{?with_doc}
%package -n %{name}-doc
Summary:    Documentation for OpenStack Magnum

Requires:    python-%{service} = %{version}-%{release}

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-stevedore
BuildRequires:  graphviz

%description -n %{name}-doc
Magnum is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

This package contains documentation files for Magnum.
%endif

# tests
%package -n python-%{service}-tests
Summary:          Tests for OpenStack Magnum

Requires:        python-%{service} = %{version}-%{release}

BuildRequires:   python-fixtures
BuildRequires:   python-hacking
BuildRequires:   python-mock
BuildRequires:   python-oslotest
BuildRequires:   python-os-testr
BuildRequires:   python-subunit
BuildRequires:   python-testrepository
BuildRequires:   python-testscenarios
BuildRequires:   python-testtools
BuildRequires:   python-tempest
BuildRequires:   openstack-macros

# copy-paste from runtime Requires
BuildRequires: python-babel
BuildRequires: PyYAML
BuildRequires: python-sqlalchemy
BuildRequires: python-wsme
BuildRequires: python-webob
BuildRequires: python-alembic
BuildRequires: python-decorator
BuildRequires: python-docker >= 2.0.0
BuildRequires: python-enum34
BuildRequires: python-eventlet
BuildRequires: python-iso8601
BuildRequires: python-jsonpatch
BuildRequires: python-keystonemiddleware
BuildRequires: python-netaddr

BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config
BuildRequires: python-oslo-context
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-messaging
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-service
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-versionedobjects
BuildRequires: python2-oslo-versionedobjects-tests
BuildRequires: python-oslo-reports

BuildRequires: python-pecan

BuildRequires: python-barbicanclient
BuildRequires: python-glanceclient
BuildRequires: python-heatclient
BuildRequires: python-neutronclient
BuildRequires: python-novaclient
BuildRequires: python-kubernetes
BuildRequires: python-keystoneclient

BuildRequires: python-requests
BuildRequires: python-six
BuildRequires: python-stevedore
BuildRequires: python-taskflow
BuildRequires: python-cryptography
BuildRequires: python-marathon

%description -n python-%{service}-tests
Magnum is an OpenStack project which offers container orchestration engines
for deploying and managing containers as first class resources in OpenStack.

%prep
%autosetup -n %{service}-%{upstream_version} -S git

# Let's handle dependencies ourselves
rm -rf {test-,}requirements{-bandit,}.txt tools/{pip,test}-requires

# Remove tests in contrib
find contrib -name tests -type d | xargs rm -rf

%build
export PBR_VERSION=%{version}
%{__python2} setup.py build
%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create fake egg-info for the tempest plugin
%py2_entrypoint %{service} %{service}

# docs generation requires everything to be installed first
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

mkdir -p %{buildroot}%{_localstatedir}/log/%{service}/
mkdir -p %{buildroot}%{_localstatedir}/run/%{service}/

# install systemd unit files
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-conductor.service

mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/
mkdir -p %{buildroot}%{_sharedstatedir}/%{service}/certificates/
mkdir -p %{buildroot}%{_sysconfdir}/%{service}/

oslo-config-generator --config-file etc/magnum/magnum-config-generator.conf --output-file %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/magnum.conf
install -p -D -m 640 etc/magnum/policy.json %{buildroot}%{_sysconfdir}/%{service}
install -p -D -m 640 etc/magnum/api-paste.ini %{buildroot}%{_sysconfdir}/%{service}

%check
%{__python2} setup.py test || true

%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common
%{_bindir}/magnum-db-manage
%{_bindir}/magnum-driver-manage
%license LICENSE
%dir %attr(0750,%{service},root) %{_localstatedir}/log/%{service}
%dir %attr(0755,%{service},root) %{_localstatedir}/run/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}
%dir %attr(0755,%{service},root) %{_sharedstatedir}/%{service}/certificates
%dir %attr(0755,%{service},root) %{_sysconfdir}/%{service}
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/magnum.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%pre common
# 1870:1870 for magnum - rhbz#845078
getent group %{service} >/dev/null || groupadd -r --gid 1870 %{service}
getent passwd %{service}  >/dev/null || \
useradd --uid 1870 -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
-c "OpenStack Magnum Daemons" %{service}
exit 0


%files conductor
%doc README.rst
%license LICENSE
%{_bindir}/magnum-conductor
%{_unitdir}/%{name}-conductor.service


%files api
%doc README.rst
%license LICENSE
%{_bindir}/magnum-api
%{_unitdir}/%{name}-api.service


%if 0%{?with_doc}
%files -n %{name}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests
%{python2_sitelib}/%{service}_tests.egg-info

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Mon Aug 28 2017 rdo-trunk <javier.pena@redhat.com> 5.0.1-1
- Update to 5.0.1

* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-1
- Update to 5.0.0
