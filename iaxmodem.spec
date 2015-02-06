%define version 1.2.0

Summary: Software modem for interfacing Asterisk and Hylafax via IAX2
Name: iaxmodem
Version: %{version}
Release: 1
License: GPL
Group: System/Servers
Url: https://sourceforge.net/projects/iaxmodem
Source0: http://prdownloads.sourceforge.net/iaxmodem/iaxmodem-%{version}.tar.gz
Source1: iaxmodem.logrotate
Source2: ttyIAX0
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}
#Requires: asterisk >= 1.4.5
#Requires: hylafax
BuildRequires: libtiff-devel

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

%description
IAXmodem is a software modem written in C that uses an IAX channel
(commonly provided by an Asterisk PBX system) instead of a traditional
phone line and uses a DSP library instead of DSP hardware chipsets.

To accomplish this, then, IAXmodem interfaces an IAX library known as
libiax2 with a DSP library known as spandsp, and then IAXmodem interfaces
the DSP library with a tty device node for interfacing with modem
applications.

%prep
%setup -q

%build
pushd lib/libiax2
autoreconf --force
%configure --disable-shared
%make
popd

pushd lib/spandsp
autoreconf --force
%configure --disable-shared
%make
popd

# set the variables
MODEMVER=iaxmodem-%{version}
DSPVER="spandsp-0.0.5"
IAXVER="libiax2-0.2.3"

# build a static version of iaxmodem
gcc $RPM_OPT_FLAGS -Wall -g -DMODEMVER=\"$MODEMVER\" -DDSPVER=\"$DSPVER\" -DIAXVER=\"$IAXVER\" -DSTATICLIBS -D_GNU_SOURCE -std=c99 -Ilib/libiax2/src -Ilib/spandsp/src -c -o iaxmodem.o iaxmodem.c
gcc -lm -lutil -ltiff -o iaxmodem iaxmodem.o lib/spandsp/src/.libs/libspandsp.a lib/libiax2/src/.libs/libiax.a

%install
mkdir -p %{buildroot}/etc/logrotate.d %{buildroot}/etc/iaxmodem %{buildroot}%{_sbindir} %{buildroot}%{_mandir}/man1
%{__install} -m 644 %{SOURCE1} %{buildroot}/etc/logrotate.d/iaxmodem
%{__install} -m 644 %{SOURCE2} %{buildroot}/etc/iaxmodem/
%{__install} -m 755 iaxmodem %{buildroot}%{_sbindir}/iaxmodem
%{__install} -m 644 iaxmodem.1 %{buildroot}%{_mandir}/man1/iaxmodem.1

%post
echo ""
echo "Recommend add the following line in the /etc/inittab file:"
echo "---------------------------------------------"
echo "iax1:2345:respawn:/usr/sbin/iaxmodem ttyIAX0"
echo "mo1:2345:respawn:/usr/sbin/faxgetty ttyIAX0"
echo "---------------------------------------------"
echo "Then run : '/sbin/init q' to reload the inittab settings"

%clean
[ "%{buildroot}" != '/' ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES FAQ README TODO
%attr(750,asterisk,asterisk) %{_sbindir}/*
%attr(0644,root,root) %{_mandir}/man1/*
%config /etc/logrotate.d/*
%config(noreplace) /etc/iaxmodem


%changelog
* Thu Mar 24 2011 zamir <zamir@mandriva.org> 1.2.0-0mdv2011.0
+ Revision: 648294
- fix spec
- first build
- create iaxmodem

