%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global pypi_name networking-bgpvpn
%global sname networking_bgpvpn
%global service neutron

Name:           python-%{pypi_name}
Version:        7.0.0
Release:        0%{?_tis_dist}.%{tis_patch_ver}
Summary:        API and Framework to interconnect bgpvpn to neutron networks

License:        ASL 2.0
URL:            https://github.com/openstack/networking-bgpvpn
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python-webob
BuildRequires:  python-webtest
BuildRequires:  python-coverage
BuildRequires:  python-hacking
BuildRequires:  python-neutron-tests
BuildRequires:  python-neutron
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-oslotest
BuildRequires:  python-openstackclient
BuildRequires:  python-openvswitch
BuildRequires:  python-pbr
BuildRequires:  python-reno
BuildRequires:  python-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python-sphinx
BuildRequires:  python-subunit
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
BuildRequires:  python-testscenarios
BuildRequires:  python-testtools
BuildRequires:  python2-devel

%description
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are
widely used Wide Area Networking technologies. The primary purpose of this
project is to allow attachment of Neutron networks and/or routers to carrier
provided.

%package -n     python2-%{pypi_name}
Summary:        API and Framework to interconnect bgpvpn to neutron networks
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python-pbr >= 1.6
Requires:       python-babel >= 2.3.4
Requires:       python-neutron-lib >= 0.4.0
Requires:       python-oslo-config >= 2.3.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-db >= 2.4.1
Requires:       python-oslo-log >= 1.8.0
Requires:       python-oslo-utils >= 2.0.0
Requires:       python-setuptools

%description -n python2-%{pypi_name}
BGPMPLS VPN Extension for OpenStack Networking This project provides an API and
Framework to interconnect BGP/MPLS VPNs to Openstack Neutron networks, routers
and ports.The Border Gateway Protocol and MultiProtocol Label Switching are
widely used Wide Area Networking technologies. The primary purpose of this
project is to allow attachment of Neutron networks and/or routers to carrier
provided.

%package -n python-%{pypi_name}-doc
Summary:        networking-bgpvpn documentation
%description -n python-%{pypi_name}-doc
Documentation for networking-bgpvpn

%package -n python-%{pypi_name}-tests
Summary:        networking-bgpvpn tests
Requires:   python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-tests
Networking-bgpvpn set of tests

%package -n python-%{pypi_name}-dashboard
Summary:    networking-bgpvpn dashboard
Requires: python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-dashboard
Dashboard to be able to handle BGPVPN functionality via Horizon

%package -n python-%{pypi_name}-heat
Summary:    networking-bgpvpn heat
Requires: python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-heat
Networking-bgpvpn heat resources

%prep
%autosetup -n %{name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
export PBR_VERSION=%{version}
%py2_build
# generate html docs
# TODO: the doc generation is commented until python-sphinxcontrib-* packages
# are included in CBS. This needs to be fixed.
#%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%py2_install
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

mkdir -p %{buildroot}%{_sysconfdir}/%{service}/policy.d
mv %{buildroot}/usr/etc/neutron/networking_bgpvpn.conf %{buildroot}%{_sysconfdir}/%{service}/
mv %{buildroot}/usr/etc/neutron/policy.d/bgpvpn.conf %{buildroot}%{_sysconfdir}/%{service}/policy.d/

# Make sure neutron-server loads new configuration file
mkdir -p %{buildroot}/%{_datadir}/neutron/server
ln -s %{_sysconfdir}/%{service}/networking_bgpvpn.conf %{buildroot}%{_datadir}/%{service}/server/networking_bgpvpn.conf


%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/networking_bgpvpn-*.egg-info
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/networking_bgpvpn.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.d/bgpvpn.conf
%{_datadir}/%{service}/server/networking_bgpvpn.conf
%exclude %{python2_sitelib}/%{sname}/tests
%exclude %{python2_sitelib}/bgpvpn_dashboard
%exclude %{python2_sitelib}/networking_bgpvpn_heat
%exclude %{python2_sitelib}/networking_bgpvpn_tempest

%files -n python-%{pypi_name}-doc
#%doc html
%license LICENSE

%files -n python-%{pypi_name}-tests
%license LICENSE
%doc networking_bgpvpn_tempest/README.rst
%{python2_sitelib}/networking_bgpvpn_tempest
%{python2_sitelib}/%{sname}/tests

%files -n python-%{pypi_name}-dashboard
%license LICENSE
%{python2_sitelib}/bgpvpn_dashboard/

%files -n python-%{pypi_name}-heat
%license LICENSE
%{python2_sitelib}/networking_bgpvpn_heat

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Mon Mar 13 2017 Matt Peters <matt.peters@windriver.com> 5.0.0-0
- Initial Version based on CentOS distribution.
