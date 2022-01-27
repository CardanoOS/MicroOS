#
# spec file for package patterns-base
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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
#


%bcond_with betatest
Name:           patterns-base
Version:        20171206
Release:        0
Summary:        Patterns for Installation (base patterns)
License:        MIT
Group:          Metapackages
Url:            https://github.com/openSUSE/patterns
Source0:        %{name}-rpmlintrc
Source1:        pattern-definition-32bit.txt
Source2:        create_32bit-patterns_file.pl
BuildRequires:  patterns-rpm-macros

%description
This is an internal package that is used to create the patterns as part
of the installation source setup.  Installation of this package does
not make sense.

This particular package contains all the base / core patterns (and those that don't fit well anywhere else).

################################################################################

# bsc#1088669 - don't provide this on s390x
%ifnarch s390 s390x
%package 32bit
%pattern_basetechnologies
Summary:        32-Bit Runtime Environment
Group:          Metapackages
Provides:       pattern() = 32bit
Provides:       pattern-icon() = pattern-cli
Provides:       pattern-order() = 1180
Provides:       pattern-visible()
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-32bit = %{version}
Provides:       patterns-openSUSE-x86 = %{version}
Obsoletes:      patterns-openSUSE-32bit < %{version}
Obsoletes:      patterns-openSUSE-x86 < %{version}
%else
Provides:       patterns-sled-32bit = %{version}
Provides:       patterns-sles-32bit = %{version}
Obsoletes:      patterns-sled-32bit < %{version}
Obsoletes:      patterns-sles-32bit < %{version}
%endif

%description 32bit
This will install the 32-bit variant of all selected patterns. This allows to execute 32-bit software.

%files 32bit
%dir %{_docdir}/patterns
%{_docdir}/patterns/32bit.txt
%endif

################################################################################

%package apparmor
%pattern_basetechnologies
Summary:        AppArmor
Group:          Metapackages
Provides:       pattern() = apparmor
Provides:       pattern-icon() = pattern-apparmor
Provides:       pattern-order() = 1100
Provides:       pattern-visible()
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-apparmor = %{version}
Obsoletes:      patterns-openSUSE-apparmor < %{version}
%else
Provides:       patterns-sled-apparmor = %{version}
Provides:       patterns-sles-apparmor = %{version}
Obsoletes:      patterns-sled-apparmor < %{version}
Obsoletes:      patterns-sles-apparmor < %{version}
%endif
Requires:       pattern() = minimal_base
%if 0%{?is_opensuse}
Recommends:     pattern() = apparmor_opt
%endif

Requires:       apparmor-abstractions
Requires:       apparmor-parser
Requires:       apparmor-profiles
Recommends:     apparmor-docs
Recommends:     apparmor-utils
Recommends:     yast2-apparmor
Suggests:       pam_apparmor
%if 0%{?is_opensuse}
Requires:       audit
%else
Recommends:     audit
%endif

%description apparmor
AppArmor is an application security framework that provides mandatory access control for programs. It protects from exploitation of software flaws and compromised systems. It offers an advanced tool set that automates the development of per-program application security without requiring additional knowledge.

%files apparmor
%dir %{_docdir}/patterns
%{_docdir}/patterns/apparmor.txt

################################################################################

%if 0%{?is_opensuse}
%package apparmor_opt
%pattern_basetechnologies
Summary:        AppArmor
Group:          Metapackages
Provides:       pattern() = apparmor_opt
Provides:       pattern-extends() = apparmor
Provides:       pattern-icon() = pattern-apparmor
Provides:       pattern-order() = 1080
Provides:       patterns-openSUSE-apparmor_opt = %{version}
Obsoletes:      patterns-openSUSE-apparmor_opt < %{version}
Requires:       pattern() = minimal_base

Requires:       apparmor-docs

%description apparmor_opt
AppArmor is an application security framework that provides mandatory access control for programs. It protects from exploitation of software flaws and compromised systems. It offers an advanced tool set that automates the development of per-program application security without requiring additional knowledge.

%files apparmor_opt
%dir %{_docdir}/patterns
%{_docdir}/patterns/apparmor_opt.txt
%endif

################################################################################

%package basesystem
%pattern_basetechnologies
Summary:        Minimal Base System (alias pattern for base)
Group:          Metapackages
Requires:       pattern() = minimal_base
Provides:       pattern() = basesystem
Provides:       pattern-icon() = pattern-basis

%description basesystem
This is the base runtime system.  It contains only a minimal multiuser booting system. For running on real hardware, you need to add additional packages and pattern to make this pattern useful on its own.

%files basesystem
%dir %{_docdir}/patterns
%{_docdir}/patterns/basesystem.txt

################################################################################

%package base
%pattern_basetechnologies
Summary:        Minimal Base System
Group:          Metapackages
Provides:       pattern() = base
Provides:       pattern-icon() = pattern-basis
Provides:       pattern-order() = 1030
Provides:       pattern-visible()
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-base = %{version}
Obsoletes:      patterns-openSUSE-base < %{version}
%else
Provides:       patterns-sles-minimal
Provides:       patterns-sles-base
Obsoletes:      patterns-sles-minimal < %{version}
Obsoletes:      patterns-sles-base < %{version}
%endif
Requires:       pattern() = minimal_base

Requires:       kbd
Requires:       openssh
Requires:       polkit
Requires:       polkit-default-privs
Requires:       shadow
Requires:       util-linux
Requires:       which
Recommends:     ca-certificates-mozilla
Recommends:     grub2
Recommends:     systemd-sysvinit
Recommends:     chrony
Recommends:     cron
# we rely on cron for daily/hourly
Recommends:     cronie
%if 0%{?is_opensuse}
# get it branded
Recommends:     branding-openSUSE
%else
Recommends:     branding-SLE
%endif
%ifarch %ix86 x86_64
%endif
%ifarch x86_64
Recommends:     shim
%endif
%ifarch ppc ppc64 ppc64le
%if !0%{?is_opensuse}
Recommends:     lshw
Recommends:     lsvpd
%endif
%endif
%ifarch ppc64 ppc64le
# bsc#1098849
Requires:     ppc64-diag
%endif


%description base
This is the base runtime system.  It contains only a minimal multiuser booting system. For running on real hardware, you need to add additional packages and pattern to make this pattern useful on its own.

%files base
%dir %{_docdir}/patterns
%{_docdir}/patterns/base.txt

################################################################################

%if 0%{?is_opensuse}
%package console
%pattern_basetechnologies
Summary:        Console Tools
Group:          Metapackages
Provides:       pattern() = console
Provides:       pattern-icon() = pattern-cli
Provides:       pattern-order() = 1120
Provides:       pattern-visible()
Provides:       patterns-openSUSE-console = %{version}
Obsoletes:      patterns-openSUSE-console < %{version}
Requires:       pattern() = enhanced_base
Recommends:     pattern() = yast2_basis

Recommends:     ed
Recommends:     emacs-nox
Recommends:     w3m
# #378747
Suggests:       cryptconfig
Suggests:       lftp
Suggests:       mlocate
Suggests:       mutt
%if 0%{?is_opensuse}
Recommends:     at
Recommends:     bc
Recommends:     libyui-ncurses
Recommends:     libyui-ncurses-pkg
Recommends:     mc
Recommends:     mosh
Recommends:     mtools
Recommends:     sensors
Recommends:     susepaste
Recommends:     susepaste-screenshot
Recommends:     tmux
Suggests:       alpine
Suggests:       bsd-games
Suggests:       cnetworkmanager
Suggests:       convert
Suggests:       dar
Suggests:       ding
Suggests:       gcal
Suggests:       grepmail
Suggests:       irssi
Suggests:       links
Suggests:       lynx
Suggests:       minicom
Suggests:       ncftp
Suggests:       pico
Suggests:       pinfo
Suggests:       slrn
Suggests:       units
Suggests:       vlock
%endif

%description console
Applications useful for those using the console and no graphical desktop environment.

%files console
%dir %{_docdir}/patterns
%{_docdir}/patterns/console.txt
%endif

################################################################################

%package documentation
%pattern_documentation
Summary:        Help and Support Documentation
Group:          Metapackages
Provides:       pattern() = documentation
Provides:       pattern-icon() = pattern-documentation
Provides:       pattern-order() = 1005
Provides:       pattern-visible()
Requires:       pattern() = basesystem
%if !0%{?is_opensuse}
Provides:       patterns-sled-documentation
Provides:       patterns-sled-documentation
Obsoletes:      patterns-sles-documentation < %{version}
Obsoletes:      patterns-sles-documentation < %{version}
%endif

Recommends:     info2html
Recommends:     man-pages
# TODO: those should use packageand to get installed
Recommends:     nfs-doc
Recommends:     pam-doc
Recommends:     susehelp
Recommends:     susehelp_en
%if !0%{?is_opensuse}
Recommends:     sled-admin_en-pdf
Recommends:     sled-gnomeuser_en-pdf
Recommends:     sled-manuals_en-pdf
Recommends:     sled-security_en-pdf
Recommends:     sled-tuning_en-pdf
%endif

%description documentation
Help and Support Documentation

%files documentation
%dir %{_docdir}/patterns
%{_docdir}/patterns/documentation.txt

################################################################################

%package enhanced_base
%pattern_basetechnologies
Summary:        Enhanced Base System
Group:          Metapackages
Provides:       pattern() = enhanced_base
Provides:       pattern-icon() = pattern-basis
Provides:       pattern-order() = 1060
Provides:       pattern-visible()
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-enhanced_base = %{version}
Obsoletes:      patterns-openSUSE-enhanced_base < %{version}
%endif
Requires:       pattern() = base
Recommends:     pattern() = apparmor

%if 0%{?is_opensuse}
Recommends:     pattern() = enhanced_base_opt
%endif

# firewall by default
Recommends:     firewalld
Recommends:     aaa_base-extras
# getfacl and setfacl
Recommends:     acl
# #302569
Recommends:     alsa-plugins
# getattr and setattr
Recommends:     attr
Recommends:     autofs
Recommends:     bind-utils
Recommends:     binutils
# compressor is interesting
Recommends:     bzip2
# #375103
Recommends:     cifs-utils
Recommends:     command-not-found
Recommends:     cpio
Recommends:     cpupower
Recommends:     cryptsetup
# cups server for remote printing queues
Recommends:     cups
# printing considered cool
Recommends:     cups-client
Recommends:     curl
Recommends:     cyrus-sasl
Recommends:     cyrus-sasl-crammd5
Recommends:     cyrus-sasl-digestmd5
Recommends:     cyrus-sasl-gssapi
Recommends:     cyrus-sasl-plain
# bnc#430895
# cyrus-sasl-saslauthd
# delta rpms are considered cool for updates
Recommends:     deltarpm
Recommends:     diffutils
Recommends:     dos2unix
Recommends:     e2fsprogs
Recommends:     file
Recommends:     fillup
Recommends:     findutils
Recommends:     fuse
Recommends:     gawk
Recommends:     genisoimage
Recommends:     gettext-runtime
Recommends:     gpart
Recommends:     gpg2
Recommends:     gpm
Recommends:     grep
Recommends:     grub2
Recommends:     gzip
Recommends:     hdparm
Recommends:     hwinfo
Recommends:     info
Recommends:     initviocons
# /bin/ip considered useful
Recommends:     iproute2
# ping is required for network tests
Recommends:     iputils
Recommends:     irqbalance
Recommends:     kmod-compat
Recommends:     krb5
Recommends:     joe

# #303857
Recommends:     kpartx
# pager
Recommends:     less
Recommends:     logrotate
Recommends:     lsscsi
Recommends:     mailx
# man by default (#304687)
Recommends:     man
# needed for detecting software raid - required by yast2-storage too
Recommends:     mdadm
Requires:       multipath-tools
# split out of ncurses
Recommends:     ncurses-utils
Recommends:     net-tools
Recommends:     netcat-openbsd
Recommends:     netcfg
Recommends:     net-snmp
Recommends:     nfs-client
Recommends:     nfsidmap
Recommends:     nscd
Recommends:     openslp
# we want a ssh server to be available
Recommends:     openssh
Recommends:     pam-config
Recommends:     parted
Recommends:     pciutils
Recommends:     pciutils-ids
Recommends:     pcre
Recommends:     perl-Bootloader
Recommends:     perl-base
Recommends:     permissions
Recommends:     pinentry
Recommends:     popt
Recommends:     postfix
# we still want /var/log/messages as all of the docu refers to it
Recommends:     rsyslog
Recommends:     rsync
# Bug 424707 - Feature "Command not found" for openSUSE by default
Recommends:     scout
Recommends:     screen
Recommends:     sed
Recommends:     sg3_utils
Recommends:     smartmontools
Recommends:     sysconfig
Recommends:     systemd-sysvinit
Recommends:     time
Recommends:     timezone
Recommends:     translation-update
Recommends:     udev
# autoconfig new printers - bnc#808014
Recommends:     udev-configure-printer
# lsusb is good for debugging USB devices - #401593
Recommends:     usbutils
# Our editor of choice
Recommends:     vim
Recommends:     wget
Recommends:     xauth
Recommends:     xz
Recommends:     zisofs-tools
Recommends:     zlib
# DELL computers mainly #403270, but #441079
Suggests:       biosdevname
Suggests:       cpupower
# #437252
Suggests:       pam_ssh
Suggests:       zip
%ifarch aarch64 %ix86 x86_64
Recommends:     dmidecode
%endif
%ifarch ppc
Recommends:     hfsutils
%endif
%ifarch ppc
# #303737
Recommends:     mouseemu
Recommends:     pdisk
Recommends:     powerpc32
%endif
# openSUSE Branding packages first
%if 0%{?is_opensuse}
# Make plymouth the new default bootsplash
# we want a branded grub2 too #757683
Recommends:     grub2-branding-openSUSE
Recommends:     plymouth
# we want a branded boot
Recommends:     plymouth-branding-openSUSE
Recommends:     release-notes-openSUSE
%else
Recommends:     plymouth
Recommends:     grub2-branding-SLE
%endif
# Packages which were pulled by base_compat
# might want to put them as Requires

Recommends:     OpenIPMI
Recommends:     bash-completion
Recommends:     cpp
Recommends:     cryptconfig
Recommends:     expect
Recommends:     ipmitool
Recommends:     lvm2
Recommends:     m4
Recommends:     make
Recommends:     mksh
Recommends:     mutt
Recommends:     quota
Recommends:     supportutils
Recommends:     sysfsutils
Recommends:     tcsh
Recommends:     w3m
Recommends:     lsof
# fuser (psmisc) by default (#304694)
Recommends:     psmisc
Recommends:     sudo

Recommends:     ethtool
# mount NTFS rw (bsc#1087242)
Recommends:     ntfs-3g
Recommends:     ntfsprogs

# Other packages we have in openSUSE and not SLE-15
%if 0%{?is_opensuse}
Recommends:     dmraid
Recommends:     dosfstools
Recommends:     ifplugd
Recommends:     klogd
# boo#1034493
Recommends:     nano
Recommends:     openldap2-client
Recommends:     prctl
Recommends:     recode
Recommends:     smp_utils
# useful for debugging
Recommends:     strace
Recommends:     syslinux
# having a ftp command line client is good for moving log files
Recommends:     tnftp
Recommends:     tuned
Recommends:     wireless-tools
Recommends:     wol
%ifarch %ix86 x86_64
Recommends:     acpica
%endif
%ifarch x86_64
Recommends:     mcelog
%endif
%ifarch aarch64 x86_64
Recommends:     numactl
%endif
%ifarch %ix86 x86_64
Recommends:     ucode-amd
Recommends:     ucode-intel
%endif
%endif

%description enhanced_base
This is the enhanced base runtime system with lots of convenience packages.

%files enhanced_base
%dir %{_docdir}/patterns
%{_docdir}/patterns/enhanced_base.txt

################################################################################

%if 0%{?is_opensuse}
%package enhanced_base_opt
%pattern_basetechnologies
Summary:        Enhanced Base System
Group:          Metapackages
Provides:       pattern() = enhanced_base_opt
Provides:       pattern-extends() = enhanced_base
Provides:       pattern-icon() = pattern-software-management
Provides:       pattern-order() = 1040
Provides:       patterns-openSUSE-enhanced_base_opt = %{version}
Obsoletes:      patterns-openSUSE-enhanced_base_opt < %{version}

Suggests:       cracklib-dict-full
Suggests:       groff
Suggests:       man-pages-posix
# needed as soon as you want to do kerberos authentication
Suggests:       cyrus-sasl-gssapi
Suggests:       hfsutils
Suggests:       unzip
# #754959
%ifarch %ix86 x86_64
Suggests:       hyper-v
%endif
Suggests:       finger
Suggests:       joe
Suggests:       ksymoops
Suggests:       man-pages
Suggests:       mpt-status
Suggests:       perl-TermReadLine-Gnu
Suggests:       prctl
Suggests:       procinfo
Suggests:       procmail
Suggests:       providers
Suggests:       setserial
Suggests:       sharutils
Suggests:       spax
Suggests:       strace
Suggests:       tcpdump
Suggests:       telnet
Suggests:       terminfo
Suggests:       vlan
Suggests:       wol
Suggests:       acpid
Suggests:       delayacct-utils
# bnc#388570
Suggests:       kerneloops
Suggests:       ocfs2-tools
Suggests:       pwgen
Suggests:       w3m-el
# delta apply
Suggests:       xdelta
# tool for xfs
Suggests:       xfsdump

%description enhanced_base_opt
This is the enhanced base runtime system with lots of convenience packages.

%files enhanced_base_opt
%dir %{_docdir}/patterns
%{_docdir}/patterns/enhanced_base_opt.txt
%endif

################################################################################

%package minimal_base
%pattern_basetechnologies
Summary:        Minimal Appliance Base
Group:          Metapackages
Provides:       pattern() = minimal_base
Provides:       pattern-icon() = pattern-basis
Provides:       pattern-order() = 5190
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-minimal_base = %{version}
Obsoletes:      patterns-openSUSE-minimal_base < %{version}
%endif
%if 0%{?is_opensuse}
Recommends:     pattern() = minimal_base_conflicts
%endif

Requires:       aaa_base
Requires:       bash
Requires:       coreutils
Requires:       device-mapper
Requires:       dracut
Requires:       e2fsprogs
Requires:       filesystem
Requires:       glibc
Requires:       kbd
Requires:       kmod
Requires:       pam
Requires:       procps
# Support multiversion(kernel) (jsc#SLE-10162)
Requires:       purge-kernels-service
Requires:       rpm
Requires:       sysconfig
Requires:       system-group-hardware
Requires:       system-user-nobody
Requires:       systemd
Requires:       zypper
Recommends:     btrfsprogs
# Add some static base tool in case system explodes
Recommends:     busybox-static
Recommends:     elfutils
Recommends:     glibc-locale-base
Recommends:     glibc-locale
Recommends:     grub2
Recommends:     iproute2
Recommends:     openssh
Recommends:     snapper
Recommends:     system-group-trusted
Recommends:     system-group-wheel
Recommends:     system-user-bin
Recommends:     system-user-daemon
%if ! 0%{?is_opensuse}
Recommends:     systemd-coredump
%endif
Recommends:     sysvinit-tools
Recommends:     tar
Recommends:     terminfo
Recommends:     terminfo-iterm
Recommends:     terminfo-screen
Recommends:     timezone
Recommends:     udev
Suggests:       ed
%if 0%{?is_opensuse}
Requires:       openSUSE-build-key
Requires:       distribution-release
%else
Recommends:     rollback-helper
Recommends:     SUSEConnect
Recommends:     suse-build-key
%endif
%ifarch x86_64 %arm
Recommends:     efibootmgr
%endif

# bsc#1095916
Recommends:     xfsprogs
# Current systems suffer from entropy starvation (bsc#1131369)
%ifarch aarch64 %ix86 x86_64 ppc64 ppc64le s390x
Recommends:     haveged
%endif
# issue-generator is not used on Leap so far (boo#1133636)
%if !(0%{?is_opensuse} && 0%{?sle_version})
Recommends:     issue-generator
%endif

%if 0%{?is_opensuse}
%description minimal_base
This is the minimal openSUSE runtime system. It is really a minimal system, you can login and a shell will be started, that's all. It is intended as base for Appliances.
%else
%description minimal_base
This is the minimal SLE runtime system. It is really a minimal system, you can login and a shell will be started, that's all. It is intended as base for Appliances.
%endif


%files minimal_base
%dir %{_docdir}/patterns
%{_docdir}/patterns/minimal_base.txt

################################################################################

%package transactional_base
%pattern_basetechnologies
Summary:        Transactional Base System
Group:          Metapackages
Provides:       pattern() = transactional_base
Provides:       pattern-icon() = pattern-kubic
Provides:       pattern-order() = 1050
Obsoletes:      pattern() = readonly_root_tools
Requires:       pattern() = base
Recommends:     pattern() = enhanced_base

Requires:       read-only-root-fs
Requires:       systemd-presets-branding-transactional-server
Requires:       transactional-update
Requires:       transactional-update-zypp-config
Suggests:       health-checker
Requires:       rebootmgr

%description transactional_base
This is the base system for a host updated by Transactional Updates. Includes Tools for systems with a read-only root filesystem.

%files transactional_base
%dir %{_docdir}/patterns
%{_docdir}/patterns/transactional_base.txt

################################################################################

%package sw_management
%pattern_basetechnologies
Summary:        Software Management
Group:          Metapackages
Provides:       pattern() = sw_management
Provides:       pattern-icon() = pattern-software-management
Provides:       pattern-order() = 1360
Provides:       pattern-visible()
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-sw_management = %{version}
Obsoletes:      patterns-openSUSE-sw_management < %{version}
%endif
Recommends:     pattern() = sw_management_x11
%if %{with betatest}
Requires:       pattern() = update_test
%endif
# Zypper is the basic sw_management stack for *SUSE
Requires:       zypper
%if 0%{?sle_version}
Recommends:     lifecycle-data
Recommends:     zypper-lifecycle-plugin
%endif

%description sw_management
This pattern provides a graphical application and a command line tool for keeping your system up to date.

%files sw_management
%dir %{_docdir}/patterns
%{_docdir}/patterns/sw_management.txt

################################################################################

%if 0%{?is_opensuse}
%package update_test
%pattern_basetechnologies
Summary:        Tests for the Update Stack
Group:          Metapackages
Provides:       patterns-openSUSE-update_test = %{version}
Provides:       pattern() = update_test
Provides:       pattern-icon() = pattern-tests
Provides:       pattern-order() = 1380
Provides:       pattern-visible()
Obsoletes:      patterns-openSUSE-update_test < %{version}

Requires:       update-test-affects-package-manager
Requires:       update-test-interactive
Requires:       update-test-optional
Requires:       update-test-reboot-needed
Requires:       update-test-security
Requires:       update-test-trivial
%if %{with betatest}
Requires:       aaa_base-malloccheck
%endif

%description update_test
Packages used for testing that the update stack works.  These tiny packages do not have any functionality themselves.

%files update_test
%dir %{_docdir}/patterns
%{_docdir}/patterns/update_test.txt
%endif

################################################################################

%package x11
%pattern_graphicalenvironments
Summary:        X Window System
Group:          Metapackages
Provides:       pattern() = x11
Provides:       pattern-icon() = pattern-x11
Provides:       pattern-order() = 1800
Provides:       pattern-visible()
Requires:       pattern() = base
%if 0%{?is_opensuse}
Provides:       patterns-openSUSE-x11 = %{version}
Obsoletes:      patterns-openSUSE-x11 < %{version}
%endif
%if 0%{?is_opensuse}
Recommends:     pattern() = x11_enhanced
Recommends:     pattern() = x11_opt
%endif

Requires:       xorg-x11-fonts-core
Requires:	xorg-x11-server
# bsc#1071953
%ifnarch s390 s390x
Requires:       xf86-input-libinput
Recommends:     xf86-input-vmmouse
Recommends:     xf86-input-wacom
%endif

Recommends:	xorg-x11
Recommends:	x11-tools
Recommends:	xorg-x11-driver-video
Recommends:	xorg-x11-essentials
Recommends:	xorg-x11-server-extra

Recommends:     xorg-x11-fonts
# required by xdm
# Requires:       xterm
# FIXME really requires ?
Requires:       yast2-qt
Recommends:     dejavu-fonts
Recommends:     google-roboto-fonts
Recommends:     icewm-theme-branding
# chooce icewm-default if you have a choice
# icewm-lite is too lightweight in new release
Recommends:     icewm-default
# Recommend lightdm so it gets installed by default
# rather then xdm bsc#1081760
Recommends:     lightdm
Recommends:     noto-sans-fonts
Recommends:     tigervnc
# really ??
# Recommends:     unclutter
Recommends:     xdmbgrd
Recommends:     xorg-x11-Xvnc
Recommends:     xtermset
Recommends:     xterm
Recommends:     libyui-qt
Recommends:     libyui-qt-pkg
Recommends:     yast2-control-center
# gnome version of askpass doesn't make sense on must openSUSE desktops (boo#1124865)
%if !0%{?is_opensuse}
Recommends:     openssh-askpass-gnome
%endif

%description x11
The X Window System provides the only standard platform-independent networked graphical window system bridging the heterogeneous platforms in today's enterprise: from network servers to desktops, thin clients, laptops, and handhelds, independent of operating system and hardware.

%files x11
%dir %{_docdir}/patterns
%{_docdir}/patterns/x11.txt

################################################################################

%package x11_enhanced
%pattern_graphicalenvironments
Summary:        X Window System
Group:          Metapackages
Provides:       pattern() = x11_enhanced
Provides:       pattern-icon() = pattern-x11
Provides:       pattern-order() = 1801
#Provides:       pattern-visible()
%if 0%{?is_opensuse}
Obsoletes:      patterns-openSUSE-x11 < %{version}
%else
Provides:       patterns-sled-minimal
Obsoletes:      patterns-sled-minimal < %{version}
%endif
Requires:       pattern() = enhanced_base
Requires:       pattern() = fonts
Requires:       pattern() = x11
Recommends:     pattern() = x11_yast
%if 0%{?is_opensuse}
Recommends:     pattern() = x11_opt
%endif

# 1057377
Requires:       glibc-locale-base
Requires:       glibc-locale
Requires:       xkeyboard-config
Recommends:     MozillaFirefox
Recommends:     MozillaFirefox-translations
Recommends:     cabextract
Recommends:     command-not-found
Recommends:     dialog
Recommends:     dbus-1-glib
Recommends:     dbus-1-x11
Recommends:     fontconfig
Recommends:     fonts-config
Recommends:     fribidi
Recommends:     ghostscript-x11
Recommends:     numlockx
# #353229 - drag in empty replacements
Recommends:     translation-update
Recommends:     xauth
Recommends:     xdmbgrd
Recommends:     xkeyboard-config
Recommends:     xorg-x11-fonts
Recommends:     xorg-x11-fonts-core
Recommends:     yast2-control-center-gnome
Recommends:     yast2-scanner
%if 0%{?is_opensuse}
# #394406
Suggests:       desktop-data-openSUSE-extra
%else
Recommends:     MozillaFirefox-branding-SLE
Recommends:     desktop-data-SLE
%endif
%if 0%{?is_opensuse}
# people love having numlock configurable
Recommends:     numlockx
Recommends:     openssh-askpass
Recommends:     susepaste
Recommends:     susepaste-screenshot
Suggests:       gvim
Suggests:       hexchat
Suggests:       wpa_supplicant-gui
%endif

%description x11_enhanced
The X Window System provides the only standard platform-independent networked graphical window system bridging the heterogeneous platforms in today's enterprise: from network servers to desktops, thin clients, laptops, and handhelds, independent of operating system and hardware.

%files x11_enhanced
%dir %{_docdir}/patterns
%{_docdir}/patterns/x11_enhanced.txt

################################################################################

%if 0%{?is_opensuse}
%package x11_opt
%pattern_graphicalenvironments
Summary:        X Window System
Group:          Metapackages
Provides:       pattern() = x11_opt
Provides:       pattern-extends() = x11
Provides:       pattern-icon() = pattern-x11
Provides:       pattern-order() = 1680
Provides:       patterns-openSUSE-x11_opt = %{version}
Obsoletes:      patterns-openSUSE-x11_opt < %{version}
Requires:       pattern() = enhanced_base
Requires:       pattern() = fonts

# needed e.g. for nvidia drivers
# #302566
Recommends:     x11-tools
Recommends:     xorg-x11-libX11-ccache
Suggests:       xorg-x11-driver-video-radeonhd
Suggests:       xorg-x11-driver-video-unichrome
Suggests:       MozillaThunderbird
Suggests:       WindowMaker
Suggests:       WindowMaker-applets
Suggests:       WindowMaker-themes
Suggests:       unclutter
Suggests:       xlockmore
# #389816
Suggests:       xorg-x11-server-sdk

%description x11_opt
The X Window System provides the only standard platform-independent networked graphical window system bridging the heterogeneous platforms in today's enterprise: from network servers to desktops, thin clients, laptops, and handhelds, independent of operating system and hardware.

%files x11_opt
%dir %{_docdir}/patterns
%{_docdir}/patterns/x11_opt.txt
%endif

################################################################################

%ifarch armv6hl armv7hl aarch64
%package x11_raspberrypi
%pattern_graphicalenvironments
Summary:        X Window System
Group:          Metapackages
Provides:       pattern() = x11_raspberrypi
Provides:       pattern-icon() = pattern-x11
Provides:       pattern-order() = 1803
Provides:       pattern-visible()
# Use only Requires - it's meant to be used on JeOS, which ignores Recommends
# Based on SUSE:SLE-15:GA:RaspberryPI/kiwi-templates-SLES15-JeOS/JeOS.kiwi
# Patterns
Requires:       pattern() = base
Requires:       pattern() = x11
# Drivers
Requires:       xf86-input-evdev
Requires:       xf86-input-libinput
Requires:       xf86-video-fbdev
# Other X11 packages
Requires:       gconf2
Requires:       xfd
Requires:       xfontsel
Requires:       xgamma
Requires:       xhost
Requires:       xinit
Requires:       xinput
Requires:       xkbcomp
Requires:       xkbevd
Requires:       xkbprint
Requires:       xkbutils
Requires:       xkeyboard-config
Requires:       xkill
Requires:       xlogo
Requires:       xlsatoms
Requires:       xlsclients
Requires:       xlsfonts
Requires:       xmag
Requires:       xmessage
Requires:       xmodmap
Requires:       xorg-x11
Requires:       xorg-x11-fonts-core
Requires:       xorg-x11-server
Requires:       xorg-x11-server-extra
Requires:       xprop
Requires:       xrandr
Requires:       xrdb
Requires:       xrestop
Requires:       xscope
Requires:       xscreensaver
Requires:       xscreensaver-data
Requires:       xset
Requires:       xsetmode
Requires:       xsetpointer
Requires:       xsetroot
Requires:       xterm
Requires:       xtermset
Requires:       xvinfo
Requires:       xwd
Requires:       xwininfo
Requires:       xdm
Requires:       x11-tools
Requires:       x11perf
Requires:       xauth
Requires:       xbacklight
Requires:       xclock
Requires:       xconsole
Requires:       xcursor-themes
Requires:       xcursorgen
Requires:       xdg-user-dirs
Requires:       xdg-user-dirs-gtk
Requires:       xdg-user-dirs-gtk-lang
Requires:       xdg-utils
Requires:       xdmbgrd
Requires:       xdpyinfo
Requires:       xev
Requires:       xeyes
Requires:       yast2-x11
Requires:       yast2-packager
Requires:       yast2-snapper
# bsc#1095870
Requires:       libyui-qt-pkg
Requires:       libyui-ncurses-pkg
Requires:       yast2-control-center-qt
Requires:       gtk3-metatheme-adwaita
Requires:       gtk2-metatheme-adwaita
# Branding
%if ! 0%{?is_opensuse}
Requires:       MozillaFirefox-branding-SLE
%endif
# X11/IceWM-specific packages
Requires:       icewm
Requires:       icewm-lite
Requires:       icewm-default
Requires:       icewm-theme-branding
Requires:       polkit-gnome-lang
Requires:       polkit-default-privs
# for IceWM taskbar mailbox icon (bsc#1093913)
Requires:       mutt
Requires:       mutt-lang

%description x11_raspberrypi
The X Window System provides the only standard platform-independent networked graphical window system bridging the heterogeneous platforms in today's enterprise: from network servers to desktops, thin clients, laptops, and handhelds, independent of operating system and hardware.

%files x11_raspberrypi
%dir %{_docdir}/patterns
%{_docdir}/patterns/x11_raspberrypi.txt
%endif

################################################################################

%prep

%build

%install
mkdir -p %{buildroot}%{_docdir}/patterns
%if 0%{?is_opensuse}
for i in apparmor base enhanced_base minimal_base \
     sw_management x11 x11_enhanced; do
 %else
for i in apparmor base enhanced_base minimal_base sw_management x11 x11_enhanced; do
%endif
    echo "This file marks the pattern $i to be installed." \
    >"%{buildroot}%{_docdir}/patterns/$i.txt"
    echo "This file marks the pattern $i to be installed." \
    >"%{buildroot}%{_docdir}/patterns/$i-32bit.txt"
done

# These packages don't generate a 32bit pattern
for i in \
%if 0%{?is_opensuse}
32bit apparmor_opt basesystem console documentation enhanced_base_opt transactional_base update_test x11_opt \
%else
%ifnarch s390 s390x
32bit \
%endif
basesystem documentation transactional_base \
%endif
%ifarch armv6hl armv7hl aarch64
x11_raspberrypi \
%endif
; do
    echo "This file marks the pattern $i to be installed." \
    >"%{buildroot}%{_docdir}/patterns/$i.txt"
done

#
# This file is created at check-in time. Sorry for the inconsistent workflow :(
#
%include %{SOURCE1}

%changelog
