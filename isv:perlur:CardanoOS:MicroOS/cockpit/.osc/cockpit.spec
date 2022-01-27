#
# spec file for package cockpit
#
# Copyright (c) 2020 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/

# Adapted from original file that is maintained at the following location:
# https://github.com/cockpit-project/cockpit/blob/master/tools/cockpit.spec

# Globals that may be defined elsewhere
#  * Version 122
#  * wip 1
#

# earliest base that the subpackages work on; the instances of this get computed/updated
# by tools/gen-spec-dependencies during "make dist", but keep a hardcoded fallback
%define required_base 122

# we generally want CentOS packages to be like RHEL; special cases need to check %{centos} explicitly
%if 0%{?centos}
%define rhel %{centos}
%endif

%if "%{!?__python3:1}"
%define __python3 /usr/bin/python3
%endif

# for testing this already gets set in fedora.install, as we want the target
# VERSION_ID, not the mock chroot's one
%if "%{!?os_version_id:1}"
%define os_version_id %(. /etc/os-release; echo $VERSION_ID)
%endif

%define _hardened_build 1

# define to build the dashboard
%define build_dashboard 1

# build basic packages like cockpit-bridge
%define build_basic 1
# build optional extensions like cockpit-docker
%define build_optional 1

# cockpit's firewall service definition moved to firewalld
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8 || 0%{?suse_version}
%define firewalld_service 0
%else
%define firewalld_service 1
%endif

%define __lib lib

# cockpit-kubernetes is RHEL 7 and Fedora < 30 only, and 64 bit arches only
%if (0%{?fedora} && 0%{?fedora} < 30) || (0%{?rhel} >= 7 && 0%{?rhel} < 8)
%ifarch aarch64 x86_64 ppc64le s390x
%define build_kubernetes 1
%endif
%endif

# cockpit-machines-ovirt is RHEL 7 and Fedora < 30 only
%if (0%{?fedora} && 0%{?fedora} < 30) || (0%{?rhel} >= 7 && 0%{?rhel} < 8)
%define build_ovirt 1
%endif

%if 0%{?rhel} >= 8
%global go_scl_prefix go-toolset-7-
%else
%global go_scl_prefix %{nil}
%endif

%if 0%{?rhel} >= 7
%define vdo_on_demand 1
%define insights_client_on_demand 1
%endif

Name:           cockpit
Summary:        Web Console for Linux servers

License:        LGPL-2.0-or-later
URL:            https://cockpit-project.org/

Version:        195.12
Release:        0
Source0:        https://github.com/cockpit-project/cockpit/releases/download/%{version}/cockpit-%{version}.tar.xz
Source1:        cockpit.pam
Source9:        cockpit-rpmlintrc
Source10:       cockpit.permissions
Source11:       cockpit_assets.tar.gz

Patch1:        branding_tests.patch

BuildRequires: gcc
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(polkit-agent-1) >= 0.105
BuildRequires: pam-devel

BuildRequires: autoconf automake
BuildRequires: /usr/bin/python3
BuildRequires: intltool
%if %{defined build_dashboard}
BuildRequires: libssh-devel >= 0.7.1
%endif
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig(krb5) >= 1.11
BuildRequires: libxslt-devel
BuildRequires: glib-networking
BuildRequires: sed

BuildRequires: glib2-devel >= 2.37.4
BuildRequires: pkgconfig(libsystemd)
%if 0%{?suse_version}
BuildRequires: libpcp-devel
BuildRequires: python3-pcp
BuildRequires: openssh
BuildRequires: intltool
BuildRequires: docbook-xsl-stylesheets
BuildRequires: distribution-release
%else
BuildRequires: pcp-libs-devel
BuildRequires: openssh-clients
BuildRequires: docbook-style-xsl
%endif
BuildRequires: krb5-server
BuildRequires: gdb

# For documentation
BuildRequires: xmlto

# This is the "cockpit" metapackage. It should only
# Require, Suggest or Recommend other cockpit-xxx subpackages

Requires: cockpit-bridge
Requires: cockpit-ws
Requires: cockpit-system

# Optional components
%if 0%{?fedora} || 0%{?rhel} >= 8
%if 0%{?rhel} == 0
Recommends: cockpit-dashboard
%ifarch x86_64 %{arm} aarch64 ppc64le i686 s390x
Recommends: (cockpit-docker if /usr/bin/docker)
%endif
%endif
Recommends: (cockpit-networkmanager if NetworkManager)
Recommends: (cockpit-storaged if udisks2)
Recommends: cockpit-packagekit
%if 0%{?rhel} >= 8 && 0%{?centos} == 0
Recommends: subscription-manager-cockpit
%endif
Suggests: cockpit-pcp
%if 0%{?build_kubernetes}
Suggests: cockpit-kubernetes
%endif
Suggests: cockpit-selinux
%endif

%prep
%setup -q -n cockpit-%{version}
%autopatch -p1
cp %SOURCE1 tools/cockpit.pam

cd src/branding/default && tar zxf %SOURCE11 --strip-components=1


%build
%configure \
    --disable-silent-rules \
    --with-cockpit-user=cockpit-wsinstance \
    --with-selinux-config-type=etc_t \
%if 0%{?rhel} >= 7 && 0%{?rhel} < 8
    --without-storaged-iscsi-sessions \
%endif
    --with-appstream-data-packages='[ "appstream-data" ]' \
    --with-nfs-client-package='"nfs-utils"' \
%if 0%{?suse_version}
    --docdir=%_defaultdocdir/%{name} \
%endif
    %{?vdo_on_demand:--with-vdo-package='"vdo"'} \
    %{?insights_client_on_demand:--with-insights-client-package='"insights-client"'}
make -j4 %{?extra_flags} all

%check
export -n XDG_CONFIG_DIRS
make -j4 check

%install
make install DESTDIR=%{buildroot}
make install-tests DESTDIR=%{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -p -m 644 tools/cockpit.pam $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/cockpit
rm -f %{buildroot}/%{_libdir}/cockpit/*.so
%if 0%{?firewalld_service} == 0
rm -f %{buildroot}/%{_prefix}/%{__lib}/firewalld/services/cockpit.xml
%endif
install -p -m 644 AUTHORS COPYING README.md %{buildroot}%{_docdir}/cockpit/

%if 0%{?suse_version}
install -p -m 644 -D %{SOURCE10} %{buildroot}%{_sysconfdir}/permissions.d/cockpit
%endif

# Build the package lists for resource packages
find %{buildroot}%{_datadir}/cockpit/base1 -type f >> base.list
find %{buildroot}%{_datadir}/cockpit/base1 -type d -exec echo %dir {} \; >> base.list
echo '%{_sysconfdir}/cockpit/machines.d' >> base.list
echo %{buildroot}%{_datadir}/polkit-1/actions/org.cockpit-project.cockpit-bridge.policy >> base.list
# RHEL 7 needs to keep cockpit-ssh in dashboard for backwards compat
%if 0%{?rhel} == 7
find %{buildroot}%{_datadir}/cockpit/ssh -type f >> dashboard.list
find %{buildroot}%{_datadir}/cockpit/ssh -type d -exec echo %dir {} \; >> dashboard.list
echo '%{_libexecdir}/cockpit-ssh' >> dashboard.list
%else
find %{buildroot}%{_datadir}/cockpit/ssh -type f >> base.list
find %{buildroot}%{_datadir}/cockpit/ssh -type d -exec echo %dir {} \; >> base.list
echo '%{_libexecdir}/cockpit-ssh' >> base.list
%endif

%if %{defined build_dashboard}
find %{buildroot}%{_datadir}/cockpit/dashboard -type f >> dashboard.list
find %{buildroot}%{_datadir}/cockpit/dashboard -type d -exec echo %dir {} \; >> dashboard.list
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/dashboard
touch dashboard.list
%endif

find %{buildroot}%{_datadir}/cockpit/pcp -type f >> pcp.list
find %{buildroot}%{_datadir}/cockpit/pcp -type d -exec echo %dir {} \; >> pcp.list

find %{buildroot}%{_datadir}/cockpit/realmd -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/realmd -type d -exec echo %dir {} \; >> system.list

find %{buildroot}%{_datadir}/cockpit/tuned -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/tuned -type d -exec echo %dir {} \; >> system.list

find %{buildroot}%{_datadir}/cockpit/shell -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/shell -type d -exec echo %dir {} \; >> system.list

find %{buildroot}%{_datadir}/cockpit/systemd -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/systemd -type d -exec echo %dir {} \; >> system.list

find %{buildroot}%{_datadir}/cockpit/users -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/users -type d -exec echo %dir {} \; >> system.list

find %{buildroot}%{_datadir}/cockpit/kdump -type f >> kdump.list
find %{buildroot}%{_datadir}/cockpit/kdump -type d -exec echo %dir {} \; >> kdump.list

find %{buildroot}%{_datadir}/cockpit/sosreport -type f >> sosreport.list
find %{buildroot}%{_datadir}/cockpit/sosreport -type d -exec echo %dir {} \; >> sosreport.list

%if %{defined build_subscriptions}
find %{buildroot}%{_datadir}/cockpit/subscriptions -type f >> system.list
find %{buildroot}%{_datadir}/cockpit/subscriptions -type d -exec echo %dir {} \; >> subscriptions.list
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/subscriptions
%endif

find %{buildroot}%{_datadir}/cockpit/storaged -type f >> storaged.list
find %{buildroot}%{_datadir}/cockpit/storaged -type d -exec echo %dir {} \; >> storaged.list

find %{buildroot}%{_datadir}/cockpit/networkmanager -type f >> networkmanager.list
find %{buildroot}%{_datadir}/cockpit/networkmanager -type d -exec echo %dir {} \; >> networkmanager.list

find %{buildroot}%{_datadir}/cockpit/packagekit -type f >> packagekit.list
find %{buildroot}%{_datadir}/cockpit/packagekit -type d -exec echo %dir {} \; >> packagekit.list

find %{buildroot}%{_datadir}/cockpit/apps -type f >> packagekit.list
find %{buildroot}%{_datadir}/cockpit/apps -type d -exec echo %dir {} \; >> packagekit.list

find %{buildroot}%{_datadir}/cockpit/machines -type f >> machines.list
find %{buildroot}%{_datadir}/cockpit/machines -type d -exec echo %dir {} \; >> machines.list

%if 0%{?build_ovirt}
find %{buildroot}%{_datadir}/cockpit/ovirt -type f >> ovirt.list
find %{buildroot}%{_datadir}/cockpit/ovirt -type d -exec echo %dir {} \; >> ovirt.list
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/ovirt
touch ovirt.list
%endif

find %{buildroot}%{_datadir}/cockpit/selinux -type f >> selinux.list
find %{buildroot}%{_datadir}/cockpit/selinux -type d -exec echo %dir {} \; >> selinux.list

find %{buildroot}%{_datadir}/cockpit/playground -type f >> tests.list
find %{buildroot}%{_datadir}/cockpit/playground -type d -exec echo %dir {} \; >> tests.list

%ifarch x86_64 %{arm} aarch64 ppc64le i686 s390x
%if 0%{?fedora} || 0%{?rhel} < 8
find %{buildroot}%{_datadir}/cockpit/docker -type f >> docker.list
find %{buildroot}%{_datadir}/cockpit/docker -type d -exec echo %dir {} \; >> docker.list
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/docker
touch docker.list
%endif
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/docker
touch docker.list
%endif

%if 0%{?build_kubernetes}
%if %{defined wip}
%else
rm %{buildroot}/%{_datadir}/cockpit/kubernetes/override.json
%endif
find %{buildroot}%{_datadir}/cockpit/kubernetes -type f >> kubernetes.list
find %{buildroot}%{_datadir}/cockpit/kubernetes -type d -exec echo %dir {} \; >> kubernetes.list
%else
rm -rf %{buildroot}/%{_datadir}/cockpit/kubernetes
rm -f %{buildroot}/%{_libexecdir}/cockpit-kube-auth
rm -f %{buildroot}/%{_libexecdir}/cockpit-kube-launch
rm %{buildroot}/%{_libexecdir}/cockpit-stub
touch kubernetes.list
%endif

# when not building basic packages, remove their files
%if 0%{?build_basic} == 0
for pkg in base1 branding motd kdump networkmanager realmd selinux shell sosreport ssh static systemd tuned users; do
    rm -r %{buildroot}/%{_datadir}/cockpit/$pkg
    rm -f %{buildroot}/%{_datadir}/metainfo/org.cockpit-project.cockpit-${pkg}.metainfo.xml
done
for data in doc locale man pixmaps polkit-1; do
    rm -r %{buildroot}/%{_datadir}/$data
done
for lib in systemd tmpfiles.d firewalld; do
    rm -r %{buildroot}/%{_prefix}/%{__lib}/$lib
done
for libexec in cockpit-askpass cockpit-session cockpit-ws cockpit-desktop; do
    rm %{buildroot}/%{_libexecdir}/$libexec
done
rm -r %{buildroot}/%{_libdir}/security %{buildroot}/%{_sysconfdir}/pam.d %{buildroot}/%{_sysconfdir}/motd.d %{buildroot}/%{_sysconfdir}/issue.d
rm %{buildroot}/usr/bin/cockpit-bridge %{buildroot}/usr/sbin/remotectl
rm -f %{buildroot}%{_libexecdir}/cockpit-ssh
rm -f %{buildroot}%{_datadir}/metainfo/cockpit.appdata.xml
%endif

# when not building optional packages, remove their files
%if 0%{?build_optional} == 0
for pkg in apps dashboard docker kubernetes machines ovirt packagekit pcp playground storaged; do
    rm -rf %{buildroot}/%{_datadir}/cockpit/$pkg
done
# files from -tests
rm -r %{buildroot}/%{_prefix}/%{__lib}/cockpit-test-assets %{buildroot}/%{_sysconfdir}/cockpit/cockpit.conf
# files from -pcp
rm -r %{buildroot}/%{_libexecdir}/cockpit-pcp %{buildroot}/%{_localstatedir}/lib/pcp/
# files from -kubernetes
rm -f %{buildroot}/%{_libexecdir}/cockpit-kube-auth %{buildroot}/%{_libexecdir}/cockpit-kube-launch %{buildroot}/%{_libexecdir}/cockpit-stub
# files from -machines
rm -f %{buildroot}/%{_prefix}/share/metainfo/org.cockpit-project.cockpit-machines.metainfo.xml
# files from -storaged
rm -f %{buildroot}/%{_prefix}/share/metainfo/org.cockpit-project.cockpit-storaged.metainfo.xml
%endif

sed -i "s|%{buildroot}||" *.list

# Build the package lists for debug package, and move debug files to installed locations
find %{buildroot}/usr/src/debug%{_datadir}/cockpit -type f -o -type l > debug.partial
sed -i "s|%{buildroot}/usr/src/debug||" debug.partial
sed -n 's/\.map\(\.gz\)\?$/\0/p' *.list >> debug.partial
sed -i '/\.map\(\.gz\)\?$/d' *.list
tar -C %{buildroot}/usr/src/debug -cf - . | tar -C %{buildroot} -xf -
rm -rf %{buildroot}/usr/src/debug

# On RHEL kdump, networkmanager, selinux, and sosreport are part of the system package
%if 0%{?rhel}
cat kdump.list sosreport.list networkmanager.list selinux.list >> system.list
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit-project.cockpit-sosreport.metainfo.xml
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit-project.cockpit-kdump.metainfo.xml
rm -f %{buildroot}%{_datadir}/pixmaps/cockpit-sosreport.png
%endif

%if 0%{?rhel}
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit-project.cockpit-selinux.metainfo.xml
%endif

%if 0%{?build_basic}
%find_lang cockpit
%endif

%if 0%{?suse_version}
# remove brandings with stale symlinks. Means they don't match
# the distro.
pushd %{buildroot}/%{_datadir}/cockpit/branding
find -L * -type l -printf "%H\n" | sort -u | xargs rm -rv
popd
# need this in SUSE as post build checks dislike stale symlinks
install -m 644 -D /dev/null %{buildroot}/run/cockpit/motd
# rm -r %{buildroot}/run
# remove files of not installable packages
rm -r %{buildroot}%{_datadir}/cockpit/{sosreport,selinux}
rm -f %{buildroot}/%{_prefix}/share/metainfo/org.cockpit-project.cockpit-{selinux,sosreport}.metainfo.xml
rm -f %{buildroot}%{_datadir}/pixmaps/cockpit-sosreport.png

find %{buildroot}%{_prefix} -type f -name \*.map -print -delete
%else
# dwz has trouble with the go binaries
# https://fedoraproject.org/wiki/PackagingDrafts/Go
%global _dwz_low_mem_die_limit 0
%if 0%{?fedora} || 0%{?rhel} >= 8
%global _debugsource_packages 1
%global _debuginfo_subpackages 0
%endif

%define find_debug_info %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_include_minidebuginfo:-m} %{?_find_debuginfo_dwz_opts} %{?_find_debuginfo_opts} %{?_debugsource_packages:-S debugsourcefiles.list} "%{_builddir}/%{?buildsubdir}"

# Redefine how debug info is built to slip in our extra debug files
%define __debug_install_post   \
   %{find_debug_info} \
   cat debug.partial >> %{_builddir}/%{?buildsubdir}/debugfiles.list \
%{nil}
%endif

# -------------------------------------------------------------------------------
# Basic Sub-packages

%if 0%{?build_basic}

%description
The Cockpit Web Console enables users to administer GNU/Linux servers using a
web browser.

It offers network configuration, log inspection, diagnostic reports, SELinux
troubleshooting, interactive command-line sessions, and more.

%files
%{_docdir}/cockpit/AUTHORS
%{_docdir}/cockpit/COPYING
%{_docdir}/cockpit/README.md
%dir %{_datadir}/cockpit
%{_datadir}/metainfo/cockpit.appdata.xml
%{_datadir}/pixmaps/cockpit.png
%doc %{_mandir}/man1/cockpit.1.gz


%package bridge
Summary: Cockpit bridge server-side component
Requires: glib-networking
%if 0%{?rhel} != 7
Provides: cockpit-ssh = %{version}
# cockpit-ssh moved from dashboard to bridge in 171
Conflicts: cockpit-dashboard < 170.x
# PR #10430 dropped workaround for ws' inability to understand x-host-key challenge
Conflicts: cockpit-ws < 181.x
%endif

%description bridge
The Cockpit bridge component installed server side and runs commands on the
system on behalf of the web based user interface.

%files bridge -f base.list
%doc %{_mandir}/man1/cockpit-bridge.1.gz
%dir %{_sysconfdir}/cockpit
%{_bindir}/cockpit-bridge
%{_libexecdir}/cockpit-askpass

%package doc
Summary: Cockpit deployment and developer guide
BuildArch: noarch

%description doc
The Cockpit Deployment and Developer Guide shows sysadmins how to
deploy Cockpit on their machines as well as helps developers who want to
embed or extend Cockpit.

%files doc
%exclude %{_docdir}/cockpit/AUTHORS
%exclude %{_docdir}/cockpit/COPYING
%exclude %{_docdir}/cockpit/README.md
%{_docdir}/cockpit

%package system
Summary: Cockpit admin interface package for configuring and troubleshooting a system
BuildArch: noarch
Requires: cockpit-bridge >= %{version}
%if !0%{?suse_version}
Requires: shadow-utils
%endif
Requires: grep
Requires: libpwquality
Requires: /usr/bin/date
Provides: cockpit-realmd = %{version}
Provides: cockpit-shell = %{version}
Provides: cockpit-systemd = %{version}
Provides: cockpit-tuned = %{version}
Provides: cockpit-users = %{version}
%if 0%{?rhel}
Provides: cockpit-networkmanager = %{version}
Obsoletes: cockpit-networkmanager
Requires: NetworkManager
Provides: cockpit-kdump = %{version}
Requires: kexec-tools
# Optional components (only when soft deps are supported)
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: polkit
%endif
%if 0%{?rhel} >= 8
Recommends: NetworkManager-team
Recommends: setroubleshoot-server >= 3.3.3
%endif
Provides: cockpit-selinux = %{version}
Provides: cockpit-sosreport = %{version}
%endif
%if %{defined build_subscriptions}
Provides: cockpit-subscriptions = %{version}
Requires: subscription-manager >= 1.13
%endif
# NPM modules which are also available as packages
#Provides: bundled(js-jquery) = %{npm-version:jquery}
#Provides: bundled(js-moment) = %{npm-version:moment}
#Provides: bundled(nodejs-flot) = %{npm-version:jquery-flot}
#Provides: bundled(nodejs-promise) = %{npm-version:promise}
#Provides: bundled(xstatic-bootstrap-datepicker-common) = %{npm-version:bootstrap-datepicker}
#Provides: bundled(xstatic-patternfly-common) = %{npm-version:patternfly}

%description system
This package contains the Cockpit shell and system configuration interfaces.

%files system -f system.list

%package ws
Summary: Cockpit Web Service
Requires: glib-networking
Requires: openssl
Requires: glib2 >= 2.37.4
# RHEL/CentOS 7 has firewalld 0.6.x, but does not ship cockpit service
# %if 0%{?rhel} != 7
# %if 0%{?firewalld_service}
# Conflicts: firewalld >= 0.6.0-1
# %else
# Conflicts: firewalld < 0.6.0-1
# %endif
# %endif
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: sscg >= 2.3
Recommends: system-logos
%endif
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%if 0%{?suse_version}
Requires(pre): permissions
Requires(post): permissions
%endif


%description ws
The Cockpit Web Service listens on the network, and authenticates users.

%files ws -f cockpit.lang
%{_sysconfdir}/permissions.d/cockpit
%doc %{_mandir}/man1/cockpit-desktop.1.gz
%doc %{_mandir}/man5/cockpit.conf.5.gz
%doc %{_mandir}/man8/cockpit-ws.8.gz
%doc %{_mandir}/man8/remotectl.8.gz
%doc %{_mandir}/man8/pam_ssh_add.8.gz
%dir %{_sysconfdir}/cockpit
%config(noreplace) %{_sysconfdir}/cockpit/ws-certs.d
%config(noreplace) %{_sysconfdir}/pam.d/cockpit
%config %{_sysconfdir}/issue.d/cockpit.issue
%dir %{_sysconfdir}/motd.d
%config %{_sysconfdir}/motd.d/cockpit
%dir %{_datadir}/cockpit/motd
%{_datadir}/cockpit/motd/update-motd
%{_datadir}/cockpit/motd/inactive.motd
%{_unitdir}/cockpit.service
%{_unitdir}/cockpit-motd.service
%{_unitdir}/cockpit.socket
%if 0%{?firewalld_service}
%{_prefix}/%{__lib}/firewalld/services/cockpit.xml
%endif
%{_prefix}/%{__lib}/tmpfiles.d/cockpit-tempfiles.conf
%{_sbindir}/remotectl
%dir %{_libdir}/security
%{_libdir}/security/pam_ssh_add.so
%{_libexecdir}/cockpit-ws
%{_libexecdir}/cockpit-desktop
%verify(not user group mode) %attr(4750, root, cockpit-wsinstance) %{_libexecdir}/cockpit-session
%attr(775, -, wheel) %{_localstatedir}/lib/cockpit
%{_datadir}/cockpit/static
%{_datadir}/cockpit/branding
%ghost %{_rundir}/cockpit/motd
%ghost %dir %{_rundir}/cockpit

%pre ws
getent group cockpit-wsinstance >/dev/null || groupadd -r cockpit-wsinstance
getent passwd cockpit-wsinstance >/dev/null || useradd -r -g cockpit-wsinstance -d /nonexisting -s /sbin/nologin -c "User for cockpit-ws" cockpit-wsinstance

%service_add_pre cockpit-motd.service
%service_add_pre cockpit.service
%service_add_pre cockpit.socket

%post ws
%service_add_post cockpit-motd.service
%service_add_post cockpit.service
%service_add_post cockpit.socket

%if 0%{?suse_version}
%set_permissions %{_libexecdir}/cockpit-session
%tmpfiles_create cockpit-tempfiles.conf
%endif
# firewalld only partially picks up changes to its services files without this
# test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

%preun ws
%systemd_preun cockpit-motd.service
%systemd_preun cockpit.service
%systemd_preun cockpit.socket

%postun ws
%systemd_postun_with_restart cockpit.socket
%systemd_postun_with_restart cockpit.service
%systemd_postun_with_restart cockpit-motd.service

%if 0%{?suse_version}
%verifyscript ws
%verify_permissions -e %{_libexecdir}/cockpit-session
%endif

# -------------------------------------------------------------------------------
# Sub-packages that are part of cockpit-system in RHEL/CentOS, but separate in Fedora

%if 0%{?rhel} == 0

%package kdump
Summary: Cockpit user interface for kernel crash dumping
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: kexec-tools
BuildArch: noarch

%description kdump
The Cockpit component for configuring kernel crash dumping.

%files kdump -f kdump.list
%{_datadir}/metainfo/org.cockpit-project.cockpit-kdump.metainfo.xml

%if ! 0%{?suse_version}
%package sosreport
Summary: Cockpit user interface for diagnostic reports
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: sos
BuildArch: noarch

%description sosreport
The Cockpit component for creating diagnostic reports with the
sosreport tool.

%files sosreport -f sosreport.list
%{_datadir}/metainfo/org.cockpit-project.cockpit-sosreport.metainfo.xml
%{_datadir}/pixmaps/cockpit-sosreport.png
%endif


%package networkmanager
Summary: Cockpit user interface for networking, using NetworkManager
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: NetworkManager
# Optional components (only when soft deps are supported)
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: NetworkManager-team
%endif
BuildArch: noarch

%description networkmanager
The Cockpit component for managing networking.  This package uses NetworkManager.

%files networkmanager -f networkmanager.list

%endif

%if 0%{?rhel} == 0 && 0%{?suse_version} == 0

%package selinux
Summary: Cockpit SELinux package
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires: setroubleshoot-server >= 3.3.3
%endif
BuildArch: noarch

%description selinux
This package contains the Cockpit user interface integration with the
utility setroubleshoot to diagnose and resolve SELinux issues.

%files selinux -f selinux.list
%{_datadir}/metainfo/org.cockpit-project.cockpit-selinux.metainfo.xml

%endif

%else # build basic packages

# RPM requires this
%description
Dummy package from building optional packages only; never install or publish me.

%endif # build basic packages

# -------------------------------------------------------------------------------
# Sub-packages that are optional extensions

%if 0%{?build_optional}

%package -n cockpit-storaged
Summary: Cockpit user interface for storage, using udisks
Requires: cockpit-shell >= %{required_base}
Requires: udisks2 >= 2.6
%if 0%{?rhel} == 7
# Recommends: not supported in RHEL <= 7
Requires: udisks2-lvm2 >= 2.6
Requires: udisks2-iscsi >= 2.6
Requires: device-mapper-multipath
Requires: python
Requires: python-dbus
%else
Recommends: udisks2-lvm2 >= 2.6
Recommends: udisks2-iscsi >= 2.6
Recommends: device-mapper-multipath
Recommends: clevis-luks
Requires: %{__python3}
%if 0%{?suse_version}
Requires: python3-dbus-python
%else
Requires: python3-dbus
%endif
%endif
BuildArch: noarch

%description -n cockpit-storaged
The Cockpit component for managing storage.  This package uses udisks.

%files -n cockpit-storaged -f storaged.list
%{_datadir}/metainfo/org.cockpit-project.cockpit-storaged.metainfo.xml

%package -n cockpit-tests
Summary: Tests for Cockpit
Requires: cockpit-bridge >= 138
Requires: cockpit-system >= 138
Requires: /usr/bin/ssh-agent /usr/bin/ssh-add
Provides: cockpit-test-assets = %{version}

%description -n cockpit-tests
This package contains tests and files used while testing Cockpit.
These files are not required for running Cockpit.

%files -n cockpit-tests -f tests.list
%dir %{_sysconfdir}/cockpit
%config(noreplace) %{_sysconfdir}/cockpit/cockpit.conf
%{_prefix}/%{__lib}/cockpit-test-assets

%package -n cockpit-machines
BuildArch: noarch
Summary: Cockpit user interface for virtual machines
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-system >= %{required_base}
%if 0%{?suse_version}
Requires: libvirt-daemon-qemu
%else
Requires: libvirt-daemon-kvm
%endif
Requires: libvirt-client
%if 0%{?centos} == 0
Requires: libvirt-dbus >= 1.2.0
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
# Optional components
Recommends: virt-install
Recommends: libosinfo
Recommends: python3-gobject-base
%endif

%description -n cockpit-machines
The Cockpit components for managing virtual machines.

If "virt-install" is installed, you can also create new virtual machines.

%files -n cockpit-machines -f machines.list
%{_datadir}/metainfo/org.cockpit-project.cockpit-machines.metainfo.xml

%if 0%{?build_ovirt}

%package -n cockpit-machines-ovirt
BuildArch: noarch
Summary: Cockpit user interface for oVirt virtual machines
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-system >= %{required_base}
Requires: libvirt-daemon-kvm
Requires: libvirt-client

%description -n cockpit-machines-ovirt
The Cockpit components for managing oVirt virtual machines.

%files -n cockpit-machines-ovirt -f ovirt.list

%endif

%package -n cockpit-pcp
Summary: Cockpit PCP integration
Requires: cockpit-bridge >= %{required_base}
Requires: pcp

%description -n cockpit-pcp
Cockpit support for reading PCP metrics and loading PCP archives.

%files -n cockpit-pcp -f pcp.list
%dir %{_localstatedir}/lib/pcp
%dir %{_localstatedir}/lib/pcp/config
%dir %{_localstatedir}/lib/pcp/config/pmlogconf
%dir %{_localstatedir}/lib/pcp/config/pmlogconf/tools
%{_libexecdir}/cockpit-pcp
%{_localstatedir}/lib/pcp/config/pmlogconf/tools/cockpit

# %post -n cockpit-pcp
# HACK - https://bugzilla.redhat.com/show_bug.cgi?id=1185764
# We can't use "systemctl reload-or-try-restart" since systemctl might
# be out of sync with reality.
# /usr/share/pcp/lib/pmlogger condrestart

%if %{defined build_dashboard}
%package -n cockpit-dashboard
Summary: Cockpit remote servers and dashboard
%if 0%{?rhel} == 7
Provides: cockpit-ssh = %{version}
# nothing depends on the dashboard, but we can't use it with older versions of the bridge
Conflicts: cockpit-bridge < 135
# PR #10430 dropped workaround for ws' inability to understand x-host-key challenge
Conflicts: cockpit-ws < 173.1
%else
BuildArch: noarch
Requires: cockpit-ssh >= 135
Conflicts: cockpit-ws < 135
%endif

%description -n cockpit-dashboard
Cockpit support for connecting to remote servers (through ssh),
bastion hosts, and a basic dashboard.

%files -n cockpit-dashboard -f dashboard.list

%endif

%ifarch x86_64 %{arm} aarch64 ppc64le i686 s390x

%if 0%{?fedora} || 0%{?rhel} < 8
%package -n cockpit-docker
Summary: Cockpit user interface for Docker containers
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: /usr/bin/docker
# Requires: /usr/lib/systemd/system/docker.service
%if 0%{?fedora}
Requires: %{__python3}
%else
Requires: python2
%endif

%description -n cockpit-docker
The Cockpit components for interacting with Docker and user interface.
This package is not yet complete.

%files -n cockpit-docker -f docker.list

%endif
%endif

%if 0%{?build_kubernetes}

%package -n cockpit-kubernetes
Summary: Cockpit user interface for Kubernetes cluster
Requires: /usr/bin/kubectl
# Requires: Needs newer localization support
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
BuildRequires: %{go_scl_prefix}golang-bin
BuildRequires: %{go_scl_prefix}golang-src
Provides: cockpit-stub = %{version}

%description -n cockpit-kubernetes
The Cockpit components for visualizing and configuring a Kubernetes
cluster. Installed on the Kubernetes master. This package is not yet complete.

%if 0%{?rhel} >= 8
%enable_gotoolset7
%endif

%files -n cockpit-kubernetes -f kubernetes.list
%{_libexecdir}/cockpit-kube-auth
%{_libexecdir}/cockpit-kube-launch
%{_libexecdir}/cockpit-stub
%endif

%package -n cockpit-packagekit
Summary: Cockpit user interface for packages
BuildArch: noarch
Requires: cockpit-bridge >= %{required_base}
Requires: PackageKit

%description -n cockpit-packagekit
The Cockpit components for installing OS updates and Cockpit add-ons,
via PackageKit.

%files -n cockpit-packagekit -f packagekit.list

%endif # build optional extension packages

# The changelog is automatically generated and merged
%changelog
