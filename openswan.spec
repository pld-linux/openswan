# NOTE:
# 32-bit tncfg and starter won't work on 64-bit kernels because of FUBAR ioctls
# (only ifru_data pointer is supported in 32->64 conversion of SIOCDEVPRIV ioctl,
#  but openswan puts some static data in structure there)
Summary:	Open Source implementation of IPsec for the Linux operating system
Summary(pl.UTF-8):	Otwarta implementacja IPseca dla systemu operacyjnego Linux
Name:		openswan
Version:	2.4.11
Release:	1
Epoch:		0
License:	GPL/BSD
Group:		Networking/Daemons
Source0:	http://www.openswan.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	6cac660e0beb6db101bac5b86c743aab
Source1:	%{name}.init
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-bash.patch
Patch2:		%{name}-enable_des.patch
URL:		http://www.openswan.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gmp-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
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
%patch1 -p1
%patch2 -p1

%{__sed} -i -e "s#/lib/ipsec#/%{_lib}/ipsec#g#" Makefile
%{__sed} -i -e "s#/lib/freeswan$#/%{_lib}/freeswan#g#" Makefile
%{__sed} -i -e "s#/lib/ipsec#/%{_lib}/ipsec#g#" Makefile.inc

%build
%{__make} programs \
	CC="%{__cc}" \
	USERCOMPILE="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/pluto}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipsec
%{__sed} -i -e "s#/lib/ipsec#/%{_lib}/ipsec#g#" $RPM_BUILD_ROOT/etc/rc.d/init.d/ipsec

for l in `find $RPM_BUILD_ROOT%{_mandir}/man3 -type l` ; do
	d=`readlink $l`
	rm -f $l
	echo ".so $d" > $l
done

# just man pages converted to HTML
rm -rf $RPM_BUILD_ROOT%{_docdir}/openswan/*.[358].html

# API not exported - kill for now
rm -rf $RPM_BUILD_ROOT%{_mandir}/man3

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
%doc BUGS CHANGES CREDITS LICENSE README doc
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/ipsec/*
%attr(754,root,root) /etc/rc.d/init.d/ipsec
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.conf
%dir %{_sysconfdir}/ipsec.d
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ipsec.d/*
%dir /var/run/pluto
%{_mandir}/man5/*
%{_mandir}/man8/*

# devel docs (but no devel libs)
#%{_mandir}/man3/*
