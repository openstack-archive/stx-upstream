%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname heatclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This is a client for the OpenStack Heat API. There's a Python API (the \
heatclient module), and a command-line script (heat). Each implements 100% of \
the OpenStack Heat API.

Name:    python-heatclient
Version: 1.16.1
Release: 1%{?dist}
Summary: Python API and CLI for OpenStack Heat

License: ASL 2.0
URL:     https://launchpad.net/python-heatclient
Source0: https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch: noarch

%description
%{common_desc}

%package -n python2-%{sname}
Summary: Python API and CLI for OpenStack Heat
%{?python_provide:%python_provide python2-heatclient}
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pbr
BuildRequires: git

Requires: python2-babel
Requires: python2-iso8601
Requires: python2-keystoneauth1 >= 3.4.0
Requires: python2-osc-lib >= 1.8.0
Requires: python2-prettytable
Requires: python2-pbr
Requires: python2-six
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-swiftclient >= 3.2.0
Requires: python2-requests
Requires: python2-cliff
%if 0%{?fedora} > 0
Requires: python2-pyyaml
%else
Requires: PyYAML
%endif

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary: Python API and CLI for OpenStack Heat
%{?python_provide:%python_provide python3-heatclient}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires: python3-babel
Requires: python3-cliff
Requires: python3-iso8601
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-osc-lib >= 1.8.0
Requires: python3-prettytable
Requires: python3-pbr
Requires: python3-six
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-swiftclient >= 3.2.0
Requires: python3-requests
Requires: python3-PyYAML

%description -n python3-%{sname}
%{common_desc}
%endif

%package doc
Summary: Documentation for OpenStack Heat API Client

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme
BuildRequires: python2-babel
BuildRequires: python2-iso8601
BuildRequires: python2-keystoneauth1
BuildRequires: python2-osc-lib
BuildRequires: python2-prettytable
BuildRequires: python2-pbr
BuildRequires: python2-six
BuildRequires: python2-oslo-serialization
BuildRequires: python2-oslo-utils
BuildRequires: python2-oslo-i18n
BuildRequires: python2-swiftclient
BuildRequires: python2-requests
BuildRequires: python2-cliff

%description doc
%{common_desc}

This package contains auto-generated documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
echo "%{version}" > %{buildroot}%{python3_sitelib}/heatclient/versioninfo
mv %{buildroot}%{_bindir}/heat %{buildroot}%{_bindir}/heat-%{python3_version}
ln -s ./heat-%{python3_version} %{buildroot}%{_bindir}/heat-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/heatclient/tests
%endif

%py2_install
echo "%{version}" > %{buildroot}%{python2_sitelib}/heatclient/versioninfo
mv %{buildroot}%{_bindir}/heat %{buildroot}%{_bindir}/heat-%{python2_version}
ln -s ./heat-%{python2_version} %{buildroot}%{_bindir}/heat-2

ln -s ./heat-2 %{buildroot}%{_bindir}/heat

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/heat.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/heat

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/heatclient/tests


export PYTHONPATH=.
sphinx-build -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
sphinx-build -W -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/heat.1 %{buildroot}%{_mandir}/man1/heat.1

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/heatclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/heat.1.gz
%{_bindir}/heat
%{_bindir}/heat-2
%{_bindir}/heat-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/heat.1.gz
%{_bindir}/heat-3
%{_bindir}/heat-%{python3_version}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Fri Aug 10 2018 RDO <dev@lists.rdoproject.org> 1.16.1-1
- Update to 1.16.1

