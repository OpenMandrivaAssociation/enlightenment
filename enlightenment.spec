%define name	enlightenment
%define bin_name e16
%define theme_version 0.16.8
%define doc_version 0.16.8-0.02
%define version	0.16.8.10
%define Name	Enlightenment
%define Summary	The Enlightenment window manager
%define prefix	%{_prefix}
%define bindir	%{prefix}/bin
%define datadir	%{prefix}/share
%define mandir	%{prefix}/man

Name:		%{name}
Version:	%{version}
Release:	%mkrel 1
Summary:	%{Summary}
License:	e16 and GPLv2+
Group:		Graphical desktop/Enlightenment
BuildRequires:  esound-devel
BuildRequires:  freetype2-devel
BuildRequires:  imlib2-devel
BuildRequires:  x11-data-bitmaps
BuildRequires:  libx11-devel
BuildRequires:  libxxf86vm-devel
BuildRequires:  libsm-devel
BuildRequires:  libxft-devel
BuildRequires:  libxrandr-devel
BuildRequires:  texinfo
BuildRequires:  ImageMagick
Source0:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-docs-%{doc_version}.tar.bz2
Source2:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-theme-BlueSteel-%{theme_version}.tar.bz2
Source3:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-theme-BrushedMetal-Tigert-%{theme_version}.tar.bz2
Source4:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-theme-Ganymede-%{theme_version}.tar.bz2
Source5:	http://prdownloads.sourceforge.net/enlightenment/%{bin_name}-theme-ShinyMetal-%{theme_version}.tar.bz2
Source7:	%{name}.png
# this overrides some themes' *.cfg files with other slightly modified to
# use fontsets, and so be able to display text in any language
# the files inside that tarball may need to be modified or new added if the
# themes' files from the Enlightenment sources change -- pablo
Source8:	%{name}-0.16.5-themes-i18n.tar.bz2  
Requires:	ImageMagick >= 4.2.9
Provides:	e16 Enlightenment
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

%setup -q -n %bin_name-%version -a 1 -a 2 -a 3 -a 4 -a 5

%build
export CFLAGS="$RPM_OPT_FLAGS"
export CXXFLAGS="$RPM_OPT_FLAGS"
%configure  --enable-fsstd \
	    --enable-sound \
	    --enable-upgrade \
	    --enable-zoom 

for i in BlueSteel BrushedMetal-Tigert Ganymede ShinyMetal; do
cd %{bin_name}-theme-$i-%{theme_version};
./configure --prefix=%{prefix}
cd ..
done;

cd %{bin_name}-docs-%{doc_version}
./configure --prefix=%{prefix}
cd ..
%make

%install
rm -rf $RPM_BUILD_ROOT

##build will fail if not done in this manner--CAE##
%makeinstall_std

# Install icons
install -d 644 $RPM_BUILD_ROOT%{_miconsdir}
install -d 644 $RPM_BUILD_ROOT%{_iconsdir}
install -d 644 $RPM_BUILD_ROOT%{_liconsdir}
install -m 644 %SOURCE7 $RPM_BUILD_ROOT%{_miconsdir}
convert %SOURCE7 -geometry 32x32 $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert %SOURCE7 -geometry 48x48 $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{Name}
Comment=%{Summary}
Exec=${_bindir}/${bin_name} 
Icon=%{name}
Terminal=false
Type=Applications
Categories=X-MandrivaLinux-System-Session-Windowmanagers;
EOF

install -d 644 $RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d
cat >$RPM_BUILD_ROOT%{_sysconfdir}/X11/wmsession.d/04enlightenment <<EOF
NAME=%{Name}
DESC=%{Summary}
EXEC=%{bindir}/%{bin_name}
SCRIPT:
exec %{bindir}/%{bin_name}
EOF


for i in BlueSteel BrushedMetal-Tigert Ganymede ShinyMetal; do
cd %{bin_name}-theme-$i-%{theme_version};
%makeinstall_std
cd ..
done;

# overwrite some themes' files with i18n'ed ones
bzcat %SOURCE8 | tar xvf - -C $RPM_BUILD_ROOT%{datadir}/%{bin_name}


cd %{bin_name}-docs-%{doc_version}
%makeinstall_std
cd ..

#rm some empty theme files
rm -fr $RPM_BUILD_ROOT/%{datadir}/%{bin_name}/themes/BlueSteel/sound/sound.cfg
rm -fr $RPM_BUILD_ROOT/%{datadir}/%{bin_name}/themes/BlueSteel/slideouts/slideouts.cfg
rm -fr $RPM_BUILD_ROOT/%{datadir}/%{bin_name}/themes/BrushedMetal-Tigert/slideouts/slideouts.cfg
rm -fr $RPM_BUILD_ROOT/%{datadir}/%{bin_name}/themes/BrushedMetal-Tigert/buttons/buttons.cfg
rm -rf $RPM_BUILD_ROOT/%{datadir}/%{bin_name}/themes/BlueSteel/buttons/buttons.cfg
rm -rf `find $RPM_BUILD_ROOT -name .xvpics`

%find_lang %{name}
rm -f $RPM_BUILD_ROOT/usr/etc/X11/dm/Sessions/enlightenment.desktop

%post
%update_menus
%make_session

%postun
%clean_menus
%make_session

%clean
rm -fr $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root,755)
%doc AUTHORS COPYING ChangeLog README COMPLIANCE
%doc sample-scripts
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/*
%{bindir}/*
%{_libdir}/*
%{_datadir}/applications/*
%{datadir}/%{bin_name}
%{datadir}/xsessions/*.desktop
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/locale/*/LC_MESSAGES/%{bin_name}.mo

