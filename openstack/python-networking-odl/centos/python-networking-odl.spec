%global drv_vendor OpenDaylight
%global pkgname networking-odl
%global srcname networking_odl
%global docpath doc/build/html

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           python-%{pkgname}
Epoch:          1
Version:        11.0.0
Release:        0%{?_tis_dist}.%{tis_patch_ver}
Summary:        %{drv_vendor} OpenStack Neutron driver

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-mock
#BuildRequires:  python-neutron-tests
BuildRequires:  python-openstackdocstheme
#BuildRequires:  python-oslotest
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-pbr
BuildRequires:  python-sphinx
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel

Requires:       openstack-neutron-ml2
Requires:       python-babel
Requires:       python-pbr
Requires:       python-websocket-client
Requires:       python-stevedore
Requires:       python-neutron-lib
Requires:       python-debtcollector

%description
This package contains %{drv_vendor} networking driver for OpenStack Neutron.


%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove gate hooks
rm -rf %{srcname}/tests/contrib

%build
export PBR_VERSION=%{version}
rm requirements.txt test-requirements.txt
%{__python2} setup.py build
%{__python2} setup.py build_sphinx -b html
rm %{docpath}/.buildinfo

%py2_build_wheel

#%check
#%{__python2} setup.py testr


%install
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

%files
%license LICENSE
%doc %{docpath}
%{_bindir}/neutron-odl-ovs-hostconfig
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 1:11.0.0-1
- Update to 11.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 1:11.0.0-0.1.0rc2
- Update to 11.0.0.0rc2

