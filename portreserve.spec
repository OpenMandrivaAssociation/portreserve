Summary:	TCP port reservation utility
Name:		portreserve
Version:	0.0.0
Release:	%mkrel 2
License:	GPL
Group:		System/Base
URL:		http://cyberelk.net/tim/portreserve/
Source0:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2
Source1:	portreserve.init
Source2:	portreserve-man_pages.tar.gz
Patch0:		portreserve_0.0.0-4.diff
Patch1:		portreserve-0.0.0-socket_dir.diff
Patch2:		portreserve-antibork.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper

%description
The portreserve program aims to help services with well-known ports that lie in
the portmap range.  It prevents portmap from a real service's port by occupying
it itself, until the real service tells it to release the port (generally in
the init script).

%prep

%setup -q -a2
%patch0 -p1 -b .debian
%patch1 -p1 -b .socket_dir
%patch2 -p0 -b .antibork

cp %{SOURCE1} portreserve-mandriva.init

%build
autoreconf

%configure2_5x \
    --sbindir=/sbin

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_localstatedir}/%{name}
install -d %{buildroot}%{_mandir}/man1

%makeinstall_std

install -m0755 portreserve-mandriva.init %{buildroot}%{_initrddir}/%{name}

install -m0644 doc/portrelease.1 %{buildroot}%{_mandir}/man1/
install -m0644 doc/portreserve.1 %{buildroot}%{_mandir}/man1/

%preun
%_preun_service %{name}

%post
%_post_service %{name}

%postun
if [ "$1" -ge "1" ]; then
    /sbin/service %{name} condrestart >/dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README debian/README.Debian debian/changelog
%dir %attr(0711,root,root) %{_localstatedir}/%{name}
%dir %attr(0711,root,root) %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) /sbin/*
%{_mandir}/man1/*
