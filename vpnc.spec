Name:           vpnc
Version:        0.3.3
Release:        1

Summary:        IPSec VPN client compatible with Cisco equipment

Group:          Applications/Internet
License:        GPL
URL:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        vpnc-0.3.3.tar.gz
Source1:        generic-vpnc.conf
Patch0:         vpnc-0.3.2-pie.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgcrypt-devel > 1.1.90
Requires:       kernel >= 2.4

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%prep
%setup -q
%patch0 -p1

%build
make PREFIX=/usr

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" PREFIX=/usr
install -m 0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/default.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/vpnc/vpnc.conf


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README

%config(noreplace) %{_sysconfdir}/vpnc/default.conf
%{_sbindir}/*
%{_sysconfdir}/vpnc
%{_mandir}/man8/*

%changelog
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
