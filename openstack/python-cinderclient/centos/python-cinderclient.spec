%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname cinderclient
%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
Client library (cinderclient python module) and command line utility \
(cinder) for interacting with OpenStack Cinder (Block Storage) API.

Name:             python-cinderclient
Version:          4.0.1
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          Python API and CLI for OpenStack Cinder

License:          ASL 2.0
URL:              http://github.com/openstack/python-cinderclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:        noarch

BuildRequires:    git

%description
%{common_desc}

%package -n python2-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python2-%{sname}}

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pip
BuildRequires:    python2-wheel
BuildRequires:    python2-pbr
%if 0%{?fedora} > 0
BuildRequires:    python2-d2to1
%else
BuildRequires:    python-d2to1
%endif

Requires:         python2-babel
Requires:         python2-pbr
Requires:         python2-prettytable
Requires:         python2-requests
Requires:         python2-six
Requires:         python2-keystoneauth1 >= 3.4.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-utils >= 3.33.0
%if 0%{?fedora} > 0
Requires:         python2-simplejson
%else
Requires:         python-simplejson
%endif

%description -n python2-%{sname}
%{common_desc}


%if 0%{?with_python3}
%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Cinder
%{?python_provide:%python_provide python3-%{sname}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-d2to1

Requires:         python3-babel
Requires:         python3-pbr
Requires:         python3-prettytable
Requires:         python3-requests
Requires:         python3-setuptools
Requires:         python3-simplejson
Requires:         python3-six
Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-oslo-i18n >= 3.15.3
Requires:         python3-oslo-utils >= 3.33.0

%description -n python3-%{sname}
%{common_desc}
%endif


%package doc
Summary:          Documentation for OpenStack Cinder API Client
Group:            Documentation

BuildRequires:    python-reno
BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme

%description      doc
%{common_desc}

This package contains auto-generated documentation.


%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Remove bundled egg-info
rm -rf python_cinderclient.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
export PBR_VERSION=%{version}
%py2_build
%py2_build_wheel
%if 0%{?with_python3}
%py3_build
%endif

sphinx-build -W -b html doc/source doc/build/html
sphinx-build -W -b man doc/source doc/build/man

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

%install
export PBR_VERSION=%{version}
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/cinder %{buildroot}%{_bindir}/cinder-%{python3_version}
ln -s ./cinder-%{python3_version} %{buildroot}%{_bindir}/cinder-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/cinderclient/tests
%endif

%py2_install
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/
mv %{buildroot}%{_bindir}/cinder %{buildroot}%{_bindir}/cinder-%{python2_version}
ln -s ./cinder-%{python2_version} %{buildroot}%{_bindir}/cinder-2
# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/cinderclient/tests

ln -s ./cinder-2 %{buildroot}%{_bindir}/cinder

install -p -D -m 644 tools/cinder.bash_completion %{buildroot}%{_sysconfdir}/bash_completion.d/cinder.bash_completion

install -p -D -m 644 doc/build/man/cinder.1 %{buildroot}%{_mandir}/man1/cinder.1

# prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients
tar zcf %{buildroot}/usr/share/remote-clients/%{name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. %{name}-%{version}


%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder
%{_bindir}/cinder-2*
%{python2_sitelib}/cinderclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d/cinder.bash_completion
%{_mandir}/man1/cinder.1*

%if 0%{?with_python3}
%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{_bindir}/cinder-3*
%{python3_sitelib}/cinderclient
%{python3_sitelib}/*.egg-info
%endif

%files doc
%doc doc/build/html

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
* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 4.0.1-1
- Update to 4.0.1

