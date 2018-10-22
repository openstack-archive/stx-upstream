%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global service keystone

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-keystone
Epoch:          0
Version:        12.0.0
Release:        1%{?_tis_dist}.%{tis_patch_ver}
Summary:        OpenStack Identity Service
License:        Apache-2.0
URL:            https://launchpad.net/keystone/
Source0:        %{service}-%{version}.tar.gz

Source1:        openstack-keystone.logrotate
Source2:        openstack-keystone.sysctl
Source3:        openstack-keystone.tmpfiles
Source4:        openstack-keystone.defaultconf

#WRS
Source99:       openstack-keystone.service
Source100:      keystone-all
Source101:      keystone-fernet-keys-rotate-active
Source102:      password-rules.conf
Source103:      public.py

BuildArch:      noarch
BuildRequires:  openstack-macros
BuildRequires:  openstack-tempest
BuildRequires:  python-webtest
BuildRequires:  python-bcrypt
BuildRequires:  python2-devel
BuildRequires:  python-fixtures
BuildRequires:  python-freezegun
BuildRequires:  python-lxml
BuildRequires:  python-mock
# WRS: Required for debian based builds only
# use openstackdocstheme on RHEL instead
#BuildRequires: python-os-api-ref
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python-os-testr
# Required to build keystone.conf
BuildRequires:  python-oslo-cache >= 1.5.0
BuildRequires:  python-oslo-config >= 2:3.9.0
BuildRequires:  python-oslotest
BuildRequires:  python-osprofiler >= 1.1.0
BuildRequires:  python-pbr >= 1.8
BuildRequires:  python-subunit
BuildRequires:  python-reno
BuildRequires:  python-requests
BuildRequires:  python2-scrypt
BuildRequires:  python-testrepository
BuildRequires:  python-testresources
# Required to compile translation files
BuildRequires:  python-babel

#WRS: Need these for build_sphinx
BuildRequires:  tsconfig
BuildRequires:  python2-pycodestyle

Requires:       python-keystone = %{epoch}:%{version}-%{release}
Requires:       python-keystoneclient >= 1:2.3.1

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires:  xmlsec1-openssl
Requires(pre):    shadow-utils

%description
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.
.
This package contains the keystone python libraries.

%package -n     python-keystone
Summary:        Keystone Python libraries
Group:          Application/System
Requires:       python-babel
Requires:       python-paste
Requires:       python-paste-deploy
Requires:       python-PyMySQL
Requires:       python-routes
Requires:       python-sqlalchemy
Requires:       python-webob
Requires:       python-bcrypt
Requires:       python-cryptography
Requires:       python-dogpile-cache
Requires:       python-jsonschema
Requires:       python-keystoneclient
Requires:       python-keystonemiddleware
Requires:       python-ldappool
Requires:       python-msgpack
Requires:       python-oauthlib
Requires:       python-oslo-cache
Requires:       python-oslo-concurrency
Requires:       python-oslo-config
Requires:       python-oslo-context
Requires:       python-oslo-db
Requires:       python-oslo-i18n
Requires:       python-oslo-log
Requires:       python-oslo-messaging
Requires:       python-oslo-middleware
Requires:       python-oslo-policy
Requires:       python-oslo-serialization
Requires:       python-oslo-utils
Requires:       python-osprofiler
Requires:       python-passlib
Requires:       python-pbr
Requires:       python-pycadf
Requires:       python-pysaml2
Requires:       python-memcached
Requires:       python-six
Requires:       python-migrate
Requires:       python-stevedore
Requires:       python-ldap

%description -n   python-keystone
Keystone is a Python implementation of the OpenStack
(http://www.openstack.org) identity service API.
This package contains the Keystone Python library.

%package doc
Summary:        Documentation for OpenStack Identity Service
Group:          Documentation
BuildRequires:  python-paste-deploy
BuildRequires:  python-routes
BuildRequires:  python-sphinx
BuildRequires:  python-cryptography
BuildRequires:  python-dogpile-cache
BuildRequires:  python-jsonschema
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-ldappool
BuildRequires:  python-msgpack
BuildRequires:  python-oauthlib
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-i18n
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-passlib
BuildRequires:  python-pysaml2
BuildRequires:  python-memcached
BuildRequires:  python2-pip
BuildRequires:  python2-wheel

%description doc
OpenStack Keystone documentaion.
.
This package contains the documentation

%prep
%setup -q -n keystone-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete
find keystone -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;
# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

# adjust paths to WSGI scripts
sed -i 's#/local/bin#/bin#' httpd/wsgi-keystone.conf
sed -i 's#apache2#httpd#' httpd/wsgi-keystone.conf
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg

%build
#PYTHONPATH=.
# WRS: export PBR version
export PBR_VERSION=%{version}
%{__python2} setup.py build

%{__python2} setup.py build_sphinx --builder=html,man
# remove the Sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# config file generation
oslo-config-generator --config-file config-generator/keystone.conf \
--output-file etc/keystone.conf.sample
# policy file generation
oslopolicy-sample-generator --config-file config-generator/keystone-policy-generator.conf --output-file etc/keystone.policy.yaml

%py2_build_wheel

%install
# WRS: export PBR version
export PBR_VERSION=%{version}
%{__python2} setup.py install --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

mkdir -p %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_sysconfdir}/keystone
install -d -m 755 %{buildroot}%{_sysconfdir}/sysctl.d
install -d -m 755 %{buildroot}%{_localstatedir}/{lib,log}/keystone
install -d -m 750 %{buildroot}%{_localstatedir}/cache/keystone
install -d -m 755 %{buildroot}%{_sysconfdir}/keystone/keystone.conf.d/

# default dir for fernet tokens
install -d -m 750 %{buildroot}%{_sysconfdir}/keystone/credential-keys/
install -D -m 644 %{SOURCE3} %{buildroot}/%{_tmpfilesdir}/keystone.conf
install -p -D -m 640 etc/keystone.conf.sample %{buildroot}%{_sysconfdir}/keystone/keystone.conf
install -D -m 640 %{SOURCE4} %{buildroot}/%{_sysconfdir}/keystone/keystone.conf.d/010-keystone.conf
#install -D -m 440 %{SOURCE5} %{buildroot}/%{_sysconfdir}/keystone/README.config
install -p -D -m 640 etc/logging.conf.sample %{buildroot}%{_sysconfdir}/keystone/logging.conf
install -p -D -m 640 etc/keystone-paste.ini %{buildroot}%{_sysconfdir}/keystone/keystone-paste.ini
install -p -D -m 640 etc/keystone.policy.yaml %{buildroot}%{_sysconfdir}/keystone/keystone.policy.yaml
install -p -D -m 640 etc/default_catalog.templates %{buildroot}%{_sysconfdir}/keystone/default_catalog.templates
install -p -D -m 640 etc/sso_callback_template.html %{buildroot}%{_sysconfdir}/keystone/sso_callback_template.html
# WRS: don't install a seperate keystone logrotate file as this is managed by syslog-ng
#install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-keystone
install -p -D -m 644 etc/policy.v3cloudsample.json %{buildroot}%{_datadir}/keystone/policy.v3cloudsample.json
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d/openstack-keystone.conf
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
# Install sample data script.
install -p -D -m 755 tools/sample_data.sh %{buildroot}%{_datadir}/keystone/sample_data.sh
# Install apache configuration files
install -p -D -m 644 httpd/wsgi-keystone.conf  %{buildroot}%{_datadir}/keystone/

# WRS install keystone cron script
install -p -D -m 755 %{SOURCE101} %{buildroot}%{_bindir}/keystone-fernet-keys-rotate-active

# WRS: install password rules(readable only)
install -p -D -m 440 %{SOURCE102} %{buildroot}%{_sysconfdir}/keystone/password-rules.conf

# WRS: install keystone public gunicorn app
install -p -D -m 755 %{SOURCE103}  %{buildroot}/%{_datarootdir}/keystone/public.py

# WRS: install openstack-keystone service script
install -p -D -m 644 %{SOURCE99} %{buildroot}%{_unitdir}/openstack-keystone.service

# WRS: Install keystone-all bash script
install -p -D -m 755 %{SOURCE100} %{buildroot}%{_bindir}/keystone-all

%pre
# 163:163 for keystone (openstack-keystone) - rhbz#752842
getent group keystone >/dev/null || groupadd -r --gid 163 keystone
getent passwd keystone >/dev/null || \
useradd --uid 163 -r -g keystone -d %{_sharedstatedir}/keystone -s /sbin/nologin \
-c "OpenStack Keystone Daemons" keystone
exit 0

# WRS: disable testr
#%check
# don't want to depend on hacking for package building
#rm keystone/tests/unit/test_hacking_checks.py
#%{__python2} setup.py testr

%post
%tmpfiles_create %{_tmpfilesdir}/keystone.conf
%systemd_post openstack-keystone.service
%sysctl_apply openstack-keystone.conf

%preun
%systemd_preun openstack-keystone.service

%postun
%systemd_postun_with_restart openstack-keystone.service

%files
%license LICENSE
%doc README.rst
%{_mandir}/man1/keystone*.1.gz
%{_bindir}/keystone-wsgi-admin
%{_bindir}/keystone-wsgi-public
%{_bindir}/keystone-manage
# WRS: add keystone-all as part of newton rebase
%{_bindir}/keystone-all
# WRS: add Keystone fernet keys cron job
%{_bindir}/keystone-fernet-keys-rotate-active
%_tmpfilesdir/keystone.conf
%dir %{_datadir}/keystone
%attr(0644, root, keystone) %{_datadir}/keystone/policy.v3cloudsample.json
%attr(0755, root, root) %{_datadir}/keystone/sample_data.sh
%attr(0644, root, keystone) %{_datadir}/keystone/wsgi-keystone.conf
# WRS: add openstack-keystone sysVinit script
%{_unitdir}/openstack-keystone.service
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone
%dir %attr(0750, root, keystone) %{_sysconfdir}/keystone/keystone.conf.d/
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone.conf.d/010-keystone.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/keystone-paste.ini
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/logging.conf
%config(noreplace) %attr(0640, root, keystone) %{_sysconfdir}/keystone/default_catalog.templates
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/keystone.policy.yaml
%config(noreplace) %attr(0640, keystone, keystone) %{_sysconfdir}/keystone/sso_callback_template.html
# WRS: add password rules configuration
%attr(0440, root, keystone) %{_sysconfdir}/keystone/password-rules.conf

# WRS: log rotate not needed
#%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-keystone
%dir %attr(0755, %{keystone}, %{keystone}) %{_localstatedir}/lib/keystone
%dir %attr(0750, %{keystone}, %{keystone}) %{_localstatedir}/log/keystone
%dir %attr(0750, %{keystone}, %{keystone}) %{_localstatedir}/cache/keystone
%{_sysconfdir}/sysctl.d/openstack-keystone.conf

%files -n python-keystone
%{_datarootdir}/keystone/public*.py*
%defattr(-,root,root,-)
%doc README.rst
%license LICENSE
%{python2_sitelib}/keystone
%{python2_sitelib}/keystone-*.egg-info

%files doc
%license LICENSE
%doc doc/build/html

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
