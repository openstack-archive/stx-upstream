%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global sname ironicclient

%global common_desc A python and command line client library for Ironic

Name:           python-ironicclient
Version:        2.5.0
Release:        1%{?dist}
Summary:        Python client for Ironic

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-ironicclient
Source0:        https://tarballs.openstack.org/python-ironicclient/python-ironicclient-%{version}%{?milestone}.tar.gz
BuildArch:      noarch


%description
%{common_desc}


%package -n python2-%{sname}
Summary:        Python client for Ironic

BuildRequires:  python2-devel
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  python2-setuptools

Requires:       python2-appdirs >= 1.3.0
Requires:       python2-keystoneauth1 >= 3.4.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-prettytable
Requires:       python2-six >= 1.10.0
Requires:       python2-osc-lib >= 1.10.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-serialization >= 2.18.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-requests
%if 0%{?fedora} > 0
Requires:       python2-dogpile-cache >= 0.6.2
Requires:       python2-jsonschema
Requires:       python2-pyyaml
%else
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-jsonschema
Requires:       PyYAML
%endif

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
%{common_desc}


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Python client for Ironic

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools

Requires:       python3-appdirs >= 1.3.0
Requires:       python3-dogpile-cache >= 0.6.2
Requires:       python3-jsonschema
Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable
Requires:       python3-six >= 1.10.0
Requires:       python3-osc-lib >= 1.10.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-serialization >= 2.18.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-requests
Requires:       python3-PyYAML

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
%{common_desc}
%endif

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif


%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/ironic %{buildroot}%{_bindir}/ironic-%{python3_version}
ln -s ./ironic-%{python3_version} %{buildroot}%{_bindir}/ironic-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/ironic %{buildroot}%{_bindir}/ironic-%{python2_version}
ln -s ./ironic-%{python2_version} %{buildroot}%{_bindir}/ironic-2

ln -s ./ironic-2 %{buildroot}%{_bindir}/ironic


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/ironic
%{_bindir}/ironic-2
%{_bindir}/ironic-%{python2_version}
%{python2_sitelib}/ironicclient*
%{python2_sitelib}/python_ironicclient*

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/ironic-3
%{_bindir}/ironic-%{python3_version}
%{python3_sitelib}/ironicclient*
%{python3_sitelib}/python_ironicclient*
%endif


%changelog
* Fri Aug 10 2018 RDO <dev@lists.rdoproject.org> 2.5.0-1
- Update to 2.5.0

