Name:           vpnc
Version:        0.3.3
Release:        15%{?dist}

Summary:        IPSec VPN client compatible with Cisco equipment

Group:          Applications/Internet
License:        GPL
URL:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        vpnc-0.3.3.tar.gz
Source1:        generic-vpnc.conf
Source2:	vpnc.consolehelper
Source3:	vpnc-disconnect.consolehelper
Source4:	vpnc.pam
Source5:	vpnc-helper
Patch0:         vpnc-0.3.2-pie.patch
Patch1:		vpnc-0.3.3-sbin-path.patch
Patch2:		vpnc-0.3.3-ip-output.patch
Patch3:		vpnc-0.3.3-no-srcport.patch
Patch4:		vpnc-0.3.3-rekeying.patch
Patch5:		vpnc-0.3.3-cloexec.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgcrypt-devel > 1.1.90
Requires:       kernel >= 2.4

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%package consoleuser
Summary:	Allows console user to run the VPN client directly
Group:		Applications/Internet
Requires:	vpnc = %{version}-%{release}
Requires:	usermode

%description consoleuser
Allows the console user to run the IPSec VPN client directly without
switching to the root account.

%prep
%setup -q
%patch0 -p1 -b .pie
%patch1 -p1 -b .sbin-path
%patch2 -p1 -b .ip-output
%patch3 -p1 -b .no-srcport
%patch4 -p1 -b .rekeying
%patch5 -p1 -b .cloexec

%build
make PREFIX=/usr

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" PREFIX=/usr
chmod 0644 $RPM_BUILD_ROOT%{_mandir}/man8/vpnc.8
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/default.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/vpnc.conf
mkdir -p $RPM_BUILD_ROOT%{_var}/run/vpnc
touch $RPM_BUILD_ROOT%{_var}/run/vpnc/pid \
      $RPM_BUILD_ROOT%{_var}/run/vpnc/defaultroute \
      $RPM_BUILD_ROOT%{_var}/run/vpnc/resolv.conf-backup
install -Dp -m 0644 %{SOURCE2} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc
install -Dp -m 0644 %{SOURCE3} \
    $RPM_BUILD_ROOT%{_sysconfdir}/security/console.apps/vpnc-disconnect
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc
install -Dp -m 0644 %{SOURCE4} \
    $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/vpnc-disconnect
install -m 0755 %{SOURCE5} \
    $RPM_BUILD_ROOT%{_sbindir}/vpnc-helper
mkdir -p $RPM_BUILD_ROOT%{_bindir}
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc
ln -sf consolehelper $RPM_BUILD_ROOT%{_bindir}/vpnc-disconnect

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README COPYING

%dir %{_sysconfdir}/vpnc
%config(noreplace) %{_sysconfdir}/vpnc/vpnc-script
%config(noreplace) %{_sysconfdir}/vpnc/default.conf
%{_sbindir}/vpnc
%{_sbindir}/vpnc-disconnect
%{_mandir}/man8/*
%dir %{_var}/run/vpnc
%ghost %verify(not md5 size mtime) %{_var}/run/vpnc/pid
%ghost %verify(not md5 size mtime) %{_var}/run/vpnc/defaultroute
%ghost %verify(not md5 size mtime) %{_var}/run/vpnc/resolv.conf-backup

%files consoleuser
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/security/console.apps/vpnc*
%config(noreplace) %{_sysconfdir}/pam.d/vpnc*
%{_bindir}/vpnc*
%{_sbindir}/vpnc-helper

%changelog
* Wed Jan 17 2007 Tomas Mraz <tmraz@redhat.com> - 0.3.3-15
- do not overwrite personalized vpnc scripts (#195842)
- we must not allow commandline options to vpnc when run through consolehelper

* Wed Jan 17 2007 Tomas Mraz <tmraz@redhat.com> - 0.3.3-14
- add consoleuser subpackage (#160571)
- fix permissions on manpage (#222578)

* Tue Nov  7 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-13
- don't leak socket fds

* Tue Sep 12 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-12
- drop hoplimit from ip route output (#205923)
- let's try enabling -fstack-protector again, seems to work now

* Thu Sep  7 2006 Tomas Mraz <tmraz@redhat.com> - 0.3.3-11
- rebuilt for FC6

* Wed Jun  7 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-9
- drop the -fstack-protector not -f-stack-protector

* Tue May 30 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-8
- drop -fstack-protector from x86_64 build (workaround for #172145)
- make rekeying a little bit better

* Thu Mar  9 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-7
- add basic rekeying support (the patch includes NAT keepalive support
  by Brian Downing)
- dropped disconnect patch (solved differently)

* Wed Feb 15 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-6
- rebuild with new gcc

* Tue Jan 24 2006 Tomas Mraz <tmraz@redhat.com> 0.3.3-5
- send the disconnect packet properly (patch by Laurence Moindrot)

* Thu Sep 22 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-4
- improve compatibility with some Ciscos

* Wed Jun 15 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-3
- improve fix_ip_get_output in vpnc-script (#160364)

* Mon May 30 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-2
- package /var/run/vpnc and ghost files it can contain (#159015)
- add /sbin /usr/sbin to the path in vpnc-script (#159099)

* Mon May 16 2005 Tomas Mraz <tmraz@redhat.com> 0.3.3-1
- new upstream version

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 05 2005 Warren Togami <wtogami@redhat.com> 0.3.2-3
- Fix 64bit

* Thu Dec 23 2004 Warren Togami <wtogami@redhat.com> 0.3.2-2
- make PIE (davej)

* Mon Dec 20 2004 Warren Togami <wtogami@redhat.com> 0.3.2-1
- 0.3.2
