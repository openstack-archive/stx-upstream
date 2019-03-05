%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:       python-django-horizon
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:      1
Version:    12.0.0
Release:    2%{?_tis_dist}.%{tis_patch_ver}
Summary:    Django application for talking to Openstack

Group:      Development/Libraries
# Code in horizon/horizon/utils taken from django which is BSD
License:    ASL 2.0 and BSD
URL:        http://horizon.openstack.org/
Source0:    horizon-%{version}.tar.gz
Source2:    openstack-dashboard-httpd-2.4.conf
Source3:    python-django-horizon-systemd.conf

# demo config for separate logging
Source4:    openstack-dashboard-httpd-logging.conf

# logrotate config
Source5:    python-django-horizon-logrotate.conf

# STX 
Source7:    horizon.init
Source8:    horizon-clearsessions
Source11:   horizon-patching-restart
Source12:   horizon-region-exclusions.csv
Source13:   guni_config.py
Source14:   horizon-assets-compress

Patch1:     0001-Remove-WRS-imports-from-novaclient.patch

#
# BuildArch needs to be located below patches in the spec file. Don't ask!
#

BuildArch:  noarch

BuildRequires:   python-django
Requires:   python-django

# STX 
BuildRequires: cgts-client
Requires: cgts-client

Requires:   pytz
Requires:   python-six >= 1.9.0
Requires:   python-pbr

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python2-pip
BuildRequires: python2-wheel
BuildRequires: python-pbr >= 2.0.0
BuildRequires: git
BuildRequires: python-six >= 1.9.0
BuildRequires: gettext

# for checks:
%if 0%{?rhel} == 0
BuildRequires:   python-django-nose >= 1.2
BuildRequires:   python-coverage
BuildRequires:   python-mox3
BuildRequires:   python-nose-exclude
BuildRequires:   python-nose
BuildRequires:   python-selenium
%endif
BuildRequires:   python-netaddr
BuildRequires:   python-anyjson
BuildRequires:   python-iso8601

# additional provides to be consistent with other django packages
Provides: django-horizon = %{epoch}:%{version}-%{release}

%description
Horizon is a Django application for providing Openstack UI components.
It allows performing site administrator (viewing account resource usage,
configuring users, accounts, quotas, flavors, etc.) and end user
operations (start/stop/delete instances, create/restore snapshots, view
instance VNC console, etc.)


%package -n openstack-dashboard
Summary:    Openstack web user interface reference implementation
Group:      Applications/System

Requires:   httpd
Requires:   mod_wsgi
Requires:   %{name} = %{epoch}:%{version}-%{release}
Requires:   python-django-openstack-auth >= 3.5.0
Requires:   python-django-compressor >= 2.0
Requires:   python-django-appconf
Requires:   python-django-babel
Requires:   python-lesscpy

Requires:   python-iso8601
Requires:   python-glanceclient
Requires:   python-keystoneclient >= 1:3.8.0
Requires:   python-novaclient
Requires:   python-neutronclient
Requires:   python-cinderclient
Requires:   python-swiftclient >= 3.2.0
Requires:   python-heatclient >= 1.6.1
Requires:   python-netaddr
Requires:   python-osprofiler >= 1.4.0
Requires:   python-pymongo >= 3.0.2
Requires:   python-django-pyscss >= 2.0.2
Requires:   python-semantic_version
Requires:   python-XStatic
Requires:   python-XStatic-jQuery
Requires:   python-XStatic-Angular >= 1:1.3.7
Requires:   python-XStatic-Angular-Bootstrap
Requires:   python-XStatic-Angular-Schema-Form
Requires:   python-XStatic-D3 >= 3.5.17.0
Requires:   python-XStatic-Font-Awesome >= 4.7.0
Requires:   python-XStatic-Hogan
Requires:   python-XStatic-JQuery-Migrate
Requires:   python-XStatic-JQuery-TableSorter
Requires:   python-XStatic-JQuery-quicksearch
Requires:   python-XStatic-JSEncrypt >= 2.3.1.1
Requires:   python-XStatic-Jasmine >= 2.4.1.1
Requires:   python-XStatic-Rickshaw
Requires:   python-XStatic-Spin
Requires:   python-XStatic-jquery-ui
Requires:   python-XStatic-Bootstrap-Datepicker
Requires:   python-XStatic-Bootstrap-SCSS >= 3.3.7.1
Requires:   python-XStatic-termjs >= 0.0.7.0
Requires:   python-XStatic-smart-table
Requires:   python-XStatic-Angular-lrdragndrop
Requires:   python-XStatic-Angular-Gettext
Requires:   python-XStatic-Angular-FileUpload
Requires:   python-XStatic-Magic-Search
Requires:   python-XStatic-bootswatch
Requires:   python-XStatic-roboto-fontface >= 0.5.0.0
Requires:   python-XStatic-mdi
Requires:   python-XStatic-objectpath
Requires:   python-XStatic-tv4

Requires:   python-scss >= 1.3.4
Requires:   fontawesome-fonts-web >= 4.1.0

Requires:   python-oslo-concurrency >= 3.8.0
Requires:   python-oslo-config >= 2:4.0.0
Requires:   python-oslo-i18n >= 2.1.0
Requires:   python-oslo-serialization >= 1.10.0
Requires:   python-oslo-utils >= 3.20.0
Requires:   python-oslo-policy >= 1.23.0
Requires:   python-babel
Requires:   python-futurist
Requires:   python-pint

Requires:   openssl
Requires:   logrotate

Requires:   PyYAML >= 3.10

BuildRequires: python-django-openstack-auth >= 3.5.0
BuildRequires: python-django-compressor >= 2.0
BuildRequires: python-django-appconf
BuildRequires: python-lesscpy
BuildRequires: python-semantic_version
BuildRequires: python-django-pyscss >= 2.0.2
BuildRequires: python-XStatic
BuildRequires: python-XStatic-jQuery
BuildRequires: python-XStatic-Angular >= 1:1.3.7
BuildRequires: python-XStatic-Angular-Bootstrap
BuildRequires: python-XStatic-Angular-Schema-Form
BuildRequires: python-XStatic-D3
BuildRequires: python-XStatic-Font-Awesome
BuildRequires: python-XStatic-Hogan
BuildRequires: python-XStatic-JQuery-Migrate
BuildRequires: python-XStatic-JQuery-TableSorter
BuildRequires: python-XStatic-JQuery-quicksearch
BuildRequires: python-XStatic-JSEncrypt >= 2.3.1.1
BuildRequires: python-XStatic-Jasmine
BuildRequires: python-XStatic-Rickshaw
BuildRequires: python-XStatic-Spin
BuildRequires: python-XStatic-jquery-ui
BuildRequires: python-XStatic-Bootstrap-Datepicker
BuildRequires: python-XStatic-Bootstrap-SCSS >= 3.3.7.1
BuildRequires: python-XStatic-termjs
BuildRequires: python-XStatic-smart-table
BuildRequires: python-XStatic-Angular-lrdragndrop
BuildRequires: python-XStatic-Angular-FileUpload
BuildRequires: python-XStatic-Magic-Search
BuildRequires: python-XStatic-Angular-Gettext
BuildRequires: python-XStatic-bootswatch
BuildRequires: python-XStatic-roboto-fontface
BuildRequires: python-XStatic-mdi
BuildRequires: python-XStatic-objectpath
BuildRequires: python-XStatic-tv4
# bootstrap-scss requires at least python-scss >= 1.2.1
BuildRequires: python-scss >= 1.3.4
BuildRequires: fontawesome-fonts-web >= 4.1.0
BuildRequires: python-oslo-concurrency
BuildRequires: python-oslo-config
BuildRequires: python-oslo-i18n
BuildRequires: python-oslo-serialization
BuildRequires: python-oslo-utils
BuildRequires: python-oslo-policy
BuildRequires: python-babel
BuildRequires: python-pint

BuildRequires: pytz
BuildRequires: systemd
# STX 
BuildRequires: systemd-devel

%description -n openstack-dashboard
Openstack Dashboard is a web user interface for Openstack. The package
provides a reference implementation using the Django Horizon project,
mostly consisting of JavaScript and CSS to tie it altogether as a standalone
site.


# Turn OFF sphinx documentation in STX environment
# Mock does not have /dev/log so sphinx-build will always fail
%if 0%{?with_doc}
%package doc
Summary:    Documentation for Django Horizon
Group:      Documentation

Requires:   %{name} = %{epoch}:%{version}-%{release}
BuildRequires: python-sphinx >= 1.1.3

# Doc building basically means we have to mirror Requires:
BuildRequires: python-openstackdocstheme
BuildRequires: python-glanceclient
BuildRequires: python-keystoneclient
BuildRequires: python-novaclient >= 1:6.0.0
BuildRequires: python-neutronclient
BuildRequires: python-cinderclient
BuildRequires: python-swiftclient
BuildRequires: python-heatclient

%description doc
Documentation for the Django Horizon application for talking with Openstack

%endif

%package -n openstack-dashboard-theme
Summary: OpenStack web user interface reference implementation theme module
Requires: openstack-dashboard = %{epoch}:%{version}-%{release}

%description -n openstack-dashboard-theme
Customization module for OpenStack Dashboard to provide a branded logo.

%prep
%autosetup -n horizon-%{upstream_version} -S git
# autosetup automatically applies the patches

# STX remove troublesome files introduced by tox
rm -f openstack_dashboard/test/.secret_key_store
rm -f openstack_dashboard/test/*.secret_key_store.lock
rm -f openstack_dashboard/local/.secret_key_store
rm -f openstack_dashboard/local/*.secret_key_store.lock
rm -rf horizon.egg-info

# drop config snippet
cp -p %{SOURCE4} .
cp -p %{SOURCE13} .

# customize default settings
# WAS [PATCH] disable debug, move web root
sed -i "/^DEBUG =.*/c\DEBUG = False" openstack_dashboard/local/local_settings.py.example
sed -i "/^WEBROOT =.*/c\WEBROOT = '/dashboard/'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*ALLOWED_HOSTS =.*/c\ALLOWED_HOSTS = ['horizon.example.com', 'localhost']" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*LOCAL_PATH =.*/c\LOCAL_PATH = '/tmp'" openstack_dashboard/local/local_settings.py.example
sed -i "/^.*POLICY_FILES_PATH =.*/c\POLICY_FILES_PATH = '/etc/openstack-dashboard'" openstack_dashboard/local/local_settings.py.example

sed -i "/^BIN_DIR = .*/c\BIN_DIR = '/usr/bin'" openstack_dashboard/settings.py
sed -i "/^COMPRESS_PARSER = .*/a COMPRESS_OFFLINE = True" openstack_dashboard/settings.py

# set COMPRESS_OFFLINE=True
sed -i 's:COMPRESS_OFFLINE.=.False:COMPRESS_OFFLINE = True:' openstack_dashboard/settings.py

# STX: MANIFEST needs .eslintrc files for angular
echo "include .eslintrc"   >> MANIFEST.in
# MANIFEST needs to include json and pot files under openstack_dashboard 
echo "recursive-include openstack_dashboard *.json *.pot .eslintrc"   >> MANIFEST.in
# MANIFEST needs to include pot files  under horizon
echo "recursive-include horizon *.pot .eslintrc"   >> MANIFEST.in


%build
# compile message strings
cd horizon && django-admin compilemessages && cd ..
cd openstack_dashboard && django-admin compilemessages && cd ..
# Dist tarball is missing .mo files so they're not listed in distributed egg metadata.
# Removing egg-info and letting PBR regenerate it was working around that issue
# but PBR cannot regenerate complete SOURCES.txt so some other files wont't get installed.
# Further reading why not remove upstream egg metadata:
# https://github.com/emonty/python-oslo-messaging/commit/f632684eb2d582253601e8da7ffdb8e55396e924
# https://fedorahosted.org/fpc/ticket/488
# STX: 2 problems.  1  we dont have an egg yet.  2 there are no .mo files
#echo >> horizon.egg-info/SOURCES.txt
#ls */locale/*/LC_MESSAGES/django*mo >> horizon.egg-info/SOURCES.txt
export PBR_VERSION=%{version}
%{__python} setup.py build

# compress css, js etc.
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py
# get it ready for compressing later in puppet-horizon
# STX: run compression on the controller
# STX: turn off compression because /dev/log does not exist in mock
#%{__python} manage.py collectstatic --noinput --clear
#%{__python} manage.py compress --force


%if 0%{?with_doc}
# build docs
export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# undo hack
cp openstack_dashboard/local/local_settings.py.example openstack_dashboard/local/local_settings.py

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%endif

%py2_build_wheel

%install
export PBR_VERSION=%{version}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
mkdir -p $RPM_BUILD_ROOT/wheels
install -m 644 dist/*.whl $RPM_BUILD_ROOT/wheels/

# STX
install -d -m 755 %{buildroot}/opt/branding
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 -D -p  %{SOURCE7} %{buildroot}%{_sysconfdir}/rc.d/init.d/horizon
install -m 755 -D -p %{SOURCE8} %{buildroot}/%{_bindir}/horizon-clearsessions
install -m 755 -D -p %{SOURCE11} %{buildroot}/%{_bindir}/horizon-patching-restart
install -m 755 -D -p %{SOURCE12} %{buildroot}/opt/branding/horizon-region-exclusions.csv
install -m 755 -D -p %{SOURCE14} %{buildroot}/%{_bindir}/horizon-assets-compress

# drop httpd-conf snippet
install -m 0644 -D -p %{SOURCE2} %{buildroot}%{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
install -d -m 755 %{buildroot}%{_datadir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sharedstatedir}/openstack-dashboard
install -d -m 755 %{buildroot}%{_sysconfdir}/openstack-dashboard

# create directory for systemd snippet
mkdir -p %{buildroot}%{_unitdir}/httpd.service.d/
cp %{SOURCE3} %{buildroot}%{_unitdir}/httpd.service.d/openstack-dashboard.conf


# Copy everything to /usr/share
mv %{buildroot}%{python_sitelib}/openstack_dashboard \
   %{buildroot}%{_datadir}/openstack-dashboard
cp manage.py %{buildroot}%{_datadir}/openstack-dashboard
# STX
cp guni_config.py %{buildroot}%{_datadir}/openstack-dashboard
rm -rf %{buildroot}%{python_sitelib}/openstack_dashboard

# remove unnecessary .po files
find %{buildroot} -name django.po -exec rm '{}' \;
find %{buildroot} -name djangojs.po -exec rm '{}' \;

# Move config to /etc, symlink it back to /usr/share
mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py.example %{buildroot}%{_sysconfdir}/openstack-dashboard/local_settings
# STX: we do not want to have this symlink, puppet will overwrite the content of local_settings
#ln -s ../../../../../%{_sysconfdir}/openstack-dashboard/local_settings %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/local/local_settings.py

mv %{buildroot}%{_datadir}/openstack-dashboard/openstack_dashboard/conf/*.json %{buildroot}%{_sysconfdir}/openstack-dashboard

%find_lang django --all-name

grep "\/usr\/share\/openstack-dashboard" django.lang > dashboard.lang
grep "\/site-packages\/horizon" django.lang > horizon.lang

# copy static files to %{_datadir}/openstack-dashboard/static
mkdir -p %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a openstack_dashboard/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
cp -a horizon/static/* %{buildroot}%{_datadir}/openstack-dashboard/static
# STX: there is no static folder, since compress step was skipped
#cp -a static/* %{buildroot}%{_datadir}/openstack-dashboard/static

# create /var/run/openstack-dashboard/ and own it
mkdir -p %{buildroot}%{_sharedstatedir}/openstack-dashboard

# create /var/log/horizon and own it
mkdir -p %{buildroot}%{_var}/log/horizon

# place logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
cp -a %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-dashboard

%check
# don't run tests on rhel
%if 0%{?rhel} == 0
# since rawhide has django-1.7 now, tests fail
#./run_tests.sh -N -P
%endif

%post -n openstack-dashboard
# ugly hack to set a unique SECRET_KEY
sed -i "/^from horizon.utils import secret_key$/d" /etc/openstack-dashboard/local_settings
sed -i "/^SECRET_KEY.*$/{N;s/^.*$/SECRET_KEY='`openssl rand -hex 10`'/}" /etc/openstack-dashboard/local_settings
# reload systemd unit files
systemctl daemon-reload >/dev/null 2>&1 || :

%postun
# update systemd unit files
%{systemd_postun}

%files -f horizon.lang
%doc README.rst openstack-dashboard-httpd-logging.conf
%license LICENSE
%dir %{python_sitelib}/horizon
%{python_sitelib}/horizon/*.py*
%{python_sitelib}/horizon/browsers
%{python_sitelib}/horizon/conf
%{python_sitelib}/horizon/contrib
%{python_sitelib}/horizon/forms
%{python_sitelib}/horizon/hacking
%{python_sitelib}/horizon/management
%{python_sitelib}/horizon/static
%{python_sitelib}/horizon/tables
%{python_sitelib}/horizon/tabs
%{python_sitelib}/horizon/templates
%{python_sitelib}/horizon/templatetags
%{python_sitelib}/horizon/test
%{python_sitelib}/horizon/utils
%{python_sitelib}/horizon/workflows
%{python_sitelib}/horizon/karma.conf.js
%{python_sitelib}/horizon/middleware
%{python_sitelib}/*.egg-info

%files -n openstack-dashboard -f dashboard.lang
%license LICENSE
%dir %{_datadir}/openstack-dashboard/
%{_datadir}/openstack-dashboard/*.py*
%{_datadir}/openstack-dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/*.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/api
%{_datadir}/openstack-dashboard/openstack_dashboard/contrib
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/admin
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/identity
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/project
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/settings
# STX
%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/__init__.py*
%{_datadir}/openstack-dashboard/openstack_dashboard/django_pyscss_fix
%{_datadir}/openstack-dashboard/openstack_dashboard/enabled
%{_datadir}/openstack-dashboard/openstack_dashboard/karma.conf.js
%{_datadir}/openstack-dashboard/openstack_dashboard/local
%{_datadir}/openstack-dashboard/openstack_dashboard/management
%{_datadir}/openstack-dashboard/openstack_dashboard/static
%{_datadir}/openstack-dashboard/openstack_dashboard/templates
%{_datadir}/openstack-dashboard/openstack_dashboard/templatetags
%{_datadir}/openstack-dashboard/openstack_dashboard/themes
%{_datadir}/openstack-dashboard/openstack_dashboard/test
%{_datadir}/openstack-dashboard/openstack_dashboard/usage
%{_datadir}/openstack-dashboard/openstack_dashboard/utils
%{_datadir}/openstack-dashboard/openstack_dashboard/wsgi
%dir %{_datadir}/openstack-dashboard/openstack_dashboard
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??/LC_MESSAGES
%dir %{_datadir}/openstack-dashboard/openstack_dashboard/locale/??_??/LC_MESSAGES
%{_datadir}/openstack-dashboard/openstack_dashboard/.eslintrc

%dir %attr(0750, root, apache) %{_sysconfdir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_sharedstatedir}/openstack-dashboard
%dir %attr(0750, apache, apache) %{_var}/log/horizon
%config(noreplace) %{_sysconfdir}/httpd/conf.d/openstack-dashboard.conf
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/local_settings
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/cinder_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/keystone_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/nova_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/glance_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/neutron_policy.json
%config(noreplace) %attr(0640, root, apache) %{_sysconfdir}/openstack-dashboard/heat_policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-dashboard
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%config(noreplace) %{_unitdir}/httpd.service.d/openstack-dashboard.conf

# STX
%dir /opt/branding
%config(noreplace) /opt/branding/horizon-region-exclusions.csv
%{_sysconfdir}/rc.d/init.d/horizon
%{_bindir}/horizon-clearsessions
%{_bindir}/horizon-patching-restart
%{_bindir}/horizon-assets-compress


%if 0%{?with_doc}

%files doc
%doc html
%license LICENSE

%endif


%files -n openstack-dashboard-theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/dashboards/theme
#%{_datadir}/openstack-dashboard/openstack_dashboard/enabled/_99_customization.*

%package wheels
Summary: %{name} wheels

%description wheels
Contains python wheels for %{name}

%files wheels
/wheels/*

%changelog
* Mon Oct 04 2017 Radomir Dopieralski <rdopiera@redhat.com> 1:12.0.0-2
- Require at least 3.3.7.1 version of XStatic-bootstrap-SCSS package

* Wed Aug 30 2017 rdo-trunk <javier.pena@redhat.com> 1:12.0.0-1
- Update to 12.0.0

* Mon Aug 28 2017 rdo-trunk <javier.pena@redhat.com> 1:12.0.0-0.3.0rc3
- Update to 12.0.0.0rc3

* Fri Aug 25 2017 Alfredo Moralejo <amoralej@redhat.com> 1:12.0.0-0.2.0rc2
- Update to 12.0.0.0rc2

* Mon Aug 21 2017 Alfredo Moralejo <amoralej@redhat.com> 1:12.0.0-0.1.0rc1
- Update to 12.0.0.0rc1


