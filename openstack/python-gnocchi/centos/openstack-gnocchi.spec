%global pypi_name gnocchi
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service gnocchi

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           %{service}
Version:        4.2.5
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        Gnocchi is a API to store metrics and index resources

License:        ASL 2.0
URL:            http://github.com/gnocchixyz/%{service}
Source0:        https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        %{pypi_name}-dist.conf
Source10:       %{name}-api.service
Source11:       %{name}-metricd.service
Source12:       %{name}-statsd.service
# WRS
Source13:       gnocchi-api.init
Source14:       gnocchi-metricd.init
# Include patches here
Patch1:         Integrate-gnocchi-storage-backend.patch

BuildArch:      noarch

BuildRequires:  python2-setuptools
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
BuildRequires:  python2-sphinx
BuildRequires:  python2-pbr
BuildRequires:  python2-devel
BuildRequires:  systemd
BuildRequires:  python2-tenacity >= 4.0.0
BuildRequires:  openstack-macros

%description
HTTP API to store metrics and index resources.

%package -n     python-%{service}
Summary:        %{service} python libraries

Requires:       numpy >= 1.9.0
Requires:       python2-daiquiri
Requires:       python-futures
Requires:       python2-iso8601
Requires:       python2-jinja2
Requires:       python2-keystonemiddleware >= 4.0.0
Requires:       python2-lz4 >= 0.9.0
Requires:       python-monotonic
Requires:       python-msgpack
Requires:       python2-oslo-config >= 2:3.22.0
Requires:       python2-oslo-db >= 4.17.0
Requires:       python2-oslo-log >= 2.3.0
Requires:       python2-oslo-middleware >= 3.22.0
Requires:       python2-oslo-policy >= 0.3.0
Requires:       python2-oslo-sphinx >= 2.2.0
Requires:       python2-oslo-serialization >= 1.4.0
Requires:       python2-pandas >= 0.18.0
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python2-pbr
Requires:       python2-pecan >= 0.9
Requires:       python-pytimeparse >= 1.1.5
Requires:       python2-requests
Requires:       python2-scipy
Requires:       python2-swiftclient >= 3.1.0
Requires:       python2-six
Requires:       python2-sqlalchemy
Requires:       python-sqlalchemy-utils
Requires:       python2-stevedore
Requires:       python-sysv_ipc
Requires:       python-tooz >= 0.30
Requires:       python-trollius
Requires:       python2-tenacity >= 4.0.0
Requires:       python2-ujson
Requires:       python-voluptuous
Requires:       python-werkzeug
Requires:       python2-pytz
Requires:       PyYAML
Requires:       python-webob >= 1.4.1
Requires:       python-alembic
Requires:       python-psycopg2
Requires:       python2-prettytable
Requires:       python2-cotyledon >= 1.5.0
Requires:       python2-jsonpatch
Requires:       python-cachetools
Requires:       python2-pyparsing

%description -n   python-%{service}
%{service} provides API to store metrics from components
and index resources.

This package contains the %{service} python library.


%package        api

Summary:        %{service} api

Requires:       %{name}-common = %{version}-%{release}
Obsoletes:      openstack-%{service}-api < 4.1.3
Provides:       openstack-%{service}-api = %{version}-%{release}

%description api
%{service} provides API to store metrics from components
and index resources.

This package contains the %{service} API service.

%package        common
Summary:        Components common to all %{service} services

# Config file generation
BuildRequires:    python2-daiquiri
BuildRequires:    python2-jsonpatch
BuildRequires:    python2-oslo-config >= 2:3.22.0
BuildRequires:    python2-oslo-concurrency
BuildRequires:    python2-oslo-db
BuildRequires:    python2-oslo-log
BuildRequires:    python2-oslo-messaging
BuildRequires:    python2-oslo-policy
BuildRequires:    python2-oslo-reports
BuildRequires:    python2-oslo-service
BuildRequires:    python2-lz4 >= 0.9.0
BuildRequires:    python2-pandas >= 0.18.0
BuildRequires:    python2-pecan >= 0.9
BuildRequires:    python-pytimeparse >= 1.1.5
BuildRequires:    python-tooz
BuildRequires:    python2-ujson
BuildRequires:    python-werkzeug
BuildRequires:    python2-gnocchiclient >= 2.1.0

Requires:         python-%{service} = %{version}-%{release}
Requires(pre):    shadow-utils

Provides:         openstack-%{service}-common = %{version}-%{release}
Obsoletes:        openstack-%{service}-common < 4.1.3

Obsoletes:        openstack-%{service}-carbonara

# openstack-gnocchi-indexer-sqlalchemy is removed and merged into common
Provides:         openstack-%{service}-indexer-sqlalchemy = %{version}-%{release}
Obsoletes:        openstack-%{service}-indexer-sqlalchemy < 4.1.3

# Obsolete old openstack-gnocchi packages

%description    common
%{service} provides services to measure and
collect metrics from components.

%package        metricd

Summary:        %{service} metricd daemon

Requires:       %{name}-common = %{version}-%{release}

Obsoletes:      openstack-%{service}-metricd < 4.1.3
Provides:       openstack-%{service}-metricd = %{version}-%{release}

%description metricd
%{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} metricd daemon


%package        statsd

Summary:        %{service} statsd daemon

Requires:       %{name}-common = %{version}-%{release}

Obsoletes:      openstack-%{service}-statsd < 4.1.3
Provides:       openstack-%{service}-statsd = %{version}-%{release}

%description statsd
%{service} provides API to store metrics from OpenStack
components and index resources.

This package contains the %{service} statsd daemon

%package -n python-%{service}-tests
Summary:        Gnocchi tests
Requires:       python-%{service} = %{version}-%{release}
Requires:       python2-gabbi >= 1.30.0

%description -n python-%{service}-tests
This package contains the Gnocchi test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for %{service}

Requires:         python-%{service} = %{version}-%{release}

Provides:         openstack-%{service}-doc = %{version}-%{release}
Obsoletes:        openstack-%{service}-doc < 4.1.3

%description      doc
%{service} provides services to measure and
collect metrics from components.

This package contains documentation files for %{service}.
%endif


%prep
%setup -q -n %{service}-%{upstream_version}

# Apply patches here
%patch1 -p1

find . \( -name .gitignore -o -name .placeholder \) -delete
find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +
sed -i '/setup_requires/d; /install_requires/d; /dependency_links/d' setup.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=%{service}/%{service}-config-generator.conf --output-file=%{service}/%{service}.conf

export PBR_VERSION=%{version}
%{__python2} setup.py build

# Programmatically update defaults in sample config
# which is installed at /etc/gnocchi/gnocchi.conf
# TODO: Make this more robust
# Note it only edits the first occurrence, so assumes a section ordering in sample
# and also doesn't support multi-valued variables.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -i "0,/^# *$name=/{s!^# *$name=.*!#$name=$value!}" %{service}/%{service}.conf
done < %{SOURCE1}

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/
mkdir -p %{buildroot}/%{_var}/log/%{name}
# WRS
mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -p -D -m 640 %{service}/rest/wsgi.py %{buildroot}%{_datadir}/%{service}/%{service}-api.py
install -p -D -m 775 %{SOURCE13} %{buildroot}%{_sysconfdir}/init.d/gnocchi-api
install -p -D -m 775 %{SOURCE14} %{buildroot}%{_sysconfdir}/init.d/gnocchi-metricd

install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf
install -p -D -m 640 %{service}/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf

#TODO(prad): build the docs at run time, once the we get rid of postgres setup dependency

# Configuration
cp -R %{service}/rest/policy.json %{buildroot}/%{_sysconfdir}/%{service}

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}

# Install systemd unit services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/%{name}-metricd.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/%{name}-statsd.service

# Backward compatibility unit services
ln -sf %{_unitdir}/%{name}-api.service %{buildroot}%{_unitdir}/openstack-%{name}-api.service
ln -sf %{_unitdir}/%{name}-metricd.service %{buildroot}%{_unitdir}/openstack-%{name}-metricd.service
ln -sf %{_unitdir}/%{name}-statsd.service %{buildroot}%{_unitdir}/openstack-%{name}-statsd.service

# Remove all of the conf files that are included in the buildroot/usr/etc dir since we installed them above
rm -f %{buildroot}/usr/etc/%{service}/*

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
if ! getent passwd %{service} >/dev/null; then
  useradd -r -g %{service} -G %{service},nobody -d %{_sharedstatedir}/%{service} -s /sbin/nologin -c "%{service} Daemons" %{service}
fi
exit 0

%files -n python-%{service}
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%files api
%defattr(-,root,root,-)
%{_bindir}/%{service}-api
%{_unitdir}/%{name}-api.service
%{_unitdir}/openstack-%{name}-api.service
%{_sysconfdir}/init.d/gnocchi-api

%files common
%{_bindir}/%{service}-config-generator
%{_bindir}/%{service}-change-sack-size
%{_bindir}/%{service}-upgrade
%dir %{_sysconfdir}/%{service}
%{_datadir}/%{service}/%{service}-api.*
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%config(noreplace) %attr(-, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%dir %attr(0750, %{service}, root)  %{_localstatedir}/log/%{service}

%defattr(-, %{service}, %{service}, -)
%dir %{_sharedstatedir}/%{service}
%dir %{_sharedstatedir}/%{service}/tmp

%files metricd
%{_bindir}/%{service}-metricd
%{_unitdir}/%{name}-metricd.service
%{_unitdir}/openstack-%{name}-metricd.service
%{_sysconfdir}/init.d/gnocchi-metricd

%files statsd
%{_bindir}/%{service}-statsd
%{_unitdir}/%{name}-statsd.service
%{_unitdir}/openstack-%{name}-statsd.service

%if 0%{?with_doc}
%files doc
%doc doc/source/
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Tue Mar 27 2018 Jon Schlueter <jschluet@redhat.com> 4.2.1-1
- Update to 4.2.1

* Wed Feb 21 2018 RDO <dev@lists.rdoproject.org> 4.2.0-1
- Update to 4.2.0
