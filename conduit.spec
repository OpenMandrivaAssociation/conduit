%define name	conduit
%define version	0.3.4
%define svn	0
%if %svn
%define release	%mkrel 0.%svn.1
%else
%define release	%mkrel 1
%endif

Summary:	Synchronization solution for GNOME
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2
Group:		Communications
URL:		http://www.conduit-project.org/
%if %svn
Source0:	%{name}-%{svn}.tar.bz2
%else
Source0:	http://files.conduit-project.org/releases/%{name}-%{version}.tar.gz
%endif
BuildRequires:	python-pygoocanvas
BuildRequires:	pygtk2.0-devel
BuildRequires:	python-vobject
BuildRequires:	python
BuildRequires:	perl-XML-Parser
BuildRequires:	dbus-devel
BuildRequires:	intltool
BuildRequires:	ImageMagick
%if %svn
BuildRequires:	gnome-common
%endif
BuildArch:	noarch
Requires:	python-sqlite
Requires:	python-pygoocanvas
Requires:	python-vobject
Suggests:	avahi-python
Suggests:	python-twisted


%description
Conduit is a synchronization solution for GNOME which allows the user
to take their emails, files, bookmarks, and any other type of personal
information and synchronize that data with another computer, an online
service, or even another electronic device.

Conduit manages the synchronization and conversion of data into other
formats. For example, conduit allows you to synchronize your tomboy 
notes to a file on a remote computer, synchronize your emails to your
mobile phone, synchronize your bookmarks to delicious, gmail, or even
your own webserver, and more.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif

# install plugins to /usr/lib regardless of arch: they are arch-independent
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/dataproviders/Makefile.am
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/dataproviders/*/Makefile.am
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/dataproviders/*/*/Makefile.am

# install pkgconfig file to /usr/share/pkgconfig instead of libdir/pkgconfig
perl -pi -e 's,\$\(libdir\)/pkgconfig,\$\(datadir\)/pkgconfig,g' data/Makefile.am

# ...and correct the paths in it to match the changes we made above
perl -pi -e 's,\@libdir\@/conduit/dataproviders,\@exec_prefix\@/lib/conduit/dataproviders,g' data/conduit.pc.in

# correct start_conduit.py for the changes made above
perl -pi -e 's.LIBDIR, \$libdir.LIBDIR, \$exec_prefix/lib.g' configure.ac
perl -pi -e 's.PKGLIBDIR, \$libdir/\$PACKAGE.PKGLIBDIR, \$exec_prefix/lib/\$PACKAGE.g' configure.ac

# correct icon name
perl -pi -e 's,conduit-icon.png,%{name},g' data/conduit.desktop.in.in

%build
%if %svn
sh ./autogen.sh
%else
autoreconf
%endif
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 data/conduit-icon.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 data/conduit-icon.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 data/conduit-icon.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%find_lang %{name}

%post
%{update_icon_cache hicolor}
%{update_menus}

%postun
%{clean_icon_cache hicolor}
%{clean_menus}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS NEWS README TODO
%{_bindir}/start_conduit
%{py_puresitedir}/%{name}
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/dbus-1/services/org.gnome.Conduit.service
%{_datadir}/gnome/autostart/conduit-autostart.desktop
%{_datadir}/pixmaps/conduit-icon.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png

