
# TODO: - work on kernel 2.6, need Requires: kernel >= 2.6.0
#       - /etc/rc.d/init.d/ipsec need work

Summary:	Open Source implementation of IPsec for the Linux operating system
Summary(pl):	Otwarta implementacja IPseca dla systemu operacyjnego Linux
Name:		openswan
Version:	2.2.0
Release:	0.1
Epoch:		0
License:	GPL/BSD
Group:		Networking/Daemons
Source0:	http://www.openswan.org/code/%{name}-%{version}.tar.gz
# Source0-md5:	f5f83204652627cf51d2567c53df5520
Source1:	%{name}.init
Patch0:		%{name}-prefix.patch
URL:		http://www.openswan.org/
BuildRequires:	gmp-devel
BuildRequires:	htmldoc
BuildRequires:	man2html
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openswan is an Open Source implementation of IPsec for the Linux 2.6.x
operating system. Is it a code fork of the FreeS/WAN project, started
by a few of the developers who were growing frustrated with the
politics surrounding the FreeS/WAN project.

%description -l pl
Openswan to otwarta implementacja IPseca dla systemu operacyjnego
Linux 2.6.x. Jest to odga³êzienie kodu z projektu FreeS/WAN,
rozpoczête przez kilku programistów coraz bardziej sfrustrowanych
polityk± otaczaj±c± projekt FreeS/WAN.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
%{__make} programs

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ipsec

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ipsec
if [ -f /var/lock/subsys/ipsec ]; then
        /etc/rc.d/init.d/ipsec restart >&2
else
        echo "Run \"/etc/rc.d/init.d/ipsec start\" to start IPSEC daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/ipsec ]; then
    		/etc/rc.d/init.d/ipsec stop>&2
	fi
        /sbin/chkconfig --del ipsec
fi

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS LICENSE README
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/ipsec/*
%attr(754,root,root) /etc/rc.d/init.d/ipsec
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipsec.conf
%dir %{_sysconfdir}/ipsec.d
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipsec.d/*
%{_datadir}/doc/openswan/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
