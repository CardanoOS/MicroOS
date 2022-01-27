#
# spec file for package openSUSE-release.spec
#
# Copyright (c) 2019 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define product MicroOS
%define betaversion Beta%{nil}
%if "%{?betaversion}" == ""
%undefine betaversion
%endif
%define codename Leap
Name:           MicroOS-release
Version:        15.2
Release:        0
# 1 is the product release, not the build release of this package 
Provides:       aaa_version
Provides:       distribution-release
Provides:       suse-release = %{version}-%{release}
Provides:       suse-release-oss = %{version}-%{release}
%if 0%{?beta_version}
# Give zypp a hint that this product must be kept up-to-date using zypper dup, not up (boo#1061384)
Provides:       product-update() = dup
%endif
# The system-installation marks the package as base product for YaST
Provides:       system-installation() = %product
Obsoletes:      aaa_version
Obsoletes:      openSUSE-Promo-release <= 11.1
Obsoletes:      openSUSE-release-live <= 11.0
Obsoletes:      product_flavor(%{product}) < 15.2
Conflicts:      sles-release <= 10 sled-release <= 10 core-release <= 10
Conflicts:      otherproviders(distribution-release)
# bnc#826592
Provides:       weakremover(kernel-default) < 3.11
Provides:       weakremover(kernel-desktop) < 4.2
Provides:       weakremover(kernel-ec2) < 3.11
Provides:       weakremover(kernel-pae) < 3.11
Provides:       weakremover(kernel-vanilla) < 3.11
Provides:       weakremover(kernel-xen) < 3.11
# boo#1029075
Provides:       weakremover(gpg-pubkey-3d25d3d9-36e12d04)
# some hints for the solver
# default Java for Leap 15.1
Suggests:       java-11-openjdk
# preferred MTA
Suggests:       postfix
# preferred ntp daemon
Suggests:       chrony
#
Recommends:     branding-openSUSE
Suggests:       distribution-logos-openSUSE-MicroOS
# we don't install control.xml on MicroOS
# BuildRequires:  skelcd-control-MicroOS
BuildRequires:  skelcd-openSUSE
# FIXME: compat with Factory
Provides:       openSUSE-MicroOS-release = %version-%release

Source100:      weakremovers.inc
%include %{SOURCE100}
Provides:       %name-%version
Provides:       product() = MicroOS
Provides:       product(MicroOS) = 15.2-1
%ifarch x86_64
Provides:       product-register-target() = openSUSE%2DLeap%2D15.2%2Dx86_64
%endif
%ifarch aarch64
Provides:       product-register-target() = openSUSE%2DLeap%2D15.2%2Daarch64
%endif
Provides:       product-label() = openSUSE%20MicroOS
Provides:       product-cpeid() = cpe%3A%2Fo%3Aopensuse%3Amicroos%3A15.2
Provides:       product-url(releasenotes) = http%3A%2F%2Fdoc.opensuse.org%2Frelease%2Dnotes%2F%{_target_cpu}%2FopenSUSE%2FLeap%2F15.2%2Frelease%2Dnotes%2DopenSUSE.rpm
Provides:       product-url(repository) = http%3A%2F%2Fdownload.opensuse.org%2Fdistribution%2Fleap%2F15.2%2Frepo%2Foss%2F
Provides:       product-url(repository) = http%3A%2F%2Fdownload.opensuse.org%2Fports%2F%{_target_cpu}%2Fdistribution%2Fleap%2F15.2%2Frepo%2Foss%2F
Provides:       product-endoflife() = 2020%2D11%2D30
Requires:       product_flavor(MicroOS)


Summary:        openSUSE MicroOS 15.2
License:        BSD-3-Clause
Group:          System/Fhs
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
#PreReq:         coreutils
# the post scriptlets uses awk, boo#976913
Requires(post):  awk

%description
openSUSE MicroOS 15.2

%package ftp
License:        BSD-3-Clause
Group:          System/Fhs
Provides:       product_flavor()
Provides:       flavor(ftp)
Provides:       product_flavor(MicroOS) = 15.2-1
Summary:        openSUSE MicroOS 15.2%{?betaversion: %{betaversion}}

%description ftp
openSUSE MicroOS 15.2

%files ftp
%defattr(-,root,root)
%doc %{_defaultdocdir}/MicroOS-release-ftp

%package dvd
License:        BSD-3-Clause
Group:          System/Fhs
Provides:       product_flavor()
Provides:       flavor(dvd)
Provides:       product_flavor(MicroOS) = 15.2-1
Summary:        openSUSE MicroOS 15.2%{?betaversion: %{betaversion}}

%description dvd
openSUSE MicroOS 15.2

%files dvd
%defattr(-,root,root)
%doc %{_defaultdocdir}/MicroOS-release-dvd

%package appliance
License:        BSD-3-Clause
Group:          System/Fhs
Provides:       product_flavor()
Provides:       flavor(appliance)
Provides:       product_flavor(MicroOS) = 15.2-1
Summary:        openSUSE MicroOS 15.2%{?betaversion: %{betaversion}}

%description appliance
openSUSE MicroOS 15.2

%files appliance
%defattr(-,root,root)
%doc %{_defaultdocdir}/MicroOS-release-appliance



%prep
%setup -qcT
mkdir license
if [ -f /CD1/license.tar.gz ]; then
  tar -C license -xzf /CD1/license.tar.gz
elif [ -f %{_libexecdir}/skelcd/CD1/license.tar.gz ]; then
  tar -C license -xzf %{_libexecdir}/skelcd/CD1/license.tar.gz
fi

%build

%install
mkdir -p %{buildroot}%{_sysconfdir} %{buildroot}%{_libexecdir} %{buildroot}/run

### XXX kill issue-generator please
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_libexecdir}/issue.d
echo -e "\nWelcome to openSUSE MicroOS 15.2 (%{_target_cpu}) - Kernel \\\r (\\\l).\n" > %{buildroot}%{_libexecdir}/issue.d/10-OS
echo -e "\n" > %{buildroot}%{_libexecdir}/issue.d/90-OS

VERSION_ID=`echo %{version}|tr '[:upper:]' '[:lower:]'|sed -e 's/ //g;'`
# note: VERSION is an optional field and has no meaning other than informative on a rolling distro
# We do thus not add it to the os-release file
cat > %{buildroot}%{_libexecdir}/os-release <<EOF
NAME="openSUSE MicroOS"
VERSION="%{version}%{?betaversion: %{betaversion}}"
ID="opensuse-microos"
ID_LIKE="suse opensuse opensuse-leap"
VERSION_ID="$VERSION_ID"
PRETTY_NAME="openSUSE MicroOS %{version}%{?betaversion: %{betaversion}}"
ANSI_COLOR="0;32"
CPE_NAME="cpe:/o:opensuse:MicroOS:%{version}"
BUG_REPORT_URL="https://bugs.opensuse.org"
HOME_URL="https://www.opensuse.org/"
EOF
ln -s ..%{_libexecdir}/os-release %{buildroot}%{_sysconfdir}/os-release

echo "Have a lot of fun..." > %{buildroot}%{_sysconfdir}/motd
# Bug 404141 - /etc/YaST/control.xml should be owned by some package
# Not on MicroOS boo#1170709
#mkdir -p %{buildroot}%{_sysconfdir}/YaST2/
#echo %{buildroot}
#if [ -f /CD1/control.xml ]; then
#  install -m 644 /CD1/control.xml %{buildroot}%{_sysconfdir}/YaST2/
#elif [ -f %{_libexecdir}/skelcd/CD1/control.xml ]; then
#  install -m 644 %{_libexecdir}/skelcd/CD1/control.xml %{buildroot}%{_sysconfdir}/YaST2/
#fi

# fate#319341, make openSUSE-release own YaST license files
# see also jsc#SLE-3067 for mess caused by SLE
install -D -d -m 755 "%{buildroot}%{_datadir}/licenses/product/base"
install -D -d -m 755 "%{buildroot}%{_defaultlicensedir}"
cp -a license "%{buildroot}%{_defaultlicensedir}/%{name}"
pushd license
# SLE compat
for i in *; do
	ln -s "%{_defaultlicensedir}/%{name}/$i" %{buildroot}%{_datadir}/licenses/product/base/$i
done

mkdir -p $RPM_BUILD_ROOT/etc/products.d
cat >$RPM_BUILD_ROOT/etc/products.d/MicroOS.prod << EOF
<?xml version="1.0" encoding="UTF-8"?>
<product schemeversion="0">
  <vendor>openSUSE</vendor>
  <name>MicroOS</name>
  <version>15.2</version>
  <release>1</release>
  <endoflife>2020-11-30</endoflife>
  <arch>%{_target_cpu}</arch>
  <cpeid>cpe:/o:opensuse:microos:15.2</cpeid>
  <productline>MicroOS</productline>
  <codestream>
    <name>openSUSE MicroOS 15</name>
    <endoflife>2021-11-30</endoflife>
  </codestream>
  <register>
    <pool>
    </pool>
    <updates>
      <distrotarget arch="x86_64">openSUSE-Leap-15.2-x86_64</distrotarget>
      <distrotarget arch="aarch64">openSUSE-Leap-15.2-aarch64</distrotarget>
    </updates>
  </register>
  <repositories>
  </repositories>
  <updaterepokey>000000000</updaterepokey>
  <summary>openSUSE MicroOS 15.2</summary>
  <shortsummary>openSUSE MicroOS</shortsummary>
  <description>openSUSE MicroOS 15.2</description>
  <linguas>
    <language>en</language>
  </linguas>
  <urls>
    <url name="releasenotes">http://doc.opensuse.org/release-notes/%{_target_cpu}/openSUSE/Leap/15.2/release-notes-openSUSE.rpm</url>
    <url name="repository" arch="x86_64">http://download.opensuse.org/distribution/leap/15.2/repo/oss/</url>
    <url name="repository" arch="aarch64">http://download.opensuse.org/ports/%{_target_cpu}/distribution/leap/15.2/repo/oss/</url>
  </urls>
  <buildconfig>
    <producttheme>MicroOS</producttheme>
    <betaversion>Beta</betaversion>
    <create_flavors>true</create_flavors>
  </buildconfig>
  <installconfig>
    <defaultlang>en_US</defaultlang>
    <releasepackage name="%{name}" flag="EQ" version="%{version}" release="%{release}"/>
    <distribution>openSUSE</distribution>
  </installconfig>
  <runtimeconfig/>
</product>

EOF

mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-ftp
cat >$RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-ftp/README << EOF
This package only exists for providing the product flavor 'ftp'.

EOF

mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-dvd
cat >$RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-dvd/README << EOF
This package only exists for providing the product flavor 'dvd'.

EOF

mkdir -p $RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-appliance
cat >$RPM_BUILD_ROOT/%{_defaultdocdir}/MicroOS-release-appliance/README << EOF
This package only exists for providing the product flavor 'appliance'.

EOF



%post
# this is a base product, create symlink  bsc#1091952
if [ ! -L %{_sysconfdir}/products.d/baseproduct ]; then
	ln -sf MicroOS.prod %{_sysconfdir}/products.d/baseproduct
fi

%files
%defattr(644,root,root,755)
%dir %{_datadir}/licenses/product
%{_datadir}/licenses/product/base
%license license/*
%{_sysconfdir}/os-release
%{_libexecdir}/os-release
# Bug 404141 - /etc/YaST/control.xml should be owned by some package
#dir %{_sysconfdir}/YaST2/
#config %{_sysconfdir}/YaST2/control.xml
%config(noreplace) %{_sysconfdir}/motd
%dir %{_libexecdir}/issue.d
%{_libexecdir}/issue.d/*-OS
%{_sysconfdir}/products.d
%ghost %{_sysconfdir}/products.d/baseproduct

%changelog
