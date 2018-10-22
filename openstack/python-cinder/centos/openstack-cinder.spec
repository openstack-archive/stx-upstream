%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name cinder

# WRS: Keep service name - used by build scripts
#%global service cinder

# WRS: remove docs - for now
%global with_doc 0

%global common_desc \
OpenStack Volume (codename Cinder) provides services to manage and \
access block storage volumes for use by Virtual Machine instances.

Name:             openstack-cinder
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:            1
Version:          11.0.0
Release:          1%{?_tis_dist}.%{tis_patch_ver}
Summary:          OpenStack Volume service

License:          ASL 2.0
URL:              http://www.openstack.org/software/openstack-storage/
Source0:          https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz

#

Source1:          cinder-dist.conf
Source2:          cinder.logrotate
# WRS: Adding pre-built config file (via: tox -egenconfig) as this is not
#      getting generated correctly in our build system. Might be due to partial
#      rebase env w/ mitaka+newton. We need to re-evaluate once rebase is
#      complete.
Source3:          cinder.conf.sample

Source10:         openstack-cinder-api.service
Source11:         openstack-cinder-scheduler.service
Source12:         openstack-cinder-volume.service
Source13:         openstack-cinder-backup.service
Source20:         cinder-sudoers

Source21:         restart-cinder
Source22:         cinder-purge-deleted-active

BuildArch:        noarch
BuildRequires:    intltool
BuildRequires:    python-d2to1
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-pbr
BuildRequires:    python-reno
BuildRequires:    python-sphinx
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python2-pip
BuildRequires:    python2-wheel
BuildRequires:    python-netaddr
BuildRequires:    systemd
BuildRequires:    git
BuildRequires:    openstack-macros
BuildRequires:    os-brick
BuildRequires:    pyparsing
BuildRequires:    pytz
BuildRequires:    python-decorator
BuildRequires:    openstack-macros
# Required to build cinder.conf
BuildRequires:    python-google-api-client >= 1.4.2
BuildRequires:    python-keystonemiddleware
BuildRequires:    python-glanceclient >= 1:2.8.0
#BuildRequires:    python-novaclient >= 1:9.0.0
BuildRequires:    python-novaclient >= 2.29.0
BuildRequires:    python-swiftclient >= 3.2.0
BuildRequires:    python-oslo-db
BuildRequires:    python-oslo-config >= 2:4.0.0
BuildRequires:    python-oslo-policy
BuildRequires:    python-oslo-reports
BuildRequires:    python-oslotest
BuildRequires:    python-oslo-utils
BuildRequires:    python-oslo-versionedobjects
BuildRequires:    python-oslo-vmware
BuildRequires:    python-os-win
BuildRequires:    python-castellan
BuildRequires:    python-cryptography
BuildRequires:    python-lxml
BuildRequires:    python-osprofiler
BuildRequires:    python-paramiko
BuildRequires:    python-suds
BuildRequires:    python-taskflow
BuildRequires:    python-tooz
BuildRequires:    python-oslo-log
BuildRequires:    python-oslo-i18n
BuildRequires:    python-barbicanclient
BuildRequires:    python-requests
BuildRequires:    python-retrying

# Required to compile translation files
BuildRequires:    python-babel

# Needed for unit tests
BuildRequires:    python-ddt
BuildRequires:    python-fixtures
BuildRequires:    python-mock
BuildRequires:    python-oslotest
BuildRequires:    python-subunit
BuildRequires:    python-testtools
BuildRequires:    python-testrepository
BuildRequires:    python-testresources
BuildRequires:    python-testscenarios
BuildRequires:    python-os-testr
BuildRequires:    python-rtslib

Requires:         python-cinder = %{epoch}:%{version}-%{release}

# we dropped the patch to remove PBR for Delorean
Requires:         python-pbr

# as convenience
Requires:         python-cinderclient

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

Requires:         lvm2
Requires:         python-osprofiler
Requires:         python-rtslib

# Required for EMC VNX driver
Requires:         python2-storops

%description
%{common_desc}


%package -n       python-cinder
Summary:          OpenStack Volume Python libraries
Group:            Applications/System

Requires:         sudo

Requires:         qemu-img
Requires:         sysfsutils
Requires:         os-brick >= 1.15.2
Requires:         python-paramiko >= 2.0
Requires:         python-simplejson >= 2.2.0

Requires:         python-castellan >= 0.7.0
Requires:         python-eventlet >= 0.18.2
Requires:         python-greenlet >= 0.3.2
Requires:         python-iso8601 >= 0.1.11
Requires:         python-lxml >= 2.3
Requires:         python-stevedore >= 1.20.0
Requires:         python-suds
Requires:         python-tooz >= 1.47.0

Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-migrate >= 0.11.0

Requires:         python-paste-deploy
Requires:         python-routes >= 2.3.1
Requires:         python-webob >= 1.7.1

Requires:         python-glanceclient >= 1:2.8.0
Requires:         python-swiftclient >= 3.2.0
Requires:         python-keystoneclient >= 3.8.0
#Requires:         python-novaclient >= 1:9.0.0
Requires:         python-novaclient >= 2.29.0

Requires:         python-oslo-config >= 2:4.0.0
Requires:         python-six >= 1.9.0
Requires:         python-psutil >= 3.2.2

Requires:         python-babel
Requires:         python-google-api-client >= 1.4.2

Requires:         python-oslo-rootwrap >= 5.0.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-db >= 4.24.0
Requires:         python-oslo-context >= 2.14.0
Requires:         python-oslo-concurrency >= 3.8.0
Requires:         python-oslo-middleware >= 3.27.0
Requires:         python-taskflow >= 2.7.0
Requires:         python-oslo-messaging >= 5.24.2
Requires:         python-oslo-policy >= 1.23.0
Requires:         python-oslo-reports >= 0.6.0
Requires:         python-oslo-service >= 1.10.0
Requires:         python-oslo-versionedobjects >= 1.19.0

Requires:         iscsi-initiator-utils

Requires:         python-osprofiler >= 1.4.0

Requires:         python-httplib2 >= 0.7.5
Requires:         python-oauth2client >= 1.5.0

Requires:         python-oslo-log >= 3.22.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-barbicanclient >= 4.0.0
Requires:         python-requests >= 2.10.0
Requires:         python-retrying >= 1.2.3
Requires:         pyparsing >= 2.0.7
Requires:         pytz
Requires:         python-decorator
Requires:         python-enum34
Requires:         python-ipaddress

Requires:         python-keystonemiddleware >= 4.12.0
Requires:         python-keystoneauth1 >= 3.1.0

Requires:         python-oslo-privsep >= 1.9.0

Requires:         python-cryptography >= 1.6


%description -n   python-cinder
%{common_desc}

This package contains the cinder Python library.

%package -n python-cinder-tests
Summary:        Cinder tests
Requires:       openstack-cinder = %{epoch}:%{version}-%{release}

# Added test requirements
Requires:       python-hacking
Requires:       python-anyjson
Requires:       python-coverage
Requires:       python-ddt
Requires:       python-fixtures
Requires:       python-mock
Requires:       python-mox3
Requires:       python-oslotest
Requires:       python-subunit
Requires:       python-testtools
Requires:       python-testrepository
Requires:       python-testresources
Requires:       python-testscenarios
Requires:       python-os-testr
Requires:       python-tempest

%description -n python-cinder-tests
%{common_desc}

This package contains the Cinder test files.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Volume
Group:            Documentation

Requires:         %{name} = %{epoch}:%{version}-%{release}

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python-eventlet
BuildRequires:    python-routes
BuildRequires:    python-sqlalchemy
BuildRequires:    python-webob
BuildRequires:    python-stevedore
# while not strictly required, quiets the build down when building docs.
BuildRequires:    python-migrate
BuildRequires:    python-iso8601 >= 0.1.9

%description      doc
%{common_desc}

This package contains documentation files for cinder.
%endif

%prep
%autosetup -n cinder-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find cinder -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

#sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
# Generate config file
PYTHONPATH=. oslo-config-generator --config-file=cinder/config/cinder-config-generator.conf
# WRS: Put this pre-built config file in place of the generated one as it's not
#      being built correctly currently
cp %{SOURCE3} etc/cinder/cinder.conf.sample

# Build
export PBR_VERSION=%{version}
%{__python2} setup.py build

# Generate i18n files
# (amoralej) we can remove '-D cinder' once https://review.openstack.org/#/c/439501/ is merged
%{__python2} setup.py compile_catalog -d build/lib/%{pypi_name}/locale -D cinder

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# Create fake egg-info for the tempest plugin
# TODO switch to %{service} everywhere as in openstack-example.spec
%global service cinder
%py2_entrypoint %{service} %{service}

# docs generation requires everything to be installed first
export PYTHONPATH="$( pwd ):$PYTHONPATH"

%if 0%{?with_doc}
%{__python2} setup.py build_sphinx --builder html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo
%endif

%{__python2} setup.py build_sphinx --builder man
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder
install -d -m 755 %{buildroot}%{_sharedstatedir}/cinder/tmp
install -d -m 755 %{buildroot}%{_localstatedir}/log/cinder

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datadir}/cinder/cinder-dist.conf
install -d -m 755 %{buildroot}%{_sysconfdir}/cinder/volumes
install -p -D -m 640 etc/cinder/rootwrap.conf %{buildroot}%{_sysconfdir}/cinder/rootwrap.conf
install -p -D -m 640 etc/cinder/api-paste.ini %{buildroot}%{_sysconfdir}/cinder/api-paste.ini
install -p -D -m 640 etc/cinder/policy.json %{buildroot}%{_sysconfdir}/cinder/policy.json
install -p -D -m 640 etc/cinder/cinder.conf.sample %{buildroot}%{_sysconfdir}/cinder/cinder.conf

# Install initscripts for services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/openstack-cinder-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/openstack-cinder-scheduler.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/openstack-cinder-volume.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/openstack-cinder-backup.service

# Install sudoers
install -p -D -m 440 %{SOURCE20} %{buildroot}%{_sysconfdir}/sudoers.d/cinder

# Install pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/cinder

# Install rootwrap files in /usr/share/cinder/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/cinder/rootwrap/
install -p -D -m 644 etc/cinder/rootwrap.d/* %{buildroot}%{_datarootdir}/cinder/rootwrap/


# Symlinks to rootwrap config files
mkdir -p %{buildroot}%{_sysconfdir}/cinder/rootwrap.d
for filter in %{_datarootdir}/os-brick/rootwrap/*.filters; do
ln -s $filter %{buildroot}%{_sysconfdir}/cinder/rootwrap.d/
done

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*/LC_*/%{pypi_name}*po
rm -f %{buildroot}%{python2_sitelib}/%{pypi_name}/locale/*pot
mv %{buildroot}%{python2_sitelib}/%{pypi_name}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{pypi_name} --all-name

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/cinder-all
rm -f %{buildroot}%{_bindir}/cinder-debug
rm -fr %{buildroot}%{python2_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/cinder/README*

# FIXME(jpena): unit tests are taking too long in the current DLRN infra
# Until we have a better architecture, let's not run them when under DLRN
%if 0%{!?dlrn}
%check
OS_TEST_PATH=./cinder/tests/unit ostestr --concurrency=2
%endif

# WRS: in-service restarts
install -p -D -m 700  %{SOURCE21} %{buildroot}%{_bindir}/restart-cinder

# WRS: purge cron
install -p -D -m 755  %{SOURCE22} %{buildroot}%{_bindir}/cinder-purge-deleted-active

%pre
getent group cinder >/dev/null || groupadd -r cinder --gid 165
if ! getent passwd cinder >/dev/null; then
  useradd -u 165 -r -g cinder -G cinder,nobody -d %{_sharedstatedir}/cinder -s /sbin/nologin -c "OpenStack Cinder Daemons" cinder
fi
exit 0

%post
%systemd_post openstack-cinder-volume
%systemd_post openstack-cinder-api
%systemd_post openstack-cinder-scheduler
%systemd_post openstack-cinder-backup

%preun
%systemd_preun openstack-cinder-volume
%systemd_preun openstack-cinder-api
%systemd_preun openstack-cinder-scheduler
%systemd_preun openstack-cinder-backup

%postun
%systemd_postun_with_restart openstack-cinder-volume
%systemd_postun_with_restart openstack-cinder-api
%systemd_postun_with_restart openstack-cinder-scheduler
%systemd_postun_with_restart openstack-cinder-backup

%files
%dir %{_sysconfdir}/cinder
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/cinder.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/api-paste.ini
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/rootwrap.conf
%config(noreplace) %attr(-, root, cinder) %{_sysconfdir}/cinder/policy.json
%config(noreplace) %{_sysconfdir}/sudoers.d/cinder
%{_sysconfdir}/cinder/rootwrap.d/
%attr(-, root, cinder) %{_datadir}/cinder/cinder-dist.conf

%dir %attr(0750, cinder, root) %{_localstatedir}/log/cinder
%dir %attr(0755, cinder, root) %{_localstatedir}/run/cinder
%dir %attr(0755, cinder, root) %{_sysconfdir}/cinder/volumes

%{_bindir}/cinder-*
%{_unitdir}/*.service
%{_datarootdir}/cinder
%{_mandir}/man1/cinder*.1.gz

#WRS: in-service patching
%{_bindir}/restart-cinder

#WRS: purge cron
%{_bindir}/cinder-purge-deleted-active

%defattr(-, cinder, cinder, -)
%dir %{_sharedstatedir}/cinder
%dir %{_sharedstatedir}/cinder/tmp

%files -n python-cinder -f %{pypi_name}.lang
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/cinder
%{python2_sitelib}/cinder-*.egg-info
%exclude %{python2_sitelib}/cinder/tests

%files -n python-cinder-tests
%license LICENSE
%{python2_sitelib}/cinder/tests
%{python2_sitelib}/%{service}_tests.egg-info

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
* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 1:11.0.0-1
- Update to 11.0.0

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 1:11.0.0-0.2.0rc2
- Update to 11.0.0.0rc2

* Tue Aug 22 2017 Alfredo Moralejo <amoralej@redhat.com> 1:11.0.0-0.1.0rc1
- Update to 11.0.0.0rc1

