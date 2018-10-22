%global pypi_name distributedcloud-client

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?fedora}
%global with_python3 1
%{!?python3_shortver: %global python3_shortver %(%{__python3} -c 'import sys; print(str(sys.version_info.major) + "." + str(sys.version_info.minor))')}
%endif

Name:          %{pypi_name}
Version:       1.0.0
Release:       1%{?_tis_dist}.%{tis_patch_ver}
Summary:       Client Library for Distributed Cloud Services

License:       ASL 2.0
URL:           unknown
Source0:       %{pypi_name}-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python2-pip
BuildRequires: python2-wheel
BuildRequires: python-jsonschema >= 2.0.0
BuildRequires: python-keystonemiddleware
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config
BuildRequires: python-oslo-context
BuildRequires: python-oslo-db
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-log
BuildRequires: python-oslo-messaging
BuildRequires: python-oslo-middleware
BuildRequires: python-oslo-policy
BuildRequires: python-oslo-rootwrap
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-service
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-versionedobjects
BuildRequires: python-pbr >= 1.8
BuildRequires: python-routes >= 1.12.3
BuildRequires: python-sphinx
BuildRequires: python-sphinxcontrib-httpdomain
BuildRequires: pyOpenSSL
BuildRequires: systemd
BuildRequires: git
# Required to compile translation files
BuildRequires: python-babel

%description
Client library for Distributed Cloud built on the Distributed Cloud API. It
provides a command-line tool (dcmanager).

Distributed Cloud provides configuration and management of distributed clouds

# DC Manager
%package dcmanagerclient
Summary: DC Manager Client

%description dcmanagerclient
Distributed Cloud Manager Client

%package          sdk
Summary:          SDK files for %{pypi_name}

%description      sdk
Contains SDK files for %{pypi_name} package

%prep
%autosetup -n %{pypi_name}-%{version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
export PBR_VERSION=%{version}
%{__python2} setup.py build
%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# prep SDK package
mkdir -p %{buildroot}/usr/share/remote-clients
tar zcf %{buildroot}/usr/share/remote-clients/%{pypi_name}-%{version}.tgz --exclude='.gitignore' --exclude='.gitreview' -C .. --transform="s/%{name}-%{version}/%{pypi_name}-%{version}/" %{name}-%{version}

%files dcmanagerclient
%license LICENSE
%{python2_sitelib}/dcmanagerclient*
%{python2_sitelib}/distributedcloud_client-*.egg-info
%exclude %{python2_sitelib}/dcmanagerclient/tests
%{_bindir}/dcmanager*

%files sdk
/usr/share/remote-clients/%{pypi_name}-%{version}.tgz

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*
