Name:           vpnc
Version:        0.3.2
Release:        3
Summary:        IPSec VPN client compatible with Cisco equipment

Group:          Applications/Internet
License:        GPL
URL:            http://www.unix-ag.uni-kl.de/~massar/vpnc/
Source0:        vpnc-0.3.2.tar.gz
Source1:        generic-vpnc.conf
Patch0:         vpnc-0.3.2-pie.patch
Patch1:         vpnc-0.3.2-64bit.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libgcrypt-devel > 0:1.1.90
Requires:       kernel >= 0:2.4

%description
A VPN client compatible with Cisco's EasyVPN equipment.

Supports IPSec (ESP) with Mode Configuration and Xauth.  Supports only
shared-secret IPSec authentication, 3DES, MD5, and IP tunneling.

%prep
%setup -q 
%patch0 -p1
%patch1 -p1

%build
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{sbin,etc}

install -m 755 vpnc $RPM_BUILD_ROOT/sbin
install -m 600 %{SOURCE1} $RPM_BUILD_ROOT/etc/vpnc.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%dev(c, 10, 200) /dev/tun
%config(noreplace) /etc/vpnc.conf
/sbin/*

%changelog
* Wed Jan 05 2005 Warren Togami <wtogami@redhat.com> 0.3.2-3
- Fix 64bit

* Thu Dec 23 2004 Warren Togami <wtogami@redhat.com> 0.3.2-2
- make PIE (davej)

* Mon Dec 20 2004 Warren Togami <wtogami@redhat.com> 0.3.2-1
- 0.3.2
