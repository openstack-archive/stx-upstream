%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library neutron-lib
%global module neutron_lib

Name:       python-%{library}
Version:    1.9.1
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    OpenStack Neutron library
License:    ASL 2.0
URL:        http://launchpad.net/neutron/

Source0:    %{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  git

Requires:   python-debtcollector >= 1.2.0
Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-context >= 2.14.0
Requires:   python-oslo-db >= 4.24.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-log >= 3.22.0
Requires:   python-oslo-messaging >= 5.24.2
Requires:   python-oslo-policy >= 1.23.0
Requires:   python-oslo-service >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-sqlalchemy >= 1.0.10
Requires:   python-stevedore

%description
OpenStack Neutron library shared by all Neutron sub-projects.


%package tests
Summary:    OpenStack Neutron library tests
Requires:   python-%{library} = %{version}-%{release}

%description tests
OpenStack Neutron library shared by all Neutron sub-projects.

This package contains the Neutron library test files.


%package doc
Summary:    OpenStack Neutron library documentation

BuildRequires: python-sphinx
BuildRequires: python-openstackdocstheme
BuildRequires: python-oslo-context
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-service
BuildRequires: python-netaddr
BuildRequires: python-debtcollector
BuildRequires: python-fixtures

%description doc
OpenStack Neutron library shared by all Neutron sub-projects.

This package contains the documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
rm -f *requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%py2_install
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/%{module}-*.egg-info
%exclude %{python2_sitelib}/%{module}/tests

%files tests
%license LICENSE
%{python2_sitelib}/%{module}/tests

%files doc
%license LICENSE
%doc doc/build/html README.rst

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 1.9.1-1
- Update to 1.9.1

