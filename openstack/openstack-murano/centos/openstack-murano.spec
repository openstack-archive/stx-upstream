%global pypi_name murano

%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

Name:          openstack-%{pypi_name}
Version:       4.0.0
Release:       1%{?_tis_dist}.%{tis_patch_ver}
Summary:       OpenStack Murano Service

License:       ASL 2.0
URL:           https://pypi.python.org/pypi/murano
Source0:       https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
#

Source1:       openstack-murano-api.service
Source2:       openstack-murano-engine.service
Source4:       openstack-murano-cf-api.service

BuildArch:     noarch

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python2-pip
BuildRequires: python2-wheel
BuildRequires: python-jsonschema >= 2.0.0
BuildRequires: python-keystonemiddleware
BuildRequires: python-oslo-config
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-messaging
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-service
BuildRequires: python-openstackdocstheme
BuildRequires: python-pbr >= 2.0.0
BuildRequires: python-routes >= 2.3.1
BuildRequires: python-sphinx
BuildRequires: python-sphinxcontrib-httpdomain
BuildRequires: python-castellan
BuildRequires: pyOpenSSL
BuildRequires: systemd
BuildRequires: openstack-macros
# Required to compile translation files
BuildRequires: python-babel

%description
Murano Project introduces an application catalog service

# MURANO-COMMON
%package common
Summary: Murano common
Requires:      python-alembic >= 0.8.7
Requires:      python-babel >= 2.3.4
Requires:      python-debtcollector >= 1.2.0
Requires:      python-eventlet >= 0.18.2
Requires:      python-iso8601 >= 0.1.9
Requires:      python-jsonpatch >= 1.1
Requires:      python-jsonschema >= 2.0.0
Requires:      python-keystonemiddleware >= 4.12.0
Requires:      python-keystoneauth1 >= 3.1.0
Requires:      python-kombu >= 1:4.0.0
Requires:      python-netaddr >= 0.7.13
Requires:      python-oslo-concurrency >= 3.8.0
Requires:      python-oslo-config >= 2:4.0.0
Requires:      python-oslo-context >= 2.14.0
Requires:      python-oslo-db >= 4.24.0
Requires:      python-oslo-i18n >= 2.1.0
Requires:      python-oslo-log >= 3.22.0
Requires:      python-oslo-messaging >= 5.24.2
Requires:      python-oslo-middleware >= 3.27.0
Requires:      python-oslo-policy >= 1.23.0
Requires:      python-oslo-serialization >= 1.10.0
Requires:      python-oslo-service >= 1.10.0
Requires:      python-oslo-utils >= 3.20.0
Requires:      python-paste
Requires:      python-paste-deploy >= 1.5.0
Requires:      python-pbr >= 2.0.0
Requires:      python-psutil >= 3.2.2
Requires:      python-congressclient >= 1.3.0
Requires:      python-heatclient >= 1.6.1
Requires:      python-keystoneclient >= 1:3.8.0
Requires:      python-mistralclient >= 3.1.0
Requires:      python-muranoclient >= 0.8.2
Requires:      python-neutronclient >= 6.3.0
Requires:      PyYAML >= 3.10
Requires:      python-routes >= 2.3.1
Requires:      python-semantic_version >= 2.3.1
Requires:      python-six >= 1.9.0
Requires:      python-stevedore >= 1.20.0
Requires:      python-sqlalchemy >= 1.0.10
Requires:      python-tenacity >= 3.2.1
Requires:      python-webob >= 1.7.1
Requires:      python-yaql >= 1.1.0
Requires:      python-castellan >= 0.7.0
Requires:      %{name}-doc = %{version}-%{release}

%description common
Components common to all OpenStack Murano services

# MURANO-ENGINE
%package engine
Summary: The Murano engine
Group:   Applications/System
Requires: %{name}-common = %{version}-%{release}

%description engine
OpenStack Murano Engine daemon

# MURANO-API
%package api
Summary: The Murano API
Group:   Applications/System
Requires: %{name}-common = %{version}-%{release}

%description api
OpenStack rest API to the Murano Engine

# MURANO-CF-API
%package cf-api
Summary: The Murano Cloud Foundry API
Group: System Environment/Base
Requires: %{name}-common = %{version}-%{release}

%description cf-api
OpenStack rest API for Murano to the Cloud Foundry

%if 0%{?with_doc}
%package doc
Summary: Documentation for OpenStack Murano services

%description doc
This package contains documentation files for Murano.
%endif

%package -n python-murano-tests
Summary:        Murano tests
Requires:       %{name}-common = %{version}-%{release}

%description -n python-murano-tests
This package contains the murano test files.

%prep
%autosetup -S git -n %{pypi_name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export PBR_VERSION=%{version}
%{__python2} setup.py build
# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{pypi_name}/locale
# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip heat's entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/oslo-config-generator/murano.conf
PYTHONPATH=. oslo-config-generator --config-file=./etc/oslo-config-generator/murano-cfapi.conf
%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create fake egg-info for the tempest plugin
# TODO switch to %{service} everywhere as in openstack-example.spec
%global service murano
%py2_entrypoint %{service} %{service}

# DOCs

pushd doc

%if 0%{?with_doc}
SPHINX_DEBUG=1 sphinx-build -b html source build/html
# Fix hidden-file-or-dir warnings
rm -fr build/html/.doctrees build/html/.buildinfo
%endif

popd

mkdir -p %{buildroot}/var/log/murano
mkdir -p %{buildroot}/var/run/murano
mkdir -p %{buildroot}/var/cache/murano/meta
mkdir -p %{buildroot}/etc/murano/
# install systemd unit files
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/murano-api.service
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/murano-engine.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/murano-cf-api.service
# install default config files
cd %{_builddir}/%{pypi_name}-%{upstream_version} && oslo-config-generator --config-file ./etc/oslo-config-generator/murano.conf --output-file %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/murano.conf.sample
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/murano.conf.sample %{buildroot}%{_sysconfdir}/murano/murano.conf
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/netconfig.yaml.sample %{buildroot}%{_sysconfdir}/murano/netconfig.yaml.sample
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/murano-paste.ini %{buildroot}%{_sysconfdir}/murano/murano-paste.ini
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/logging.conf.sample %{buildroot}%{_sysconfdir}/murano/logging.conf
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/murano-cfapi.conf.sample %{buildroot}%{_sysconfdir}/murano/murano-cfapi.conf
install -p -D -m 640 %{_builddir}/%{pypi_name}-%{upstream_version}/etc/murano/murano-cfapi-paste.ini %{buildroot}%{_sysconfdir}/murano/murano-cfapi-paste.ini

# Creating murano core library archive(murano meta packages written in muranoPL with execution plan main minimal logic)
pushd meta/io.murano
zip -r %{buildroot}%{_localstatedir}/cache/murano/meta/io.murano.zip .
popd
# Creating murano core library archive(murano meta packages written in muranoPL with execution plan main minimal logic)
pushd meta/io.murano.applications
zip -r %{buildroot}%{_localstatedir}/cache/murano/meta/io.murano.applications.zip .
popd
# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*/LC_*/%{pypi_name}*po
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{pypi_name}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{pypi_name} --all-name

%files common -f %{pypi_name}.lang
%license LICENSE
%{python2_sitelib}/murano
%{python2_sitelib}/murano-*.egg-info
%exclude %{python2_sitelib}/murano/tests
%exclude %{python2_sitelib}/murano_tempest_tests
%exclude %{python2_sitelib}/%{service}_tests.egg-info
%{_bindir}/murano-manage
%{_bindir}/murano-db-manage
%{_bindir}/murano-test-runner
%{_bindir}/murano-cfapi-db-manage
%dir %attr(0750,murano,root) %{_localstatedir}/log/murano
%dir %attr(0755,murano,root) %{_localstatedir}/run/murano
%dir %attr(0755,murano,root) %{_localstatedir}/cache/murano
%dir %attr(0755,murano,root) %{_sysconfdir}/murano
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano.conf
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano-paste.ini
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/netconfig.yaml.sample
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/logging.conf
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano-cfapi.conf
%config(noreplace) %attr(-, root, murano) %{_sysconfdir}/murano/murano-cfapi-paste.ini

%files engine
%doc README.rst
%license LICENSE
%{_bindir}/murano-engine
%{_unitdir}/murano-engine.service

%post engine
%systemd_post murano-engine.service

%preun engine
%systemd_preun murano-engine.service

%postun engine
%systemd_postun_with_restart murano-engine.service

%files api
%doc README.rst
%license LICENSE
%{_localstatedir}/cache/murano/*
%{_bindir}/murano-api
%{_bindir}/murano-wsgi-api
%{_unitdir}/murano-api.service

%files cf-api
%doc README.rst
%license LICENSE
%{_bindir}/murano-cfapi
%{_unitdir}/murano-cf-api.service

%files doc
%doc doc/build/html

%files -n python-murano-tests
%license LICENSE
%{python2_sitelib}/murano/tests
%{python2_sitelib}/murano_tempest_tests
%{python2_sitelib}/%{service}_tests.egg-info

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 4.0.0-1
- Update to 4.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-0.2.0rc2
- Update to 4.0.0.0rc2

* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-0.1.0rc1
- Update to 4.0.0.0rc1

