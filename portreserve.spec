Summary:	TCP port reservation utility
Name:		portreserve
Version:	0.0.5
Release:	15
License:	GPLv2
Group:		System/Base
Url:		https://cyberelk.net/tim/portreserve/
Source0:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2
Source1:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2.sig
Source2:	portreserve.service
Patch0:		portreserve-pid-file.patch
Patch1:		portreserve-0.0.0-socket_dir.diff
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto

%description
The portreserve program aims to help services with well-known ports that lie in
the portmap range.  It prevents portmap from a real service's port by occupying
it itself, until the real service tells it to release the port (generally in
the init script).

%prep
%autosetup -p1
cp %{SOURCE2} portreserve-mandriva.init
autoreconf

%build
%configure \
	--sbindir=/sbin

%make_build

%install
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_mandir}/man1

%make_install
install -m644 %{SOURCE2} -D %{buildroot}%{_unitdir}/%{name}.service
install -m0644 doc/portrelease.1 %{buildroot}%{_mandir}/man1/
install -m0644 doc/portreserve.1 %{buildroot}%{_mandir}/man1/

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %attr(0711,root,root) %{_localstatedir}/lib/%{name}
%dir %attr(0711,root,root) %{_sysconfdir}/%{name}
%{_unitdir}/%{name}.service
%attr(0755,root,root) /sbin/*
%{_mandir}/man1/*
