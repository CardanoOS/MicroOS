#
# spec file for package iodine-tools
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
#


Name:           microos-devel-tools
Version:        0
Release:        0
Summary:        some tools
License:        MIT
Source0:        rpm-sortbysize     
Source1:        microos-rw
Source2:        microos-ro
Source3:        rpmorphan.c
Source10:       macros.microos-runtime
Source20:       dracut.conf
BuildRequires:  gcc
BuildRequires:  pkgconfig(rpm)

%description
Some tools for debugging etc

%package rpm-macros
License:        MIT
Summary:        some tools

%description rpm-macros
RPM macros for MicroOS runtime

%package dracut
License:        MIT
Summary:        dracut config for MicroOS

%description dracut
dracut config for MicroOS

%prep
%setup -qcT
gcc -o rpmorphan -Wall -g %{optflags} `pkg-config --cflags rpm` %{SOURCE3} `pkg-config --libs rpm`

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 %{SOURCE0} %{buildroot}%{_bindir}
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}
install -m 755 rpmorphan %{buildroot}%{_bindir}
install -D -m 0644 %{SOURCE10} %{buildroot}%{_prefix}/lib/rpm/macros.d/macros.microos-runtime
install -D -m 0644 %{SOURCE20} %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/50-noi18n.conf


%files
%defattr(-,root,root)
%{_bindir}/rpm-sortbysize
%{_bindir}/rpmorphan
%{_bindir}/microos-rw
%{_bindir}/microos-ro

%files rpm-macros
%defattr(-,root,root)
%{_prefix}/lib/rpm/macros.d/macros.microos-runtime

%files dracut
%defattr(-,root,root)
%dir %{_prefix}/lib/dracut
%dir %{_prefix}/lib/dracut/dracut.conf.d
%{_prefix}/lib/dracut/dracut.conf.d/50-noi18n.conf

%changelog
