%global pypi_name aodhclient

%if 0%{?fedora}
%global with_python3 1
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
This is a client library for Aodh built on the Aodh API. It \
provides a Python API (the aodhclient module) and a command-line tool.

Name:             python-aodhclient
Version:          1.1.1
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Aodh

License:          ASL 2.0
URL:              https://launchpad.net/python-aodhclient
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch

%description
%{common_desc}

%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    git

Requires:         python-pbr
Requires:         python-cliff >= 1.14.0
Requires:         python-oslo-i18n >= 1.5.0
Requires:         python-oslo-serialization >= 1.4.0
Requires:         python-oslo-utils >= 2.0.0
Requires:         python-keystoneauth1 >= 1.0.0
Requires:         python-six >= 1.9.0
Requires:         python-osc-lib >= 1.0.1
Requires:         pyparsing

%description -n python2-%{pypi_name}
%{common_desc}


%package  doc
Summary:          Documentation for OpenStack Aodh API Client

BuildRequires:    python-sphinx
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/476759/ is in u-c
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-keystoneauth1
BuildRequires:    python-oslo-utils
BuildRequires:    python-oslo-serialization
BuildRequires:    python-cliff


%description doc
%{common_desc}
(aodh).

This package contains auto-generated documentation.

%package -n python2-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc}


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh

%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-setuptools
BuildRequires:    python3-devel
BuildRequires:    python3-pbr

Requires:         python3-pbr
Requires:         python3-cliff >= 1.14.0
Requires:         python3-oslo-i18n >= 1.5.0
Requires:         python3-oslo-serialization >= 1.4.0
Requires:         python3-oslo-utils >= 2.0.0
Requires:         python3-keystoneauth1 >= 1.0.0
Requires:         python3-six >= 1.9.0
Requires:         python3-osc-lib >= 1.0.1
Requires:         python3-pyparsing

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}

%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the requirements
rm -f {,test-}requirements.txt


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/aodh %{buildroot}%{_bindir}/aodh-%{python3_version}
ln -s ./aodh-%{python3_version} %{buildroot}%{_bindir}/aodh-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/aodh %{buildroot}%{_bindir}/aodh-%{python2_version}
ln -s ./aodh-%{python2_version} %{buildroot}%{_bindir}/aodh-2

ln -s ./aodh-2 %{buildroot}%{_bindir}/aodh

export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{python2_sitelib}/aodhclient
%{python2_sitelib}/*.egg-info
%{_bindir}/aodh
%{_bindir}/aodh-2
%{_bindir}/aodh-%{python2_version}
%exclude %{python2_sitelib}/aodhclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/aodhclient/tests

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.egg-info
%{_bindir}/aodh-3
%{_bindir}/aodh-%{python3_version}
%exclude %{python3_sitelib}/aodhclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/aodhclient/tests
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 1.1.1-1
- Update to 1.1.1

