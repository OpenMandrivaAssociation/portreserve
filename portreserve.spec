Summary:	TCP port reservation utility
Name:		portreserve
Version:	0.0.5
Release:	%mkrel 2
License:	GPL
Group:		System/Base
URL:		http://cyberelk.net/tim/portreserve/
Source0:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2
Source1:	http://cyberelk.net/tim/data/portreserve/stable/%{name}-%{version}.tar.bz2.sig
Source2:	portreserve.init
Patch1:		portreserve-0.0.0-socket_dir.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	xmlto
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The portreserve program aims to help services with well-known ports that lie in
the portmap range.  It prevents portmap from a real service's port by occupying
it itself, until the real service tells it to release the port (generally in
the init script).

%prep

%setup -q
%patch1 -p1 -b .socket_dir

cp %{SOURCE2} portreserve-mandriva.init

%build
autoreconf

%configure2_5x \
    --sbindir=/sbin

%make

%install
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%dir %attr(0711,root,root) %{_localstatedir}/lib/%{name}
%dir %attr(0711,root,root) %{_sysconfdir}/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) /sbin/*
%{_mandir}/man1/*


%changelog
* Sun Jun 26 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-1mdv2011.0
+ Revision: 687262
- 0.0.5

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-5
+ Revision: 667807
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-4mdv2011.0
+ Revision: 607193
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.4-3mdv2010.1
+ Revision: 519055
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.0.4-2mdv2010.0
+ Revision: 426755
- rebuild

* Sat Mar 14 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.0.4-1mdv2009.1
+ Revision: 354878
- update to new version 0.0.4

* Wed Mar 11 2009 Gustavo De Nardin <gustavodn@mandriva.com> 0.0.3-3mdv2009.1
+ Revision: 353839
- portreserve does not require the network to be up
- should start before network is up (network-up script has no chkconfig
  headers)

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.0.3-2mdv2009.1
+ Revision: 351639
- rebuild

* Tue Jul 01 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.3-1mdv2009.0
+ Revision: 230562
- 0.0.3
- generate the man pages

* Mon Jun 30 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.2-1mdv2009.0
+ Revision: 230349
- 0.0.2
- drop P0, it's in there

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Mon Apr 21 2008 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-3mdv2009.0
+ Revision: 196218
- added lsb headers to the init script

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Aug 31 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-2mdv2008.0
+ Revision: 76943
- fix build
- rebuild

* Sun Aug 19 2007 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-1mdv2008.0
+ Revision: 66672
- Import portreserve



* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 0.0.0-1mdv2007.0
- initial Mandriva package
