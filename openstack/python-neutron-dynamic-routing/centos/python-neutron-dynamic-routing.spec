%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name neutron-dynamic-routing
%global sname neutron_dynamic_routing
%global service neutron

Name:           python-%{pypi_name}
Version:        11.0.0
Release:        0%{?_tis_dist}.%{tis_patch_ver}
Summary:        Dynamic routing services for OpenStack Neutron.

License:        ASL 2.0
URL:            https://github.com/openstack/neutron-dynamic-routing
Source0:        %{name}-%{version}.tar.gz

# WRS
Source1:       neutron-bgp-dragent.init
Source2:       neutron-bgp-dragent.service
Source3:       neutron-bgp-dragent.pmon

BuildArch:      noarch

BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python2-devel

%description
Neutron dynamic routing enables advertisement of self-service (private) network prefixes
to physical network devices that support dynamic routing protocols such as routers, thus
removing the conventional dependency on static routes.

%package -n     python2-%{pypi_name}
Summary:        Dynamic routing services for OpenStack Neutron.

Requires:       python-pbr >= 1.6
Requires:       python-eventlet >= 0.18.4
Requires:       python-httplib2 >= 0.7.5
Requires:       python-netaddr >= 0.7.18
Requires:       python-six >= 1.9.0
Requires:       python-neutron-lib >= 0.4.0
Requires:       python-oslo-config >= 3.14.0
Requires:       python-oslo-db >= 4.13.3
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 5.2.0
Requires:       python-oslo-serialization >= 1.10.0
Requires:       python-oslo-service >= 1.10.0
Requires:       python-oslo-utils >= 3.16.0

%description -n python2-%{pypi_name}
Neutron dynamic routing enables advertisement of self-service (private) network prefixes
to physical network devices that support dynamic routing protocols such as routers, thus

%package -n python-%{pypi_name}-doc
Summary:    neutron-dynamic-routing documentation
%description -n python-%{pypi_name}-doc
Documentation for neutron-dynamic-routing

%package -n python-%{pypi_name}-tests
Summary:    neutron-dynamic-routing tests
Requires:   python-%{pypi_name} = %{version}-%{release}
%description -n python-%{pypi_name}-tests
neutron-dynamic-routing set of tests

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
export PBR_VERSION=%{version}
%py2_build
# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/oslo-config-generator/bgp_dragent.ini
# generate html docs
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%py2_build_wheel

%install
export PBR_VERSION=%{version}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/neutron-bgp-dragent.service
install -d %{buildroot}%{_sysconfdir}/init.d
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/init.d/neutron-bgp-dragent
install -d %{buildroot}%{_sysconfdir}/%{service}/pmon
install -m 755 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{service}/pmon/neutron-bgp-dragent.conf
%py2_install
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

mkdir -p %{buildroot}%{_sysconfdir}/%{service}/policy.d
mv %{buildroot}/usr/etc/%{service}/policy.d/dynamic_routing.conf %{buildroot}%{_sysconfdir}/%{service}/policy.d/
mv etc/bgp_dragent.ini.sample %{buildroot}%{_sysconfdir}/%{service}/bgp_dragent.ini


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/%{sname}-*.egg-info
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.d/dynamic_routing.conf
%{_bindir}/neutron-bgp-dragent
%exclude %{python2_sitelib}/%{sname}/tests
%{_unitdir}/neutron-bgp-dragent.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/pmon/neutron-bgp-dragent.conf
%{_sysconfdir}/init.d/%{service}-bgp-dragent
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/bgp_dragent.ini


%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%files -n python-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{sname}/tests

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*


%changelog
* Mon Mar 13 2017 Matt Peters <matt.peters@windriver.com> 9.2.0-0
- Initial Version
