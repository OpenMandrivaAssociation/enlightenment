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
BuildRequires:  pkgconfig(sm)
BuildRequires:	pkgconfig(sndfile)
BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  texinfo
BuildRequires:  imagemagick
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

##build will fail if not done in this manner--CAE##
%makeinstall_std

# Install icons
install -d 644 %{buildroot}%{_miconsdir}
install -d 644 %{buildroot}%{_iconsdir}
install -d 644 %{buildroot}%{_liconsdir}
install -m 644 %SOURCE7 %{buildroot}%{_miconsdir}
convert %SOURCE7 -geometry 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert %SOURCE7 -geometry 48x48 %{buildroot}%{_liconsdir}/%{name}.png

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

#installed in right directory by %doc macro in file list
rm -f %{buildroot}%{_docdir}/e16/README.html %{buildroot}%{_docdir}/e19/e19-docs.html


cd %{bin_name}-docs-%{doc_version}
%makeinstall_std
cd ..

%find_lang %{bin_name}
rm -f %{buildroot}/usr/etc/X11/dm/Sessions/enlightenment.desktop

%files -f %{bin_name}.lang
%defattr(-, root, root,755)
%doc AUTHORS COPYING ChangeLog COMPLIANCE
%doc sample-scripts
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{_bindir}/*
%{_libdir}/e19
%{_datadir}/applications/*
%{_datadir}/gnome-session/sessions/e19-gnome.session
%{_datadir}/%{bin_name}
%{_datadir}/doc/*
%{_datadir}/xsessions/*.desktop
%{_mandir}/man1/*
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
