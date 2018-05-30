%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global sname ironicclient

Name:           python-ironicclient
Version:        1.17.0
Release:        0%{?_tis_dist}.%{tis_patch_ver}
Summary:        Python client for Ironic

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/python-ironicclient
Source0:        https://tarballs.openstack.org/python-ironicclient/python-ironicclient-%{version}%{?milestone}.tar.gz
BuildArch:      noarch


%description
A python and command line client library for Ironic.


%package -n python2-%{sname}
Summary:        Python client for Ironic

BuildRequires:  python2-devel
BuildRequires:  python-pbr >= 2.0.0
BuildRequires:  python-setuptools

Requires:       python-appdirs >= 1.3.0
Requires:       python-dogpile-cache >= 0.6.2
Requires:       python-httplib2
Requires:       python-jsonschema
Requires:       python-openstackclient >= 3.3.0
Requires:       python-keystoneauth1 >= 3.1.0
Requires:       python-pbr >= 2.0.0
Requires:       python-prettytable
Requires:       python-six >= 1.9.0
Requires:       python-osc-lib >= 1.7.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-utils >= 3.20.0
Requires:       python-requests
Requires:       PyYAML

%{?python_provide:%python_provide python2-%{sname}}

%description -n python2-%{sname}
A python and command line client library for Ironic


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:        Python client for Ironic

BuildRequires:  python3-devel
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-setuptools

Requires:       python3-appdirs >= 1.3.0
Requires:       python3-dogpile-cache >= 0.6.2
Requires:       python3-httplib2
Requires:       python3-jsonschema
Requires:       python3-openstackclient >= 3.3.0
Requires:       python3-keystoneauth1 >= 3.1.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-prettytable
Requires:       python3-six >= 1.9.0
Requires:       python3-osc-lib >= 1.7.0
Requires:       python3-oslo-i18n >= 2.1.0
Requires:       python3-oslo-serialization >= 1.10.0
Requires:       python3-oslo-utils >= 3.20.0
Requires:       python3-requests
Requires:       python3-PyYAML

%{?python_provide:%python_provide python3-%{sname}}

%description -n python3-%{sname}
A python and command line client library for Ironic
%endif

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

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
mv %{buildroot}%{_bindir}/ironic %{buildroot}%{_bindir}/ironic-%{python3_version}
ln -s ./ironic-%{python3_version} %{buildroot}%{_bindir}/ironic-3
%endif

%py2_install
mv %{buildroot}%{_bindir}/ironic %{buildroot}%{_bindir}/ironic-%{python2_version}
ln -s ./ironic-%{python2_version} %{buildroot}%{_bindir}/ironic-2

ln -s ./ironic-2 %{buildroot}%{_bindir}/ironic

install -p -D -m 644 tools/ironic.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/ironic.bash_completion

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/ironic
%{_bindir}/ironic-2
%{_bindir}/ironic-%{python2_version}
%{python2_sitelib}/ironicclient*
%{python2_sitelib}/python_ironicclient*
%{_sysconfdir}/bash_completion.d/ironic.bash_completion

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
* Wed Sep 06 2017 rdo-trunk <javier.pena@redhat.com> 1.17.0-1
- Update to 1.17.0

* Mon Aug 14 2017 Alfredo Moralejo <amoralej@redhat.com> 1.16.0-1
- Update to 1.16.0

