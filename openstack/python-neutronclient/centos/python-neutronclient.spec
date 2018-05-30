%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname neutronclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:       python-neutronclient
Version:    6.5.0
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    Python API and CLI for OpenStack Neutron

License:    ASL 2.0
URL:        http://launchpad.net/python-neutronclient/
Source0:    %{name}-%{version}.tar.gz

BuildArch:  noarch

Obsoletes:  python-%{sname}-tests <= 4.1.1-3

%description
Client library and command line utility for interacting with OpenStack
Neutron's API.

%package -n python2-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python2-neutronclient}

BuildRequires: git
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

Requires: python-babel >= 2.3.4
Requires: python-cliff >= 2.8.0
Requires: python-dateutil
Requires: python-iso8601 >= 0.1.11
Requires: python-netaddr >= 0.7.13
Requires: python-os-client-config >= 1.28.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-pbr
Requires: python-requests >= 2.10.0
Requires: python-simplejson >= 2.2.0
Requires: python-six >= 1.9.0
Requires: python-debtcollector >= 1.2.0
Requires: python-osc-lib >= 1.7.0
Requires: python-keystoneauth1 >= 3.1.0
Requires: python-keystoneclient >= 1:3.8.0

%description -n python2-%{sname}
Client library and command line utility for interacting with OpenStack
Neutron's API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:    Python API and CLI for OpenStack Neutron
%{?python_provide:%python_provide python3-neutronclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires: python3-babel >= 2.3.4
Requires: python3-cliff >= 2.8.0
Requires: python3-iso8601 >= 0.1.11
Requires: python3-netaddr >= 0.7.13
Requires: python3-os-client-config >= 1.28.0
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.20.0
Requires: python3-pbr
Requires: python3-requests >= 2.10.0
Requires: python3-simplejson >= 2.2.0
Requires: python3-six >= 1.9.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-osc-lib >= 1.7.0
Requires: python3-keystoneauth1 >= 3.1.0
Requires: python3-keystoneclient >= 1:3.8.0

%description -n python3-%{sname}
Client library and command line utility for interacting with OpenStack
Neutron's API.
%endif

%package doc
Summary:          Documentation for OpenStack Neutron API Client

BuildRequires:    python-dateutil
BuildRequires:    python-sphinx
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-reno
BuildRequires:    python-cliff
BuildRequires:    python-keystoneauth1
BuildRequires:    python-keystoneclient
BuildRequires:    python-os-client-config
BuildRequires:    python-osc-lib
BuildRequires:    python-oslo-serialization
BuildRequires:    python-oslo-utils

%description      doc
Client library and command line utility for interacting with OpenStack
Neutron's API.


%package          sdk
Summary:          SDK files for %{name}

%description      sdk
Contains SDK files for %{name} package


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
export PBR_VERSION=%{version}
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python3_version}
ln -s ./neutron-%{python3_version} %{buildroot}%{_bindir}/neutron-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/neutronclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/neutron %{buildroot}%{_bindir}/neutron-%{python2_version}
ln -s ./neutron-%{python2_version} %{buildroot}%{_bindir}/neutron-2

ln -s ./neutron-2 %{buildroot}%{_bindir}/neutron

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/neutron.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/neutron

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/neutronclient/tests

%{__python2} setup.py build_sphinx -b html

# prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients/%{name}
tar zcf %{buildroot}/usr/share/remote-clients/%{name}/%{name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. %{name}-%{version}


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/neutronclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_bindir}/neutron
%{_bindir}/neutron-2
%{_bindir}/neutron-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_bindir}/neutron-3
%{_bindir}/neutron-%{python3_version}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%files sdk
/usr/share/remote-clients/%{name}/%{name}-%{version}.tgz

%changelog
* Mon Aug 14 2017 Alfredo Moralejo <amoralej@redhat.com> 6.5.0-1
- Update to 6.5.0

