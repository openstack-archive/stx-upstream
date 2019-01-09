%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%global pypi_name pankoclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

Name:             python-pankoclient
Version:          0.5.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Panko

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch


%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Panko
%{?python_provide:%python_provide python2-%{pypi_name}}


BuildRequires:    git
BuildRequires:    python-setuptools
BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    python-tools

Requires:         python-keystoneauth1 >= 2.18.0
Requires:         python-osc-lib >= 1.2.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.18.0
Requires:         python-pbr
Requires:         python-requests
Requires:         python-six >= 1.9.0


%description -n python2-%{pypi_name}
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.


%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Panko API Client
Group:            Documentation

BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme
# FIXME: remove following line when a new release including https://review.openstack.org/#/c/476760/ is in u-c
BuildRequires:    python-oslo-sphinx
BuildRequires:    python-openstack-doc-tools
BuildRequires:    python-osc-lib
# test
BuildRequires:    python-babel

%description      doc
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool
(panko).

This package contains auto-generated documentation.

%package -n python2-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Panko Tests
Requires:         python-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Panko

%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools
BuildRequires:    python3-tools

Requires:         python3-keystoneauth1 >= 2.18.0
Requires:         python3-osc-lib >= 1.2.0
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-serialization >= 1.10.0
Requires:         python3-oslo-utils >= 3.18.0
Requires:         python3-pbr
Requires:         python3-requests
Requires:         python3-six >= 1.9.0

%description -n python3-%{pypi_name}
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Panko Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.

%endif

%description
This is a client library for Panko built on the Panko API. It
provides a Python API (the pankoclient module) and a command-line tool.


%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

# Remove bundled egg-info
rm -rf pankoclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%py2_build
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif


%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
popd
mv %{buildroot}%{_bindir}/panko %{buildroot}%{_bindir}/panko-%{python3_version}
ln -s ./panko-%{python3_version} %{buildroot}%{_bindir}/panko-3
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/panko %{buildroot}%{_bindir}/panko-%{python2_version}
ln -s %{_bindir}/panko-%{python2_version} %{buildroot}%{_bindir}/panko-2
ln -s %{_bindir}/panko-2 %{buildroot}%{_bindir}/panko

# Some env variables required to successfully build our doc
export PATH=$PATH:%{buildroot}%{_bindir}
export LANG=en_US.utf8
%{__python2} setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/panko
%{_bindir}/panko-2
%{_bindir}/panko-%{python2_version}
# XXX: man page build is broken
#%{_mandir}/man1/panko.1*
%{python2_sitelib}/pankoclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/pankoclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/pankoclient/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/panko-3
%{_bindir}/panko-%{python3_version}
%{python3_sitelib}/pankoclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/pankoclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/pankoclient/tests

%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%changelog
* Wed Aug 22 2018 RDO <dev@lists.rdoproject.org> 0.5.0-1
- Update to 0.5.0


