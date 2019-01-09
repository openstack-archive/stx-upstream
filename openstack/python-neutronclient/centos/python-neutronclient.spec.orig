%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname neutronclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Client library and command line utility for interacting with OpenStack \
Neutron's API.

Name:       python-neutronclient
Version:    6.9.1
Release:    1%{?dist}
Summary:    Python API and CLI for OpenStack Neutron

License:    ASL 2.0
URL:        http://launchpad.net/%{name}/
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:  noarch

Obsoletes:  python-%{sname}-tests <= 4.1.1-3

%description
%{common_desc}

%package -n python2-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python2-neutronclient}

BuildRequires: git
BuildRequires: openstack-macros
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pbr
# Required for unit tests
BuildRequires: python2-osc-lib-tests
BuildRequires: python2-oslotest
BuildRequires: python2-testtools
BuildRequires: python2-testrepository
BuildRequires: python2-testscenarios

Requires: python2-babel >= 2.3.4
Requires: python2-iso8601 >= 0.1.11
Requires: python2-os-client-config >= 1.28.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-pbr
Requires: python2-requests >= 2.14.2
Requires: python2-six >= 1.10.0
Requires: python2-debtcollector >= 1.2.0
Requires: python2-osc-lib >= 1.10.0
Requires: python2-keystoneauth1 >= 3.4.0
Requires: python2-keystoneclient >= 1:3.8.0
Requires: python2-cliff >= 2.8.0
%if 0%{?fedora} > 0
Requires: python2-netaddr >= 0.7.18
Requires: python2-simplejson >= 3.5.1
%else
Requires: python-netaddr >= 0.7.18
Requires: python-simplejson >= 3.5.1
%endif

%description -n python2-%{sname}
%{common_desc}

%package -n python2-%{sname}-tests
Summary:    Python API and CLI for OpenStack Neutron - Unit tests
%{?python_provide:%python_provide python2-%{sname}-tests}
Requires: python2-%{sname} == %{version}-%{release}
Requires: python2-osc-lib-tests
Requires: python2-oslotest
Requires: python2-testtools
Requires: python2-testrepository
Requires: python2-testscenarios

%description -n python2-%{sname}-tests
%{common_desc}

This package containts the unit tests.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python3-neutronclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr
# Required for unit tests
BuildRequires: python3-osc-lib-tests
BuildRequires: python3-oslotest
BuildRequires: python3-testrepository
BuildRequires: python3-testtools
BuildRequires: python3-testscenarios

Requires: python3-babel >= 2.3.4
Requires: python3-cliff >= 2.8.0
Requires: python3-iso8601 >= 0.1.11
Requires: python3-netaddr >= 0.7.18
Requires: python3-os-client-config >= 1.28.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-pbr
Requires: python3-requests >= 2.14.2
Requires: python3-simplejson >= 3.5.1
Requires: python3-six >= 1.10.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-osc-lib >= 1.10.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-keystoneclient >= 1:3.8.0

%description -n python3-%{sname}
%{common_desc}


%package -n python3-%{sname}-tests
Summary:    Python API and CLI for OpenStack Neutron - Unit tests
%{?python_provide:%python_provide python3-%{sname}-tests}
Requires: python3-%{sname} == %{version}-%{release}
Requires: python3-osc-lib-tests
Requires: python3-oslotest
Requires: python3-testrepository
Requires: python3-testtools
Requires: python3-testscenarios

%description -n python3-%{sname}-tests
%{common_desc}

This package containts the unit tests.
%endif

%package doc
Summary:          Documentation for OpenStack Neutron API Client

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-reno
BuildRequires:    python2-keystoneauth1
BuildRequires:    python2-keystoneclient
BuildRequires:    python2-os-client-config
BuildRequires:    python2-osc-lib
BuildRequires:    python2-oslo-serialization
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-cliff

%description      doc
%{common_desc}

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Build HTML docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python3_version}
ln -s ./neutron-%{python3_version} %{buildroot}%{_bindir}/neutron-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python2_version}
ln -s ./neutron-%{python2_version} %{buildroot}%{_bindir}/neutron-2
ln -s ./neutron-2 %{buildroot}%{_bindir}/neutron

%check
# (TODO) Ignore unit tests results until https://bugs.launchpad.net/python-neutronclient/+bug/1783789
# is fixed.
%{__python2} setup.py testr || true
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py testr || true
%endif

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/neutronclient
%{python2_sitelib}/*.egg-info
%{_bindir}/neutron
%{_bindir}/neutron-2
%{_bindir}/neutron-%{python2_version}
%exclude %{python2_sitelib}/neutronclient/tests

%files -n python2-%{sname}-tests
%{python2_sitelib}/neutronclient/tests

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_bindir}/neutron-3
%{_bindir}/neutron-%{python3_version}
%exclude %{python3_sitelib}/neutronclient/tests

%files -n python3-%{sname}-tests
%{python3_sitelib}/neutronclient/tests
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Thu Sep 20 2018 RDO <dev@lists.rdoproject.org> 6.9.1-1
- Update to 6.9.1

* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 6.9.0-1
- Update to 6.9.0

