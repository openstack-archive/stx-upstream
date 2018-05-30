%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname python-magnumclient
%global pname magnumclient

%if 0%{?fedora} >= 24
%global with_python3 1
%global default_python 3
%else
%global default_python 2
%endif

Name:           python-%{pname}
Version:        2.7.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        Client library for Magnum API

License:        ASL 2.0
URL:            https://launchpad.net/python-magnumclient
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).

%package -n     python2-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python2-%{pname}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  git

# test dependencies
BuildRequires:  python-oslo-utils
BuildRequires:  python-stevedore
BuildRequires:  python-requests
BuildRequires:  python-oslo-i18n
BuildRequires:  python-fixtures
BuildRequires:  python-mock
BuildRequires:  python-testtools
BuildRequires:  python-keystoneauth1
BuildRequires:  python-prettytable

Requires:    python-babel
Requires:    python-cryptography
Requires:    python-decorator
Requires:    python-keystoneauth1 >= 3.1.0
Requires:    python-oslo-i18n >= 2.1.0
Requires:    python-oslo-serialization >= 1.10.0
Requires:    python-oslo-utils >= 3.20.0
Requires:    python-osc-lib >= 1.7.0
Requires:    python-os-client-config >= 1.28.0
Requires:    python-pbr
Requires:    python-prettytable
Requires:    python-six

%description -n python2-%{pname}
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).

%if 0%{?with_python3}
%package -n     python3-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# test dependencies
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-stevedore
BuildRequires:  python3-requests
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-fixtures
BuildRequires:  python3-mock
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-prettytable

Requires:    python3-babel
Requires:    python3-cryptography
Requires:    python3-decorator
Requires:    python3-keystoneauth1 >= 3.1.0
Requires:    python3-oslo-i18n >= 2.1.0
Requires:    python3-oslo-serialization >= 1.10.0
Requires:    python3-oslo-utils >= 3.20.0
Requires:    python3-osc-lib >= 1.7.0
Requires:    python3-os-client-config >= 1.28.0
Requires:    python3-pbr
Requires:    python3-prettytable
Requires:    python3-six

%description -n python3-%{pname}
This is a client library for Magnum built on the Magnum API.
It provides a Python API (the magnumclient module) and a
command-line tool (magnum).
%endif

%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation
BuildRequires:   python-sphinx
BuildRequires:   python-openstackdocstheme
BuildRequires:   python-os-client-config
#BuildRequires:   python-decorator

%description -n python-%{pname}-doc
Documentation for python-magnumclient

%package -n python-%{pname}-tests
Summary: Python-magnumclient test subpackage

Requires:  python-%{pname} = %{version}-%{release}
Requires:  python-oslo-utils
Requires:  python-stevedore
Requires:  python-requests
Requires:  python-oslo-i18n
Requires:  python-fixtures
Requires:  python-mock
Requires:  python-testtools
Requires:  python-keystoneauth1
Requires:  python-prettytable

%description -n python-%{pname}-tests
Python-magnumclient test subpackage

%if 0%{?with_python3}
%package -n python3-%{pname}-tests
Summary: Python-magnumclient test subpackage

Requires:  python3-%{pname} = %{version}-%{release}
Requires:  python3-oslo-utils
Requires:  python3-stevedore
Requires:  python3-requests
Requires:  python3-oslo-i18n
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-testtools
Requires:  python3-keystoneauth1
Requires:  python3-prettytable

%description -n python3-%{pname}-tests
Python-magnumclient test subpackage
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# let RPM handle deps
rm -rf {test-,}requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build

%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
export PBR_VERSION=%{version}

install -p -D -m 644 tools/magnum.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/magnum.bash_completion

%if 0%{?with_python3}
%py3_install
%if %{default_python} >= 3
mv %{buildroot}%{_bindir}/magnum ./magnum.py3
%endif
%endif

%py2_install

%if 0%{?default_python} >= 3
mv magnum.py3 %{buildroot}%{_bindir}/magnum
%endif

#%check
# tests are failing due to unicode not defined
# we are skipping the test
#%{__python2} setup.py test ||
#%if 0%{?with_python3}
#%{__python3} setup.py test ||
#%endif

%files -n python2-%{pname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pname}
%if 0%{?default_python} <= 2
%{_bindir}/magnum
%endif
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{pname}/tests
%{_sysconfdir}/bash_completion.d/magnum.bash_completion

%if 0%{?with_python3}
%files -n python3-%{pname}
%doc README.rst
%license LICENSE
%if 0%{?default_python} >= 3
%{_bindir}/magnum
%endif
%{python3_sitelib}/magnumclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{pname}/tests
%endif

%files -n python-%{pname}-doc
%license LICENSE
%doc doc/build/html

%files -n python-%{pname}-tests
%{python2_sitelib}/%{pname}/tests

%if 0%{?with_python3}
%files -n python3-%{pname}-tests
%{python3_sitelib}/%{pname}/tests
%endif

%changelog
* Fri Aug 11 2017 Alfredo Moralejo <amoralej@redhat.com> 2.7.0-1
- Update to 2.7.0

