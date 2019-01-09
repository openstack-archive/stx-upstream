%global pypi_name muranoclient

%if 0%{?fedora}
%global with_python3 0
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Client library for Murano built on the Murano API. It provides a Python \
API (the muranoclient module) and a command-line tool (murano).

Name:           python-%{pypi_name}
Version:        1.1.1
Release:        1%{?dist}
Summary:        Client library for OpenStack Murano API

License:        ASL 2.0
URL:            http://pypi.python.org/pypi/%{name}
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n     python2-%{pypi_name}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pbr >= 2.0.0

Requires:       python2-babel >= 2.3.4
Requires:       python2-glanceclient >= 1:2.8.0
Requires:       python2-iso8601 >= 0.1.11
Requires:       python2-keystoneclient >= 1:3.8.0
Requires:       python2-murano-pkg-check >= 0.3.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-prettytable >= 0.7.2
Requires:       python2-requests >= 2.14.2
Requires:       python2-six >= 1.10.0
Requires:       python2-yaql >= 1.1.3
Requires:       python2-osc-lib >= 1.10.0
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pyOpenSSL >= 16.2.0
%if 0%{?fedora} > 0
Requires:       python2-pyyaml >= 3.10
%else
Requires:       PyYAML >= 3.10
%endif

Summary:        Client library for OpenStack Murano API.
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{common_desc}

# Python3 package
%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Support of EC2 API for OpenStack
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python-tools

Requires:       python3-babel >= 2.3.4
Requires:       python3-glanceclient >= 1:2.8.0
Requires:       python3-iso8601 >= 0.1.11
Requires:       python3-keystoneclient >= 1:3.8.0
Requires:       python3-murano-pkg-check >= 0.3.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable >= 0.7.2
Requires:       python3-requests >= 2.14.2
Requires:       python3-six >= 1.10.0
Requires:       python3-yaql >= 1.1.3
Requires:       python3-osc-lib >= 1.10.0
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pyOpenSSL >= 16.2.0
Requires:       python3-PyYAML >= 3.10

%description -n python3-%{pypi_name}
%{common_desc}
%endif

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Murano API Client

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme

%description -n python-%{pypi_name}-doc
Documentation for the client library for interacting with Openstack
Murano API.

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
# Let RPM handle the dependencies
%py_req_cleanup

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif

# generate html docs
export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/murano %{buildroot}%{_bindir}/python3-murano
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
pushd %{buildroot}%{_bindir}
%if 0%{?with_python3}
for i in %{pypi_name}-{3,%{?python3_shortver}}; do
    ln -s  python3-%{pypi_name} $i
done
%endif
popd

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/python_%{pypi_name}-*-py?.?.egg-info
%{_bindir}/murano*

# Files for python3
%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/python3-murano
%{_bindir}/murano*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/python_%{pypi_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE

%changelog
* Thu Aug 16 2018 RDO <dev@lists.rdoproject.org> 1.1.1-1
- Update to 1.1.1

