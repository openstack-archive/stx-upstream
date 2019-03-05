%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Client library and command line utility for interacting with Openstack \
Identity API.

Name:       python-keystoneclient
Epoch:      1
Version:    3.17.0
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    Client library for OpenStack Identity API
License:    ASL 2.0
URL:        https://launchpad.net/python-keystoneclient
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires: /usr/bin/openssl


%description
%{common_desc}

%package -n python2-keystoneclient
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python2-keystoneclient}

BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python2-pip
BuildRequires: python2-wheel
BuildRequires: python2-pbr >= 2.0.0
BuildRequires: git

Requires: python2-oslo-config >= 2:5.2.0
Requires: python2-oslo-i18n >= 3.15.3
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-requests >= 2.14.2
Requires: python2-six >= 1.10.0
Requires: python2-stevedore >= 1.20.0
Requires: python2-pbr >= 2.0.0
Requires: python2-debtcollector >= 1.2.0
Requires: python2-keystoneauth1 >= 3.4.0
%if 0%{?fedora} > 0
Requires: python2-keyring >= 5.5.1
%else
Requires: python-keyring >= 5.5.1
%endif

%description -n python2-keystoneclient
%{common_desc}

%if 0%{?with_python3}
%package -n python3-keystoneclient
Summary:    Client library for OpenStack Identity API
%{?python_provide:%python_provide python3-keystoneclient}

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr >= 2.0.0

Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-i18n >= 3.15.3
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-requests >= 2.14.2
Requires: python3-six >= 1.10.0
Requires: python3-stevedore >= 1.20.0
Requires: python3-pbr >= 2.0.0
Requires: python3-debtcollector >= 1.2.0
Requires: python3-keystoneauth1 >= 3.4.0
Requires: python3-keyring >= 5.5.1

%description -n python3-keystoneclient
Client library for interacting with Openstack Identity API.
%endif

%package -n python2-keystoneclient-tests
Summary:  python2-keystoneclient test subpackage
Requires:  python2-keystoneclient = %{epoch}:%{version}-%{release}

BuildRequires:  python2-hacking
BuildRequires:  python2-fixtures
BuildRequires:  python2-mock
BuildRequires:  python2-oauthlib
BuildRequires:  python2-oslotest
BuildRequires:  python2-testtools
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-oslo-serialization
BuildRequires:  python2-oslo-i18n
BuildRequires:  python2-stestr
BuildRequires:  python2-testresources
BuildRequires:  python2-testscenarios
%if 0%{?fedora} > 0
BuildRequires:  python2-keyring >= 5.5.1
BuildRequires:  python2-lxml
BuildRequires:  python2-requests-mock
%else
BuildRequires:  python-keyring >= 5.5.1
BuildRequires:  python-lxml
BuildRequires:  python-requests-mock
%endif

Requires:  python2-hacking
Requires:  python2-fixtures
Requires:  python2-mock
Requires:  python2-oauthlib
Requires:  python2-oslotest
Requires:  python2-stestr
Requires:  python2-testtools
Requires:  python2-testresources
Requires:  python2-testscenarios
%if 0%{?fedora} > 0
Requires:  python2-lxml
Requires:  python2-requests-mock
%else
Requires:  python-lxml
Requires:  python-requests-mock
%endif


%description -n python2-keystoneclient-tests
python2-keystoneclient test subpackages

%if 0%{?with_python3}
%package -n python3-keystoneclient-tests
Summary:  python3-keystoneclient test subpackage
Requires:  python3-keystoneclient = %{epoch}:%{version}-%{release}

BuildRequires:  python3-hacking
BuildRequires:  python3-fixtures
BuildRequires:  python3-keyring >= 5.5.1
BuildRequires:  python3-lxml
BuildRequires:  python3-mock
BuildRequires:  python3-oauthlib
BuildRequires:  python3-oslotest
BuildRequires:  python3-requests-mock
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-testtools
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-oslo-serialization
BuildRequires:  python3-oslo-i18n
BuildRequires:  python3-stestr

Requires:  python3-hacking
Requires:  python3-fixtures
Requires:  python3-lxml
Requires:  python3-mock
Requires:  python3-oauthlib
Requires:  python3-oslotest
Requires:  python3-requests-mock
Requires:  python3-stestr
Requires:  python3-testresources
Requires:  python3-testscenarios
Requires:  python3-testtools


%description -n python3-keystoneclient-tests
python3-keystoneclient test subpackages
%endif

%package doc
Summary: Documentation for OpenStack Keystone API client

BuildRequires: python2-sphinx
BuildRequires: python2-openstackdocstheme

%description doc
Documentation for the keystoneclient module

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# disable warning-is-error, this project has intersphinx in docs
# so some warnings are generated in network isolated build environment
# as koji
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
%py2_build_wheel
%if 0%{?with_python3}
%py3_build
%endif

%install
export PBR_VERSION=%{version}
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

# Build HTML docs
%{__python2} setup.py build_sphinx -b html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}

# STX: stage wheels
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# STX: prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients
tar zcf %{buildroot}/usr/share/remote-clients/%{name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. %{name}-%{version}

%check
stestr --test-path=./keystoneclient/tests/unit run
%if 0%{?with_python3}
stestr-3 --test-path=./keystoneclient/tests/unit run
%endif

%files -n python2-keystoneclient
%license LICENSE
%doc README.rst
%{python2_sitelib}/keystoneclient
%{python2_sitelib}/*.egg-info
%exclude %{python2_sitelib}/keystoneclient/tests

%if 0%{?with_python3}
%files -n python3-keystoneclient
%license LICENSE
%doc README.rst
%{python3_sitelib}/keystoneclient
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/keystoneclient/tests
%endif

%files doc
%doc doc/build/html
%license LICENSE

%files -n python2-keystoneclient-tests
%license LICENSE
%{python2_sitelib}/keystoneclient/tests

%if 0%{?with_python3}
%files -n python3-keystoneclient-tests
%license LICENSE
%{python3_sitelib}/keystoneclient/tests
%endif

%package          sdk
Summary:          SDK files for %{name}

%description      sdk
Contains SDK files for %{name} package

%files sdk
/usr/share/remote-clients/%{name}-%{version}.tgz

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*


%changelog
* Wed Aug 08 2018 RDO <dev@lists.rdoproject.org> 1:3.17.0-1
- Update to 3.17.0

