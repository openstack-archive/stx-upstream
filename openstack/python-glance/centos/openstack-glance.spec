%global service glance

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}

# WRS: remove docs - for now
%global with_doc 0

%global common_desc \
OpenStack Image Service (code-named Glance) provides discovery, registration, \
and delivery services for virtual disk images. The Image Service API server \
provides a standard REST interface for querying information about virtual disk \
images stored in a variety of back-end stores, including OpenStack Object \
Storage. Clients can register new virtual disk images with the Image Service, \
query for information on publicly available disk images, and use the Image \
Service's client library for streaming virtual disk images.

Name:             openstack-glance
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          15.0.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          OpenStack Image Service

License:          ASL 2.0
URL:              http://glance.openstack.org
Source0:          https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz

#

Source001:         openstack-glance-api.service
Source003:         openstack-glance-registry.service
Source004:         openstack-glance-scrubber.service
Source010:         openstack-glance.logrotate

Source021:         glance-api-dist.conf
Source022:         glance-cache-dist.conf
Source024:         glance-registry-dist.conf
Source025:         glance-scrubber-dist.conf
Source026:         glance-swift.conf

Source030:         glance-sudoers
Source031:         restart-glance
Source032:         glance-purge-deleted-active

BuildArch:        noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python2-pip
BuildRequires:    python2-wheel
BuildRequires:    python-pbr
BuildRequires:    intltool
# Required for config generation
BuildRequires:    openstack-macros
BuildRequires:    python-alembic
BuildRequires:    python-cursive
BuildRequires:    python-crypto
BuildRequires:    python-eventlet
BuildRequires:    python-futurist
BuildRequires:    python-glance-store >= 0.21.0
BuildRequires:    python-httplib2
BuildRequires:    python-oslo-config >= 2:4.0.0
BuildRequires:    python-oslo-log
BuildRequires:    python-oslo-middleware >= 3.27.0
BuildRequires:    python-oslo-policy >= 1.23.0
BuildRequires:    python-oslo-utils >= 3.20.0
BuildRequires:    python-osprofiler
BuildRequires:    python-paste-deploy
BuildRequires:    python-requests
BuildRequires:    python-routes
BuildRequires:    python-oslo-messaging >= 5.24.2
BuildRequires:    python-taskflow >= 2.7.0
BuildRequires:    python-wsme >= 0.8

Requires(pre):    shadow-utils
Requires:         python-glance = %{epoch}:%{version}-%{release}
Requires:         python-glanceclient >= 1:2.8.0

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: python-psutil
BuildRequires: python-mock

%description
%{common_desc}

This package contains the API and registry servers.

%package -n       python-glance
Summary:          Glance Python libraries

Requires:         pysendfile
Requires:         python-cursive
Requires:         python-cryptography >= 1.6
Requires:         python-debtcollector >= 1.2.0
Requires:         python-eventlet >= 0.18.2
Requires:         python-futurist >= 0.11.0
Requires:         python-glance-store >= 0.21.0
Requires:         python-httplib2
Requires:         python-iso8601 >= 0.1.11
Requires:         python-jsonschema
Requires:         python-keystoneauth1 >= 3.1.0
Requires:         python-keystoneclient >= 1:3.8.0
Requires:         python-keystonemiddleware >= 4.12.0
Requires:         python-migrate >= 0.11.0
Requires:         python-monotonic >= 0.6
Requires:         python-oslo-concurrency >= 3.8.0
Requires:         python-oslo-config >= 2:4.0.0
Requires:         python-oslo-context >= 2.14.0
Requires:         python-oslo-db >= 4.24.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.22.0
Requires:         python-oslo-messaging >= 5.24.2
Requires:         python-oslo-middleware >= 3.27.0
Requires:         python-oslo-policy >= 1.23.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-oslo-vmware >= 0.11.1
Requires:         python-osprofiler
Requires:         python-paste
Requires:         python-paste-deploy
Requires:         python-pbr
Requires:         python-prettytable
Requires:         python-retrying
Requires:         python-routes
Requires:         python-six >= 1.9.0
Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-stevedore >= 1.20.0
Requires:         python-swiftclient >= 2.2.0
Requires:         python-taskflow >= 2.7.0
Requires:         python-webob >= 1.7.1
Requires:         python-wsme >= 0.8
Requires:         pyOpenSSL
Requires:         pyxattr
Requires:         python-os-brick >= 1.8.0
Requires:         python-alembic >= 0.8.7
Requires:         python-sqlparse

#test deps: python-mox python-nose python-requests
#test and optional store:
#ceph - glance.store.rdb
#python-boto - glance.store.s3
Requires:         python-boto

%description -n   python-glance
%{common_desc}

This package contains the glance Python library.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Image Service

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    systemd-units
BuildRequires:    python-sphinx
BuildRequires:    python-openstackdocstheme
BuildRequires:    graphviz
# Required to build module documents
BuildRequires:    python-boto
BuildRequires:    python-cryptography >= 1.6
BuildRequires:    python-keystoneauth1
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-oslo-concurrency >= 3.5.0
BuildRequires:    python-oslo-context >= 0.2.0
BuildRequires:    python-oslo-db >= 4.1.0
BuildRequires:    python-sqlalchemy >= 1.0.10
BuildRequires:    python-stevedore
BuildRequires:    python-webob >= 1.2.3
BuildRequires:    python-oslotest
BuildRequires:    python-psutil
BuildRequires:    python-testresources
BuildRequires:    pyxattr
# Required to compile translation files
BuildRequires:    python-babel

%description      doc
%{common_desc}

This package contains documentation files for glance.
%endif

%package -n python-%{service}-tests
Summary:        Glance tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
%{common_desc}

This package contains the Glance test files.


%prep
%autosetup -n glance-%{upstream_version} -S git

sed -i '/\/usr\/bin\/env python/d' glance/common/config.py glance/common/crypt.py glance/db/sqlalchemy/migrate_repo/manage.py

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
PYTHONPATH=. oslo-config-generator --config-dir=etc/oslo-config-generator/
export PBR_VERSION=%{version}

# Build
%{__python2} setup.py build

# Generate i18n files
%{__python2} setup.py compile_catalog -d build/lib/%{service}/locale

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

export PYTHONPATH="$( pwd ):$PYTHONPATH"
%if 0%{?with_doc}
%{__python2} setup.py build_sphinx
%{__python2} setup.py build_sphinx --builder man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

# Fix hidden-file-or-dir warnings
%if 0%{?with_doc}
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif
rm -f %{buildroot}/usr/share/doc/glance/README.rst

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/glance
install -d -m 755 %{buildroot}%{_sharedstatedir}/glance/images
install -d -m 755 %{buildroot}%{_sysconfdir}/glance/metadefs

# WRS:
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-api-paste.ini
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_sysconfdir}/glance/glance-registry-paste.ini

# WRS in-service restarts
install -p -D -m 700  %{SOURCE31} %{buildroot}%{_bindir}/restart-glance

# WRS purge cron
install -p -D -m 755  %{SOURCE32} %{buildroot}%{_bindir}/glance-purge-deleted-active

# Config file
install -p -D -m 640 etc/glance-api.conf %{buildroot}%{_sysconfdir}/glance/glance-api.conf
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_datadir}/glance/glance-api-dist.conf
install -p -D -m 644 etc/glance-api-paste.ini %{buildroot}%{_datadir}/glance/glance-api-dist-paste.ini
##
install -p -D -m 640 etc/glance-cache.conf %{buildroot}%{_sysconfdir}/glance/glance-cache.conf
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_datadir}/glance/glance-cache-dist.conf
##
install -p -D -m 640 etc/glance-registry.conf %{buildroot}%{_sysconfdir}/glance/glance-registry.conf
install -p -D -m 644 %{SOURCE24} %{buildroot}%{_datadir}/glance/glance-registry-dist.conf
install -p -D -m 644 etc/glance-registry-paste.ini %{buildroot}%{_datadir}/glance/glance-registry-dist-paste.ini
##
install -p -D -m 640 etc/glance-scrubber.conf %{buildroot}%{_sysconfdir}/glance/glance-scrubber.conf
install -p -D -m 644 %{SOURCE25} %{buildroot}%{_datadir}/glance/glance-scrubber-dist.conf
##
install -p -D -m 644 %{SOURCE26} %{buildroot}%{_sysconfdir}/glance/glance-swift.conf

install -p -D -m 640 etc/policy.json %{buildroot}%{_sysconfdir}/glance/policy.json
install -p -D -m 640 etc/rootwrap.conf %{buildroot}%{_sysconfdir}/glance/rootwrap.conf
install -p -D -m 640 etc/schema-image.json %{buildroot}%{_sysconfdir}/glance/schema-image.json

# Move metadefs
install -p -D -m  640 etc/metadefs/*.json %{buildroot}%{_sysconfdir}/glance/metadefs/

# systemd services
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-glance-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-glance-registry.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-glance-scrubber.service

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/glance

# Install log directory
install -d -m 755 %{buildroot}%{_localstatedir}/log/glance

# Install sudoers
install -p -D -m 440 %{SOURCE30} %{buildroot}%{_sysconfdir}/sudoers.d/glance

# Symlinks to rootwrap config files
mkdir -p %{buildroot}%{_sysconfdir}/glance/rootwrap.d
for filter in %{_datarootdir}/os-brick/rootwrap/*.filters; do
  ln -s $filter %{buildroot}%{_sysconfdir}/glance/rootwrap.d
done
for filter in %{_datarootdir}/glance_store/rootwrap/*.filters; do
  test -f $filter && ln -s $filter %{buildroot}%{_sysconfdir}/glance/rootwrap.d
done

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python2_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

# Cleanup
rm -rf %{buildroot}%{_prefix}%{_sysconfdir}

%pre
getent group glance >/dev/null || groupadd -r glance -g 161
getent passwd glance >/dev/null || \
useradd -u 161 -r -g glance -d %{_sharedstatedir}/glance -s /sbin/nologin \
-c "OpenStack Glance Daemons" glance
exit 0

%post
# Initial installation
%systemd_post openstack-glance-api.service
%systemd_post openstack-glance-registry.service
%systemd_post openstack-glance-scrubber.service


%preun
%systemd_preun openstack-glance-api.service
%systemd_preun openstack-glance-registry.service
%systemd_preun openstack-glance-scrubber.service

%postun
%systemd_postun_with_restart openstack-glance-api.service
%systemd_postun_with_restart openstack-glance-registry.service
%systemd_postun_with_restart openstack-glance-scrubber.service

%files
%doc README.rst
%{_bindir}/glance-api
%{_bindir}/glance-wsgi-api
%{_bindir}/glance-control
%{_bindir}/glance-manage
%{_bindir}/glance-registry
%{_bindir}/glance-cache-cleaner
%{_bindir}/glance-cache-manage
%{_bindir}/glance-cache-prefetcher
%{_bindir}/glance-cache-pruner
%{_bindir}/glance-scrubber
%{_bindir}/glance-replicator

%{_datadir}/glance/glance-api-dist.conf
%{_datadir}/glance/glance-cache-dist.conf
%{_datadir}/glance/glance-registry-dist.conf
%{_datadir}/glance/glance-scrubber-dist.conf
%{_datadir}/glance/glance-api-dist-paste.ini
%{_datadir}/glance/glance-registry-dist-paste.ini

%{_unitdir}/openstack-glance-api.service
%{_unitdir}/openstack-glance-registry.service
%{_unitdir}/openstack-glance-scrubber.service

#WRS: in-service patching
%{_bindir}/restart-glance

#WRS: purge cron
%{_bindir}/glance-purge-deleted-active

%dir %attr(770, root, glance) %{_sysconfdir}/glance
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api-paste.ini
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry-paste.ini

%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-api.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-cache.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-registry.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-scrubber.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/glance-swift.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/policy.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/rootwrap.conf
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/schema-image.json
%config(noreplace) %attr(-, root, glance) %{_sysconfdir}/glance/metadefs/*.json
%{_sysconfdir}/glance/rootwrap.d/
%dir %attr(0755, glance, nobody) %{_sharedstatedir}/glance
%dir %attr(0750, glance, glance) %{_localstatedir}/log/glance
%config(noreplace) %{_sysconfdir}/sudoers.d/glance

%files -n python-glance -f %{service}.lang
%doc README.rst
%{python2_sitelib}/glance
%{python2_sitelib}/glance-*.egg-info
%exclude %{python2_sitelib}/glance/tests

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%endif

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 1:15.0.0-1
- Update to 15.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 1:15.0.0-0.2.0rc2
- Update to 15.0.0.0rc2

* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 1:15.0.0-0.1.0rc1
- Update to 15.0.0.0rc1

