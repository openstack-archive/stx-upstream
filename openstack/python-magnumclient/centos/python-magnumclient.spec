%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global sname python-magnumclient
%global pname magnumclient

%if 0%{?fedora} >= 24
%global with_python3 1
%global default_python 3
%else
%global default_python 2
%endif

%global common_desc \
This is a client library for Magnum built on the Magnum API. \
It provides a Python API (the magnumclient module) and a \
command-line tool (magnum).

%global common_desc_tests Python-magnumclient test subpackage

Name:           python-%{pname}
Version:        2.10.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        Client library for Magnum API

License:        ASL 2.0
URL:            https://launchpad.net/python-magnumclient
Source0:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python2-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python2-%{pname}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python2-pbr
BuildRequires:  git

# test dependencies
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-openstackclient
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslo-log
BuildRequires:  python2-osprofiler
BuildRequires:  python2-stevedore
BuildRequires:  python2-requests
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-fixtures
BuildRequires:  python2-mock
BuildRequires:  python2-testtools
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-prettytable

Requires:    python2-babel
Requires:    python2-cryptography
Requires:    python2-keystoneauth1 >= 3.4.0
Requires:    python2-oslo-i18n >= 3.15.3
Requires:    python2-oslo-log >= 3.36.0
Requires:    python2-oslo-serialization >= 2.18.0
Requires:    python2-oslo-utils >= 3.33.0
Requires:    python2-osc-lib >= 1.8.0
Requires:    python2-os-client-config >= 1.28.0
Requires:    python2-pbr
Requires:    python2-prettytable
Requires:    python2-six
%if 0%{?fedora} > 0
Requires:    python2-decorator
%else
Requires:    python-decorator
%endif

%description -n python2-%{pname}
%{common_desc}

%if 0%{?with_python3}
%package -n     python3-%{pname}
Summary:        Client library for Magnum API
%{?python_provide:%python_provide python3-%{pname}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr

# test dependencies
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-openstackclient
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-log
BuildRequires:  python3-osprofiler
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
Requires:    python3-keystoneauth1 >= 3.4.0
Requires:    python3-oslo-i18n >= 3.15.3
Requires:    python3-oslo-log >= 3.36.0
Requires:    python3-oslo-serialization >= 2.18.0
Requires:    python3-oslo-utils >= 3.33.0
Requires:    python3-osc-lib >= 1.8.0
Requires:    python3-os-client-config >= 1.28.0
Requires:    python3-pbr
Requires:    python3-prettytable
Requires:    python3-six

%description -n python3-%{pname}
%{common_desc}
%endif

%package -n python-%{pname}-doc
Summary:        python-magnumclient documentation
BuildRequires:   python2-sphinx
BuildRequires:   python2-openstackdocstheme
BuildRequires:   python2-os-client-config
BuildRequires:   openstack-macros
%if 0%{?fedora} > 0
BuildRequires:   python2-decorator
%else
BuildRequires:   python-decorator
%endif

%description -n python-%{pname}-doc
Documentation for python-magnumclient

%package -n python2-%{pname}-tests
Summary: Python-magnumclient test subpackage
%{?python_provide:%python_provide python2-%{pname}-tests}

Requires:  python2-%{pname} = %{version}-%{release}
Requires:  python2-oslo-utils
Requires:  python2-stevedore
Requires:  python2-requests
Requires:  python2-oslo-i18n
Requires:  python2-fixtures
Requires:  python2-mock
Requires:  python2-testtools
Requires:  python2-keystoneauth1
Requires:  python2-prettytable

%description -n python2-%{pname}-tests
%{common_desc_tests}

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
%{common_desc_tests}
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

%build
export PBR_VERSION=%{version}
%py2_build
%py2_build_wheel

%if 0%{?with_python3}
%py3_build
%endif
# generate html docs
# (TODO) Re-add -W once https://review.openstack.org/#/c/554197 is in a
# tagged release
sphinx-build -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
export PBR_VERSION=%{version}
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

mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%check
# tests are failing due to unicode not defined
# we are skipping the test
%{__python2} setup.py test ||
%if 0%{?with_python3}
%{__python3} setup.py test ||
%endif

%files -n python2-%{pname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/%{pname}
%if 0%{?default_python} <= 2
%{_bindir}/magnum
%endif
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/%{pname}/tests

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

%files -n python2-%{pname}-tests
%{python2_sitelib}/%{pname}/tests

%if 0%{?with_python3}
%files -n python3-%{pname}-tests
%{python3_sitelib}/%{pname}/tests
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 2.10.0-1
- Update to 2.10.0

