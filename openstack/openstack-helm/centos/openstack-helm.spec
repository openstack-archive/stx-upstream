%global sha b9fab949aaf9627be59487c35156428ca12f7442
%global helm_folder  /usr/lib/helm
%global toolkit_version 0.1.0
%global helmchart_version 0.1.0

Summary: Openstack-Helm charts
Name: openstack-helm
Version: 1.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: base
Packager: Wind River <info@windriver.com>
URL: https://github.com/openstack/openstack-helm

Source0: %{name}-%{sha}.tar.gz

BuildArch:     noarch

Patch01: 0001-Fix-neutron-to-use-first-local-ip.patch
Patch02: 0002-Fix-up-key-exchange-for-ssh-to-VM-in-test-heat-scrip.patch
Patch03: 0003-Enable-nova-containers-to-look-at-files-directories-.patch
Patch04: 0004-cinder-Enable-external-ceph.patch
Patch05: 0005-Cinder-chart-update.patch
Patch06: 0006-Fix-cinder-chart-for-ceph-backup-driver.patch
Patch07: 0007-Cinder-template-updates-for-Jewel-compliant-rulesets.patch
Patch08: 0008-Cinder-chart-updates-for-multiple-Ceph-backends.patch
Patch09: 0009-Temporarily-remove-nova-upgrade_levels-compute-auto-.patch
Patch10: 0010-Revert-Neutron-TaaS-support-as-L2-Extension.patch
Patch11: 0011-Revert-Openstack-Use-k8s-secret-to-store-config.patch
Patch12: 0012-Undo-mapping-compute_extend.conf-into-nova-compute-c.patch
Patch13: 0013-Undo-mapping-compute_host.conf-into-nova-compute-con.patch
Patch14: 0014-ceilometer-chart-updates.patch
Patch15: 0015-ceilometer-fix-syntax-from-last-commit.patch

BuildRequires: docker-ce
BuildRequires: helm
BuildRequires: openstack-helm-infra
Requires: openstack-helm-infra

%description
Openstack Helm charts

%prep
%setup -n openstack-helm
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

%build
echo "PWD"
pwd
# initialize helm and stage the toolkit
helm init --client-only
# Host a server for the charts
cp  %{helm_folder}/helm-toolkit-%{toolkit_version}.tgz .
helm serve --repo-path . &
helm repo rm local
helm repo add local http://localhost:8879/charts

# Make the charts. These produce a tgz file
make barbican
make ceilometer
make cinder
make congress
make glance
make heat
make horizon
make ironic
make keystone
make magnum
make mistral
make neutron
make nova
make senlin
make tempest

%install
# helm_folder is created by openstack-helm-infra
install -d -m 755 ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 barbican-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 ceilometer-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 cinder-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 congress-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 glance-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 heat-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 horizon-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 ironic-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 keystone-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 magnum-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 mistral-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 neutron-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 nova-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 senlin-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}
install -p -D -m 755 tempest-%{helmchart_version}.tgz ${RPM_BUILD_ROOT}%{helm_folder}

%files
#helm_folder is owned by openstack-helm-infra
%defattr(-,root,root,-)
%{helm_folder}/barbican-%{helmchart_version}.tgz
%{helm_folder}/ceilometer-%{helmchart_version}.tgz
%{helm_folder}/cinder-%{helmchart_version}.tgz
%{helm_folder}/congress-%{helmchart_version}.tgz
%{helm_folder}/glance-%{helmchart_version}.tgz
%{helm_folder}/heat-%{helmchart_version}.tgz
%{helm_folder}/horizon-%{helmchart_version}.tgz
%{helm_folder}/ironic-%{helmchart_version}.tgz
%{helm_folder}/keystone-%{helmchart_version}.tgz
%{helm_folder}/magnum-%{helmchart_version}.tgz
%{helm_folder}/mistral-%{helmchart_version}.tgz
%{helm_folder}/neutron-%{helmchart_version}.tgz
%{helm_folder}/nova-%{helmchart_version}.tgz
%{helm_folder}/senlin-%{helmchart_version}.tgz
%{helm_folder}/tempest-%{helmchart_version}.tgz

