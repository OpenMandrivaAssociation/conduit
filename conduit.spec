%define name	conduit
%define version	0.3.5
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
Source0:	http://files.conduit-project.org/releases/%{name}-%{version}.tar.bz2
%endif
BuildRequires:	python-pygoocanvas
BuildRequires:	pygtk2.0-devel
BuildRequires:	python-vobject
BuildRequires:	python
BuildRequires:	perl-XML-Parser
BuildRequires:	dbus-devel
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils
%if %svn
BuildRequires:	gnome-common
%endif
BuildArch:	noarch
Requires:	python-sqlite
Requires:	python-pygoocanvas
Requires:	python-vobject
Requires:	python-pyxml
Requires:	gnome-python-gtkmozembed
Requires:	gnome-python-desktop
Suggests:	avahi-python
Suggests:	python-twisted
Suggests:	python-libgmail
Suggests:	python-gpod
Suggests:	ffmpeg
Suggests:	mencoder

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
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/modules/Makefile.am
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/modules/*/Makefile.am
perl -pi -e 's,\$\(libdir\)/conduit,\$\(exec_prefix\)/lib/conduit,g' conduit/modules/*/*/Makefile.am

# install pkgconfig file to /usr/share/pkgconfig instead of libdir/pkgconfig
perl -pi -e 's,\$\(libdir\)/pkgconfig,\$\(datadir\)/pkgconfig,g' data/Makefile.am

# ...and correct the paths in it to match the changes we made above
perl -pi -e 's.MODULEDIR, \$libdir.MODULEDIR, \$exec_prefix/lib.g' configure.ac

# correct start_conduit.py for the changes made above
perl -pi -e 's.LIBDIR, \$libdir.LIBDIR, \$exec_prefix/lib.g' configure.ac

%build
%if %svn
sh ./autogen.sh
%else
# redefinition of ACLOCAL is needed because conduit ships its own
# Awsum Hax0reD .m4 files and a normal aclocal uses the standard ones
# and breaks build. - AdamW 2007/10
ACLOCAL="aclocal -I ./m4" autoreconf
%endif
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

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
%{_bindir}/%{name}
%{_bindir}/%{name}-client
%{_bindir}/%{name}.real
%{py_puresitedir}/%{name}
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/dbus-1/services/org.%{name}.service
%{_datadir}/gnome/autostart/%{name}-autostart.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_datadir}/gnome/help/%{name}
%{_datadir}/omf/%{name}

