%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname novaclient

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
This is a client for the OpenStack Nova API. There's a Python API (the \
novaclient module), and a command-line script (nova). Each implements 100% of \
the OpenStack Nova API.

Name:             python-novaclient
Epoch:            1
Version:          11.0.0
Release:          1%{?dist}
Summary:          Python API and CLI for OpenStack Nova
License:          ASL 2.0
URL:              https://launchpad.net/%{name}
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:        noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%description
%{common_desc}

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python2-novaclient}

BuildRequires:    python2-devel
BuildRequires:    python2-pbr
BuildRequires:    python2-setuptools

Requires:         python2-babel >= 2.3.4
Requires:         python2-iso8601 >= 0.1.11
Requires:         python2-keystoneauth1 >= 3.4.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-serialization >= 2.18.0
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-pbr >= 2.0.0
Requires:         python2-prettytable >= 0.7.2
Requires:         python-simplejson >= 3.5.1
Requires:         python2-six >= 1.10.0

%description -n python2-%{sname}
%{common_desc}

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python3-novaclient}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:         python3-babel >= 2.3.4
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-utils >= 3.33.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-prettytable >= 0.7.2
Requires:         python3-simplejson >= 3.5.1
Requires:         python3-six >= 1.10.0

%description -n python3-%{sname}
%{common_desc}
%endif

%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python2-sphinx
BuildRequires:    python2-openstackdocstheme
BuildRequires:    python2-oslo-utils
BuildRequires:    python2-keystoneauth1
BuildRequires:    python2-oslo-serialization
BuildRequires:    python2-prettytable

%description      doc
%{common_desc}

This package contains auto-generated documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the requirements
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/nova %{buildroot}%{_bindir}/nova-%{python3_version}
ln -s ./nova-%{python3_version} %{buildroot}%{_bindir}/nova-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/novaclient/tests
%endif

%py2_install
mv %{buildroot}%{_bindir}/nova %{buildroot}%{_bindir}/nova-%{python2_version}
ln -s ./nova-%{python2_version} %{buildroot}%{_bindir}/nova-2

ln -s ./nova-2 %{buildroot}%{_bindir}/nova

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/novaclient/tests

%{__python2} setup.py build_sphinx -b html
%{__python2} setup.py build_sphinx -b man

install -p -D -m 644 doc/build/man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%files -n python2-%{sname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{sname}
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz
%{_bindir}/nova
%{_bindir}/nova-2
%{_bindir}/nova-%{python2_version}


%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/nova.1.gz
%{_bindir}/nova-3
%{_bindir}/nova-%{python3_version}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 1:11.0.0-1
- Update to 11.0.0

