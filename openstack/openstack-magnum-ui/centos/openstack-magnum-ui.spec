%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global library magnum-ui
%global module magnum_ui

Name:       openstack-%{library}
Version:    3.0.0
Release:    1%{?_tis_dist}.%{tis_patch_ver}
Summary:    OpenStack Magnum UI Horizon plugin
License:    ASL 2.0
URL:        http://launchpad.net/%{library}/

Source0:    https://tarballs.openstack.org/%{library}/%{library}-%{upstream_version}.tar.gz

BuildArch:  noarch

BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  git

Requires:   python-pbr
Requires:   python-babel
Requires:   python-magnumclient >= 2.0.0
Requires:   openstack-dashboard >= 8.0.0
Requires:   python-django >= 1.8
Requires:   python-django-babel
Requires:   python-django-compressor >= 2.0
Requires:   python-django-openstack-auth >= 3.5.0
Requires:   python-django-pyscss >= 2.0.2

%description
OpenStack Magnum UI Horizon plugin

# Documentation package
%package -n python-%{library}-doc
Summary:    OpenStack example library documentation

BuildRequires: python-sphinx
BuildRequires: python-django
BuildRequires: python-django-nose
BuildRequires: openstack-dashboard
BuildRequires: python-openstackdocstheme
BuildRequires: python-magnumclient
BuildRequires: python-mock
BuildRequires: python-mox3

%description -n python-%{library}-doc
OpenStack Magnum UI Horizon plugin documentation

This package contains the documentation.

%prep
%autosetup -n %{library}-%{upstream_version} -S git
# Let's handle dependencies ourseleves
rm -f *requirements.txt


%build
export PBR_VERSION=%{version}
%{__python2} setup.py build
%py2_build_wheel

# generate html docs
export PYTHONPATH=/usr/share/openstack-dashboard
#%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
#rm -rf doc/build/html/.{doctrees,buildinfo}

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Move config to horizon
install -p -D -m 640 %{module}/enabled/_1370_project_container_infra_panel_group.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1370_project_container_infra_panel_group.py
install -p -D -m 640 %{module}/enabled/_1371_project_container_infra_clusters_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1371_project_container_infra_clusters_panel.py
install -p -D -m 640 %{module}/enabled/_1372_project_container_infra_cluster_templates_panel.py %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_1372_project_container_infra_cluster_templates_panel.py


%files
%license LICENSE
%{python2_sitelib}/%{module}
%{python2_sitelib}/*.egg-info
%{_datadir}/openstack-dashboard/openstack_dashboard/local/enabled/_137*

%files -n python-%{library}-doc
%license LICENSE
#%doc doc/build/html README.rst

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*


%changelog
* Thu Aug 24 2017 Alfredo Moralejo <amoralej@redhat.com> 3.0.0-1
- Update to 3.0.0

