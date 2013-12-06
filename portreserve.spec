Summary:	TCP port reservation utility
Name:		portreserve
Version:	0.0.5
Release:	6
License:	GPLv2
Group:		System/Base
Url:		http://cyberelk.net/tim/portreserve/
Source0:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2
Source1:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2.sig
Source2:	portreserve.init
Patch1:		portreserve-0.0.0-socket_dir.diff
Requires(pre,postun):	rpm-helper
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto

%description
The portreserve program aims to help services with well-known ports that lie in
the portmap range.  It prevents portmap from a real service's port by occupying
it itself, until the real service tells it to release the port (generally in
the init script).

%prep

%setup -q
%apply_patches

cp %{SOURCE2} portreserve-mandriva.init
autoreconf

%build
%configure2_5x \
	--sbindir=/sbin

%make

%install
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
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

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %attr(0711,root,root) %{_localstatedir}/lib/%{name}
%dir %attr(0711,root,root) %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) /sbin/*
%{_mandir}/man1/*

