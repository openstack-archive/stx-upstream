%global pypi_name networking-sfc
%global module networking_sfc
%global with_doc 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pypi_name}
Version:        5.0.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        API and implementations to support Service Function Chaining in Neutron

License:        ASL 2.0
URL:            https://github.com/openstack/networking-sfc
Source0:        %{name}-%{version}.tar.gz

#

BuildArch:      noarch

BuildRequires:  openstack-macros
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-sphinx
#BuildRequires:  openstack-neutron
# Test requirements
BuildRequires:  python-mock
BuildRequires:  python-requests-mock
BuildRequires:  python-oslotest
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-neutron-lib-tests
BuildRequires:  python-neutron-tests
BuildRequires:  python2-pip
BuildRequires:  python2-wheel

%description
This project provides APIs and implementations to support Service Function
Chaining in Neutron.

Service Function Chaining is a mechanism for overriding the basic destination
based forwarding that is typical of IP networks. It is conceptually related to
Policy Based Routing in physical networks but it is typically thought of as a
Software Defined Networking technology. It is often used in conjunction with
security functions although it may be used for a broader range of features.
Fundamentally SFC is the ability to cause network packet flows to route through
a network via a path other than the one that would be chosen by routing table
lookup on the packet's destination IP address. It is most commonly used in
conjunction with Network Function Virtualization when recreating in a virtual
environment a series of network functions that would have traditionally been
implemented as a collection of physical network devices connected in series by
cables.

%package -n python2-%{pypi_name}
Summary:        API and implementations to support Service Function Chaining in Neutron
%{?python_provide:%python_provide python2-%{pypi_name}}

#Requires:       openstack-neutron-common
#Requires:       openstack-neutron
Requires:       python-alembic
Requires:       python-eventlet
Requires:       python-netaddr
Requires:       python-neutron
Requires:       python-neutron-lib >= 1.9.0
Requires:       python-neutronclient >= 6.3.0
Requires:       python-oslo-config >= 2:4.0.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 3.22.0
Requires:       python-oslo-messaging >= 5.24.2
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-six
Requires:       python-sqlalchemy
Requires:       python-stevedore >= 1.20.0

%description -n python2-%{pypi_name}
This project provides APIs and implementations to support Service Function
Chaining in Neutron.

Service Function Chaining is a mechanism for overriding the basic destination
based forwarding that is typical of IP networks. It is conceptually related to
Policy Based Routing in physical networks but it is typically thought of as a
Software Defined Networking technology. It is often used in conjunction with
security functions although it may be used for a broader range of features.
Fundamentally SFC is the ability to cause network packet flows to route through
a network via a path other than the one that would be chosen by routing table
lookup on the packet's destination IP address. It is most commonly used in
conjunction with Network Function Virtualization when recreating in a virtual
environment a series of network functions that would have traditionally been
implemented as a collection of physical network devices connected in series by
cables.


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for networking-sfc
%description -n python-%{pypi_name}-doc
Documentation for networking-sfc
%endif

%package -n python2-%{pypi_name}-tests
Summary:        Tests for networking-sfc
Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python-mock
Requires:       python-requests-mock
Requires:       python-oslotest
Requires:       python-testrepository
Requires:       python-testresources
Requires:       python-testscenarios
Requires:       python-neutron-lib-tests
Requires:       python-neutron-tests

%description -n python2-%{pypi_name}-tests
Networking-sfc set of tests

%package -n python2-%{pypi_name}-tests-tempest
Summary:    Tempest plugin for %{name}

Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python-tempest-tests

%description -n python2-%{pypi_name}-tests-tempest
It contains the tempest plugin for %{name}.

%prep
%autosetup -n %{name}-%{upstream_version}
# Let RPM handle the dependencies
%py_req_cleanup

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# FIXME(bcafarel): require neutronclient.tests.unit (python-neutronclient-tests package was dropped)
rm -rf %{module}/tests/unit/cli

%build
export PBR_VERSION=%{version}
%py2_build
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif
# generate the configuration file
PYTHONPATH=. oslo-config-generator --config-file etc/oslo-config-generator/networking-sfc.conf

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%py2_install
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create a fake tempest plugin entrypoint
%py2_entrypoint %{module} %{pypi_name}

# The generated config files are not moved automatically by setup.py
mkdir -p %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server
mv etc/networking-sfc.conf.sample %{buildroot}%{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf

#%check
#export OS_TEST_PATH='./networking_sfc/tests/functional'
#export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
#%{__python2} setup.py testr

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/conf.d/neutron-server/networking-sfc.conf
%exclude %{python2_sitelib}/%{module}/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html/*
%license LICENSE
%endif

%files -n python2-%{pypi_name}-tests
%{python2_sitelib}/%{module}/tests
%exclude %{python2_sitelib}/%{module}/tests/contrib
%exclude %{python2_sitelib}/%{module}/tests/tempest_plugin

%files -n python2-%{pypi_name}-tests-tempest
%{python2_sitelib}/%{module}_tests.egg-info
%{python2_sitelib}/%{module}/tests/tempest_plugin
%{python2_sitelib}/%{module}/tests/__init__.py*

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 5.0.0-1
- Update to 5.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-0.1.0rc2
- Update to 5.0.0.0rc2

