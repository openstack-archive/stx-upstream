%{!?python2_shortver: %global python2_shortver %(%{__python2} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}

%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc \
This is a client library for Gnocchi built on the Gnocchi API. It \
provides a Python API (the gnocchiclient module) and a command-line tool.

Name:             python-gnocchiclient
Version:          7.0.1
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Gnocchi

License:          ASL 2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

BuildArch:        noarch


%package -n python2-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi
%{?python_provide:%python_provide python2-gnocchiclient}


BuildRequires:    python2-setuptools
BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-tools

Requires:         python-cliff >= 1.16.0
Requires:         python2-osc-lib >= 1.7.0
Requires:         python2-keystoneauth1 >= 2.0.0
Requires:         python2-six >= 1.10.0
Requires:         python2-futurist
Requires:         python2-ujson
Requires:         python2-pbr
Requires:         python2-iso8601
Requires:         python-dateutil
Requires:         python2-debtcollector
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:         python2-monotonic
%else
Requires:         python-monotonic
%endif

%description -n python2-%{pypi_name}
%{common_desc}


%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

BuildRequires:    python2-sphinx
BuildRequires:    python2-oslo-sphinx
BuildRequires:    python2-openstack-doc-tools
BuildRequires:    python-cliff
BuildRequires:    python2-keystoneauth1
BuildRequires:    python2-six
BuildRequires:    python2-futurist
BuildRequires:    python2-ujson
BuildRequires:    python2-sphinx_rtd_theme
# test
BuildRequires:    python2-babel
# Runtime requirements needed during documentation build
BuildRequires:    python2-osc-lib
BuildRequires:    python-dateutil

%description      doc
%{common_desc}

This package contains auto-generated documentation.

%package -n python2-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Gnocchi Tests
Requires:         python2-%{pypi_name} = %{version}-%{release}

%description -n python2-%{pypi_name}-tests
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Gnocchi

%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools
BuildRequires:    python3-tools

Requires:         python3-cliff >= 1.16.0
Requires:         python3-osc-lib >= 1.7.0
Requires:         python3-keystoneauth1 >= 2.0.0
Requires:         python3-six >= 1.10.0
Requires:         python3-futurist
Requires:         python3-ujson
Requires:         python3-pbr
Requires:         python3-monotonic
Requires:         python3-iso8601
Requires:         python3-dateutil
Requires:         python3-debtcollector

%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Gnocchi Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}

%endif

%description
%{common_desc}

%package          sdk
Summary:          SDK files for %{pypi_name}

%description      sdk
Contains SDK files for %{pypi_name} package

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
2to3 --write --nobackups %{py3dir}
%endif

# Remove bundled egg-info
rm -rf gnocchiclient.egg-info

# Let RPM handle the requirements
rm -f test-requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py build
popd
%endif


%install
export PBR_VERSION=%{version}
%if 0%{?with_python3}
pushd %{py3dir}
LANG=en_US.UTF-8 %{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/gnocchi %{buildroot}%{_bindir}/python3-gnocchi
popd
%endif

%{__python2} setup.py install --skip-build --root %{buildroot}

# rename binaries, make compat symlinks
install -m 755 -d %{buildroot}/%{_bindir}
pushd %{buildroot}%{_bindir}
for i in gnocchi-{2,%{?python2_shortver}}; do
    ln -s gnocchi $i
done
%if 0%{?with_python3}
for i in gnocchi-{3,%{?python3_shortver}}; do
    ln -s  python3-gnocchi $i
done
%endif
popd

# Some env variables required to successfully build our doc
export PATH=$PATH:%{buildroot}%{_bindir}
export PYTHONPATH=.
export LANG=en_US.utf8
python setup.py build_sphinx -b html

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo

# prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients
tar zcf %{buildroot}/usr/share/remote-clients/%{pypi_name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. %{pypi_name}-%{version}

%files -n python2-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{_bindir}/gnocchi-2*
%{python2_sitelib}/gnocchiclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/gnocchiclient/tests

%files -n python2-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/gnocchiclient/tests


%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/python3-gnocchi
%{_bindir}/gnocchi-3*
%{python3_sitelib}/gnocchiclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/gnocchiclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/gnocchiclient/tests

%endif

%files -n python-%{pypi_name}-doc
%doc doc/build/html

%files sdk
/usr/share/remote-clients/%{pypi_name}-%{version}.tgz

%changelog
* Tue Feb 13 2018 RDO <dev@lists.rdoproject.org> 7.0.1-1
- Update to 7.0.1
