%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname novaclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:             python-novaclient
Epoch:            1
Version:          9.1.1
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Nova
License:          ASL 2.0
URL:              https://launchpad.net/python-novaclient
Source0:          %{name}-%{version}.tar.gz
BuildArch:        noarch

%description
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python2-novaclient}

BuildRequires:    python2-devel
BuildRequires:    python-pbr
BuildRequires:    git
BuildRequires:    python-setuptools
BuildRequires:    python-dateutil

Requires:         python-babel >= 2.3.4
Requires:         python-iso8601 >= 0.1.11
Requires:         python-keystoneauth1 >= 3.1.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-pbr >= 2.0.0
Requires:         python-prettytable >= 0.7.1
Requires:         python-requests
Requires:         python-simplejson >= 2.2.0
Requires:         python-six >= 1.9.0

%description -n python2-%{sname}
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python3-novaclient}

BuildRequires:    python3-devel
BuildRequires:    python3-pbr
BuildRequires:    python3-setuptools

Requires:         python3-babel >= 2.3.4
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-keystoneauth1 >= 3.1.0
Requires:         python3-oslo-i18n >= 2.1.0
Requires:         python3-oslo-serialization >= 1.10.0
Requires:         python3-oslo-utils >= 3.20.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-prettytable >= 0.7.1
Requires:         python3-requests
Requires:         python3-simplejson >= 2.2.0
Requires:         python3-six >= 1.9.0

%description -n python3-%{sname}
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.
%endif

%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-oslo-utils
BuildRequires:    python-keystoneauth1
BuildRequires:    python-oslo-serialization
BuildRequires:    python-prettytable

%description      doc
This is a client for the OpenStack Nova API. There's a Python API (the
novaclient module), and a command-line script (nova). Each implements 100% of
the OpenStack Nova API.

This package contains auto-generated documentation.

%package          sdk
Summary:          SDK files for %{name}

%description      sdk
Contains SDK files for %{name} package

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the requirements
rm -f test-requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
export PBR_VERSION=%{version}
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

# prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients/%{name}
tar zcf %{buildroot}/usr/share/remote-clients/%{name}/%{name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. %{name}-%{version}

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

%files sdk
/usr/share/remote-clients/%{name}/%{name}-%{version}.tgz

%changelog
* Fri Oct 06 2017 rdo-trunk <javier.pena@redhat.com> 1:9.1.1-1
- Update to 9.1.1

* Mon Aug 14 2017 Alfredo Moralejo <amoralej@redhat.com> 1:9.1.0-1
- Update to 9.1.0

