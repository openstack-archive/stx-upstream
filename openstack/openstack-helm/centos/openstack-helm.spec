%global sha add7a9bc1175f6fafa8ea2918bc1d62209aaf243
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

Patch01: 0001-Revert-Neutron-TaaS-support-as-L2-Extension.patch
Patch02: 0002-Revert-Openstack-Use-k8s-secret-to-store-config.patch
Patch03: 0003-ceilometer-chart-updates.patch

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

