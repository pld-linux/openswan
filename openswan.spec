
# TODO: - work on kernel 2.6, need Requires: kernel >= 2.6.0
#       - /etc/rc.d/init.d/ipsec need work

Summary:	Open Source implementation of IPsec for the Linux operating system
Name:		openswan
Version:	2.1.2
Release:	0.1
Epoch:		0
License:	GPL/BSD
Group:		Networking/Daemons
Source0:	http://www.openswan.org/code/%{name}-%{version}.tar.gz
# Source0-md5:	3504c480097136b5df5988b313315811
Patch0:		%{name}-prefix.patch
URL:		http://www.openswan.org/
BuildRequires:	make
BuildRequires:	gmp-devel
BuildRequires:	man2html
Requires:	kernel-headers
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Openswan is an Open Source implementation of IPsec for the Linux
operating system. Is it a code fork of the FreeS/WAN project, started
by a few of the developers who were growing frustrated with the
politics surrounding the FreeS/WAN project.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
make programs 

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

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

%postun

%files
%defattr(644,root,root,755)
%doc BUGS CHANGES CREDITS LICENSE README
%attr(755,root,root) %{_sbindir}/*
%dir %{_libdir}/ipsec
%attr(755,root,root) %{_libdir}/ipsec/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/ipsec
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipsec.conf
%dir %{_sysconfdir}/ipsec.d
%dir %{_sysconfdir}/ipsec.d/policies
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipsec.d/policies/*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/ipsec.d/*
%dir %{_docdir}/freeswan
%{_docdir}/freeswan
%{_mandir}/man3
%{_mandir}/man5
%{_mandir}/man8
