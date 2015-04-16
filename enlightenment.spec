%define name	enlightenment
%define version	0.19.4
%define Name	Enlightenment
%define Summary	The Enlightenment window manager

Name:		%{name}
Version:	%{version}
Release:	0
Summary:	%{Summary}
License:	e19 and GPLv2+
Group:		Graphical desktop/Enlightenment
BuildRequires:  pulseaudio-devel
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  imlib2-devel
BuildRequires:  x11-data-bitmaps
BuildRequires:  pkgconfig(x11)
BuildRequires:  libxxf86vm-devel
BuildRequires:	gettext-devel
BuildRequires:	pam-devel
BuildRequires:	libalsa-devel
BuildRequires:	multiarch-utils
BuildRequires:  texinfo
BuildRequires:  imagemagick
BuildRequires:  xcb-util-devel
BuildRequires:  efl-devel
BuildRequires:  pkgconfig(sm)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-keysyms)
Requires:	acpitool
Requires:   desktop-common-data
Requires:	consolekit
Requires:	libmount1 >= 2.22.2


Source0:	https://download.enlightenment.org/enlightenment/rel/apps/enlightenment/enlightenment-0.9.4.tar.xz
Requires:	imagemagick >= 4.2.9
Provides:	e19 Enlightenment
URL:		http://www.enlightenment.org/

%description
Enlightenment is a window manager for the X Window System that is designed to
be powerful, extensible, configurable and pretty darned good looking! It is one
of the more graphically intense window managers.

Enlightenment goes beyond managing windows by providing a useful and appealing
graphical shell from which to work. It is open in design and instead of
dictating a policy, allows the user to define their own policy, down to every
last detail.

This package will install the Enlightenment window manager.

%prep

%setup -q -n  

%build
%configure2_5x  --disable-static \
	    --enable-sound
	    
./configure --prefix=%{_prefix}
cd ..

%make

%install
rm -rf %{buildroot}

rm -f %{buildroot}%{_datadir}/applications/*.desktop
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{Name}
Comment=%{Summary}
Exec=%{_bindir}/%{bin_name} 
Icon=%{name}
Terminal=false
Type=Applications
Categories=X-MandrivaLinux-System-Session-Windowmanagers;
EOF

install -d 644 %{buildroot}%{_sysconfdir}/X11/wmsession.d
cat >%{buildroot}%{_sysconfdir}/X11/wmsession.d/04enlightenment <<EOF
NAME=%{Name}
DESC=%{Summary}
EXEC=%{_bindir}/%{bin_name}
SCRIPT:
exec %{_bindir}/%{bin_name}
EOF

%files -f enlightenment.lang
%defattr(-,root,root)
%doc AUTHORS README COPYING doc/*
%_bindir/enlightenment
%_bindir/enlightenment_imc
%_bindir/enlightenment_remote
%_bindir/enlightenment_start
%_bindir/enlightenment_open
%_datadir/enlightenment
%exclude %_datadir/xsessions/*
%_libdir/enlightenment
%config %_sysconfdir/X11/wmsession.d/23E19
%config(noreplace) %_sysconfdir/enlightenment/sysactions.conf
%_sysconfdir/xdg/menus/enlightenment.menu
%_sysconfdir/xdg/menus/e-applications.menu


%files devel
%defattr(-,root,root)
%{_bindir}/enlightenment-config
%{_libdir}/pkgconfig/enlightenment.pc
%multiarch %{multiarch_bindir}/enlightenment-config
%_includedir/enlightenment
%{_libdir}/pkgconfig/everything.pc

%files efile
%defattr(-,root,root)
%_bindir/enlightenment_filemanager
%_datadir/applications/enlightenment_filemanager.desktop