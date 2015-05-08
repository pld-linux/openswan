# TODO:
# - openswan.init needs update for 2.6.x
# - warning: Installed (but unpackaged) file(s) found:
#   /usr/share/doc/openswan/index.html
#   /usr/share/doc/openswan/ipsec.conf-sample
#
# NOTE:
# - 32-bit tncfg and starter won't work on 64-bit kernels because of FUBAR
#   ioctls (only ifru_data pointer is supported in 32->64 conversion of
#   SIOCDEVPRIV ioctl, but openswan puts some static data in structure there)
#
Summary:	Open Source implementation of IPsec for the Linux operating system
Summary(pl.UTF-8):	Otwarta implementacja IPseca dla systemu operacyjnego Linux
Name:		openswan
Version:	2.6.43
Release:	0.1
License:	GPL v2+ (main parts), BSD (DES and radij code)
Group:		Networking/Daemons
Source0:	https://download.openswan.org/openswan/%{name}-%{version}.tar.gz
# Source0-md5:	87c4d7d4e537df57dc8e67c60e514724
Source1:	%{name}.init
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-bash.patch
URL:		http://www.openswan.org/
BuildRequires:	bison
BuildRequires:	docbook-dtd412-xml
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	perl-tools-pod
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	which
BuildRequires:	xmlto
Requires(post,preun):	/sbin/chkconfig
Requires:	bash
Requires:	rc-scripts
Provides:	freeswan
Obsoletes:	freeswan
Obsoletes:	ipsec-tools
Obsoletes:	strongswan
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openswan is an Open Source implementation of IPsec for the Linux 2.6.x
operating system. Is it a code fork of the FreeS/WAN project, started
by a few of the developers who were growing frustrated with the
politics surrounding the FreeS/WAN project.

%description -l pl.UTF-8
Openswan to otwarta implementacja IPseca dla systemu operacyjnego
Linux 2.6.x. Jest to odgałęzienie kodu z projektu FreeS/WAN,
rozpoczęte przez kilku programistów coraz bardziej sfrustrowanych
polityką otaczającą projekt FreeS/WAN.

%prep
%setup -q
%patch0 -p1
#%patch1 -p1

%{__sed} -i -e 's#/lib/ipsec#/%{_lib}/ipsec#g#' Makefile Makefile.inc

%build
USE_WEAKSTUFF=true \
USE_NOCRYPTO=true \
%{__make} -j1 programs \
	CC="%{__cc}" \
	USERCOMPILE="%{rpmcflags}" \
	IPSECVERSION=%{version}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/pluto}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	IPSECVERSION=%{version}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipsec
%{__sed} -i -e "s#/lib/ipsec#/%{_lib}/ipsec#g#" $RPM_BUILD_ROOT/etc/rc.d/init.d/ipsec

for l in `find $RPM_BUILD_ROOT%{_mandir}/man3 -type l` ; do
	d=`readlink $l`
	rm -f $l
	echo ".so $d" > $l
done

# API not exported - kill for now
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man3

install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}
cat >$RPM_BUILD_ROOT%{systemdtmpfilesdir}/openswan.conf <<EOF
d /var/run/pluto 0755 root root -
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipsec
%service ipsec restart "IPSEC daemon"

%preun
if [ "$1" = "0" ]; then
	%service ipsec stop
	/sbin/chkconfig --del ipsec
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS LICENSE README
%attr(755,root,root) %{_sbindir}/ipsec
%dir %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/ipsec/*
%attr(754,root,root) /etc/rc.d/init.d/ipsec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.conf
%dir %{_sysconfdir}/ipsec.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/hub-spoke.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/ipv6.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/l2tp-cert.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/l2tp-psk.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/linux-linux.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/mast-l2tp-psk.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/oe-exclude-dns.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/sysctl.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/xauth.conf
%dir %{_sysconfdir}/ipsec.d/aacerts
%dir %{_sysconfdir}/ipsec.d/cacerts
%dir %{_sysconfdir}/ipsec.d/certs
%dir %{_sysconfdir}/ipsec.d/crls
%dir %{_sysconfdir}/ipsec.d/ocspcerts
%dir %{_sysconfdir}/ipsec.d/policies
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/policies/block
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/policies/clear
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/policies/clear-or-private
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/policies/private
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/policies/private-or-clear
%dir %{_sysconfdir}/ipsec.d/private
%dir /var/run/pluto
%{systemdtmpfilesdir}/openswan.conf
%{_mandir}/man5/ipsec.conf.5*
%{_mandir}/man5/ipsec.secrets.5*
%{_mandir}/man5/ipsec_*.5*
%{_mandir}/man8/ipsec.8*
%{_mandir}/man8/ipsec_*.8*

# devel docs (but no devel libs)
#%{_mandir}/man3/ipsec_*.3*
