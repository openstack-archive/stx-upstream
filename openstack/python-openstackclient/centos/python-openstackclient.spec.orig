%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

# Python3 support in OpenStack starts with version 3.5,
# which is only in Fedora 24+
%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global client openstackclient
%global with_doc 1

%global common_desc \
python-openstackclient is a unified command-line client for the OpenStack APIs. \
It is a thin wrapper to the stock python-*client modules that implement the \
actual REST API client actions.

Name:             python-openstackclient
Version:          3.16.2
Release:          1%{?dist}
Summary:          OpenStack Command-line Client

License:          ASL 2.0
URL:              http://launchpad.net/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    openstack-macros

%description
%{common_desc}

%package -n python2-%{client}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python2-%{client}}

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pbr
BuildRequires:    python2-six
BuildRequires:    python2-oslo-i18n
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-requests
BuildRequires:    python2-glanceclient
BuildRequires:    python2-keystoneclient
BuildRequires:    python2-novaclient
BuildRequires:    python2-cinderclient
BuildRequires:    python2-mock
BuildRequires:    python2-os-client-config
%if 0%{?fedora} > 0
BuildRequires:    python2-d2to1
BuildRequires:    python2-cliff
BuildRequires:    python2-simplejson
BuildRequires:    python2-requests-mock
%else
BuildRequires:    python-d2to1
BuildRequires:    python-cliff
BuildRequires:    python-simplejson
BuildRequires:    python-requests-mock
%endif
# Required to compile translation files
BuildRequires:    python2-babel
# Required for unit tests
BuildRequires:    python2-os-testr
BuildRequires:    python2-osc-lib-tests
BuildRequires:    python2-fixtures
BuildRequires:    python2-oslotest
BuildRequires:    python2-reno
BuildRequires:    python2-requestsexceptions
BuildRequires:    python2-openstacksdk
BuildRequires:    python2-osprofiler

Requires:         python2-pbr
Requires:         python2-babel
Requires:         python2-openstacksdk >= 0.11.2
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-glanceclient >= 1:2.8.0
Requires:         python2-keystoneauth1 >= 3.4.0
Requires:         python2-keystoneclient >= 1:3.17.0
Requires:         python2-novaclient >= 9.1.0
Requires:         python2-cinderclient >= 3.3.0
Requires:         python2-neutronclient >= 6.7.0
Requires:         python2-six >= 1.10.0
Requires:         python2-osc-lib >= 1.10.0
%if 0%{?fedora} > 0
Requires:         python2-cliff
%else
Requires:         python-cliff
%endif
Requires:         python-%{client}-lang = %{version}-%{release}


%description -n python2-%{client}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{client}-doc
Summary:          Documentation for OpenStack Command-line Client

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-sphinxcontrib-apidoc

Requires:         %{name} = %{version}-%{release}

%description -n python-%{client}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package  -n python-%{client}-lang
Summary:   Translation files for Openstackclient

%description -n python-%{client}-lang
Translation files for Openstackclient

%if 0%{?with_python3}
%package -n python3-%{client}
Summary:    OpenStack Command-line Client
%{?python_provide:%python_provide python3-%{client}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-d2to1
BuildRequires:    python3-oslo-sphinx
BuildRequires:    python3-six
BuildRequires:    python3-cliff
BuildRequires:    python3-oslo-i18n
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-simplejson
BuildRequires:    python3-requests
BuildRequires:    python3-glanceclient
BuildRequires:    python3-keystoneclient
BuildRequires:    python3-novaclient
BuildRequires:    python3-cinderclient
BuildRequires:    python3-mock
BuildRequires:    python3-requests-mock
BuildRequires:    python3-os-client-config
# Required to compile translation files
BuildRequires:    python3-babel
# Required for unit tests
BuildRequires:    python3-os-testr
BuildRequires:    python3-osc-lib-tests
BuildRequires:    python3-coverage
BuildRequires:    python3-fixtures
BuildRequires:    python3-oslotest
BuildRequires:    python3-reno
BuildRequires:    python3-requestsexceptions
BuildRequires:    python3-openstacksdk
BuildRequires:    python3-osprofiler

Requires:         python3-pbr
Requires:         python3-babel
Requires:         python3-cliff
Requires:         python3-openstacksdk >= 0.11.2
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-glanceclient >= 1:2.8.0
Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-keystoneclient >= 1:3.17.0
Requires:         python3-novaclient >= 9.1.0
Requires:         python3-cinderclient >= 3.3.0
Requires:         python3-neutronclient >= 6.7.0
Requires:         python3-six >= 1.10.0
Requires:         python3-osc-lib >= 1.10.0
Requires:         python-%{client}-lang = %{version}-%{release}

%description -n python3-%{client}
%{common_desc}
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# We handle requirements ourselves, pkg_resources only bring pain
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/openstackclient/locale

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/openstack %{buildroot}%{_bindir}/openstack-%{python3_version}
ln -s ./openstack-%{python3_version} %{buildroot}%{_bindir}/openstack-3
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
ln -s ./openstack %{buildroot}%{_bindir}/openstack-2
ln -s ./openstack %{buildroot}%{_bindir}/openstack-%{python2_version}

%if 0%{?with_doc}
sphinx-build -b html doc/source doc/build/html
sphinx-build -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/openstack.1 %{buildroot}%{_mandir}/man1/openstack.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*/LC_*/openstackclient*po
rm -f %{buildroot}%{python2_sitelib}/openstackclient/locale/*pot
mv %{buildroot}%{python2_sitelib}/openstackclient/locale %{buildroot}%{_datadir}/locale

%if 0%{?with_python3}
rm -rf %{buildroot}%{python3_sitelib}/openstackclient/locale
%endif

# Find language files
%find_lang openstackclient --all-name

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{client}
%license LICENSE
%doc README.rst
%{_bindir}/openstack
%{_bindir}/openstack-2
%{_bindir}/openstack-%{python2_version}
%{python2_sitelib}/openstackclient
%{python2_sitelib}/*.egg-info
%if 0%{?with_doc}
%{_mandir}/man1/openstack.1*

%files -n python-%{client}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{client}-lang -f openstackclient.lang
%license LICENSE

%if 0%{?with_python3}
%files -n python3-%{client}
%license LICENSE
%doc README.rst
%{_bindir}/openstack-3
%{_bindir}/openstack-%{python3_version}
%{python3_sitelib}/openstackclient
%{python3_sitelib}/*.egg-info
%endif
%changelog
* Tue Nov 27 2018 RDO <dev@lists.rdoproject.org> 3.16.2-1
- Update to 3.16.2

* Thu Sep 20 2018 RDO <dev@lists.rdoproject.org> 3.16.1-1
- Update to 3.16.1

* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 3.16.0-1
- Update to 3.16.0

