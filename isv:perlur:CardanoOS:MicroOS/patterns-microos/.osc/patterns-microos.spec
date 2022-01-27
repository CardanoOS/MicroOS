#
# spec file for package patterns-microos
#
# Copyright (c) 2020 SUSE LLC
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


Name:           patterns-microos
Version:        5.0.0
Release:        0
Summary:        Patterns for SUSE Linux Enterprise Micro
License:        MIT
Group:          Metapackages
URL:            http://en.opensuse.org/Patterns
Source0:        %{name}-rpmlintrc
ExclusiveArch:  x86_64 armv7l armv7hl aarch64 ppc64le s390x

%description
This is an internal package that is used to create the patterns as part
of the installation source setup. Installation of this package does
not make sense.

%package basesystem
Summary:        SLE Micro Base System (alias pattern for microos-base)
Group:          Metapackages
Provides:       pattern() = basesystem
Provides:       pattern-icon() = pattern-kubic
Requires:       pattern() = microos-base
Obsoletes:	patterns-base-basesystem

%description basesystem
This is the SUSE Linux Enterprise Micro runtime system. It contains only a minimal multiuser
booting system.

%package base
Summary:        SUSE Linux Enterprise Micro
Group:          Metapackages
Provides:       pattern() = microos-base
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9010
Provides:       pattern-visible()
Requires:       distribution-release
Requires:       aaa_base
Requires:       audit
Requires:       bash
Requires:       btrfsmaintenance
Requires:       btrfsprogs
Requires:       ca-certificates
Requires:       ca-certificates-mozilla
Requires:       chrony
Requires:       coreutils
Requires:       cracklib-dict-small
Requires:       dosfstools
Requires:       dracut
Requires:       elfutils
Requires:       filesystem
Requires:       glibc
Requires:       haveged
Requires:       health-checker
Requires:       health-checker-plugins-MicroOS
Requires:       hwinfo
Requires:       iputils
### bsc#1174393
Requires:       issue-generator
Requires:       kbd
Requires:       kdump
Requires:       kernel-base
Requires:       kmod
Requires:       glibc-locale-base
Requires:       less
Requires:       libnss_usrfiles2
Requires:       login
Requires:       logrotate
Requires:       microos-tools
### not in SLES Requires:       nano
Requires:       net-tools
Requires:       openssh
Requires:       pam
Requires:       parted
Requires:       pkgconfig
Requires:       procps
Requires:       rebootmgr
Requires:       rpm
Requires:       shadow
Requires:       snapper
Requires:       sudo
Requires:       supportutils
Requires:       sysconfig
Requires:       sysfsutils
#Requires:       branding-SLE
# FIX branding to similar to SLES
%ifnarch s390x
Requires:	grub2-branding
%endif
Requires:       system-group-hardware
Requires:       system-group-wheel
Requires:       system-group-kvm
Requires:       system-user-nobody
Requires:       systemd
### fix branding
Requires:       systemd-presets-branding
### not in SLES Requires:       tallow
Requires:       terminfo
Requires:       timezone
Requires:       transactional-update
Requires:       transactional-update-zypp-config
Requires:       udev
Requires:       vlan
Requires:       which
Requires:       wicked
Requires:       xfsprogs
Requires:       yast2-logs
Requires:       zypper
Requires:       zypper-needs-restarting
Requires:	vim-small
### not in SLES Requires:       pattern() = bootloader
Conflicts:      gettext-runtime-mini
Conflicts:      krb5-mini
#Obsolete CaaSP Patterns
Provides:       patterns-caasp-MicroOS
Obsoletes:      patterns-caasp-MicroOS <= 4.0
#Requires:       openSUSE-build-key
#Obsoletes:      suse-build-key < 12.1

%description base
This is the SUSE Linux Enterprise Micro runtime system. It contains only a minimal multiuser
booting system.

%package defaults
Summary:        SUSE Linux Enterprise Micro Micro defaults
Group:          Metapackages
Provides:       pattern() = microos-defaults
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9011
Requires:       pattern() = microos-base
Requires:       systemd-logger
#Obsolete CaaSP Patterns
Provides:       patterns-caasp-MicroOS-defaults
Obsoletes:      patterns-caasp-MicroOS-defaults <= 4.0

%description defaults
This provides default packages for SUSE Linux Enterprise Micro which can be optionally
replaced by alternatives.

%package hardware
Summary:        Hardware Support
Group:          Metapackages
Provides:       pattern() = microos-hardware
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9030
Provides:       pattern-visible()
Requires:       fcoe-utils
Requires:       kernel-firmware
#Obsolete CaaSP Patterns
Provides:       patterns-caasp-hardware
Obsoletes:      patterns-caasp-hardware <= 4.0
%ifarch armv7l armv7hl
Requires:       kernel-lpae
%else
Requires:       kernel-default
%endif
%ifnarch s390x
Requires:       irqbalance
%endif

%description hardware
Packages required to install SUSE Linux Enterprise Micro on real hardware.

%package selinux
Summary:        SELinux Support
Group:          Metapackages
Provides:       pattern() = microos-selinux
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-generic
Provides:       pattern-order() = 9055
Provides:       pattern-visible()
Requires:       container-selinux
Requires:       policycoreutils
Requires:       selinux-policy-targeted
Requires:       selinux-tools

%description selinux
This are packages which are required to enable SELinux on SUSE Linux Enterprise Micro

%package salt_minion
Summary:        Salt Minion
Group:          Metapackages
Provides:       pattern() = microos-salt_minion
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-generic
Provides:       pattern-order() = 9901
Requires:       salt-minion

%description salt_minion
Packages to manage the host using Salt or management solutions which utilize Salt, e.g. SUSE Manager

%package kvm_host
Summary:        KVM Virtualization Host
Group:          Metapackages
Provides:       pattern() = microos-kvm_host
Provides:       pattern-category() = MicroOS
Provides:       pattern-icon() = pattern-generic
Provides:       pattern-order() = 9050
Provides:       pattern-visible()
Requires:       guestfs-tools
Requires:       python3-libvirt-python
Requires:       qemu-tools

# fix issue because qemu-kvm is not present on all arch and 
# we would like to deprecate it for the futur (will be only
# updated if already installed on the system)
%ifarch %ix86 x86_64
Requires:       qemu-x86
%endif
%ifarch ppc ppc64 ppc64le
Requires:       qemu-ppc
%endif
%ifarch s390x
Requires:       qemu-s390
%endif
%ifarch %arm aarch64 armv7hl
Requires:       qemu-arm
Requires:       qemu-ipxe
%endif
Requires:       tftp
Recommends:     libvirt-daemon-qemu
Recommends:     tigervnc
Recommends:     virt-install
Recommends:     vm-install

%description kvm_host
Packages to run virtual machines using the KVM hypervisor

%package container_runtime
Summary:        Container Runtime for non-clustered systems
Group:          Metapackages
Provides:       pattern() = microos-container_runtime
Provides:       pattern-category() = Containers
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 9040
Provides:       pattern-visible()
#Obsolete CaaSP Patterns
Provides:       patterns-caasp-container-runtime
Obsoletes:      patterns-caasp-container-runtime <= 4.0
Requires:       podman
Requires:       podman-cni-config
Requires:       toolbox
Requires:       pattern() = basesystem

%description container_runtime
This pattern installs the default container runtime packages for non-clustered systems.

%package cockpit
Summary: Web based remote system management
Group: Metapackages
Provides: pattern() = microos-cockpit
Provides: pattern-category() = MicroOS
Provides: pattern-icon() = pattern-generic
Provides: pattern-order() = 9060
Provides: pattern-visible()
# Podman pattern not yet available
# Requires: cockpit-podman
Requires: cockpit-system
Requires: cockpit-ws
Requires: cockpit

%description cockpit
Packages required to run the Cockpit system management service.
For the web service the cockpit-ws container is required.


%prep
# empty on purpose

%build
# empty on purpose

%install
mkdir -p %{buildroot}%{_docdir}/patterns-microos/
for i in basesystem base defaults hardware selinux salt_minion kvm_host container_runtime cockpit; do
	echo "This file marks the pattern $i to be installed." >%{buildroot}%{_docdir}/patterns-microos/$i.txt
done

%files basesystem
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/basesystem.txt

%files base
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/base.txt

%files defaults
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/defaults.txt

%files hardware
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/hardware.txt

%files selinux
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/selinux.txt

%files salt_minion
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/salt_minion.txt

%files kvm_host
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/kvm_host.txt

%files container_runtime
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/container_runtime.txt

%files cockpit
%dir %{_docdir}/patterns-microos
%{_docdir}/patterns-microos/cockpit.txt

%changelog
