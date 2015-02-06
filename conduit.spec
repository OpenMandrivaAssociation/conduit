Summary:	Synchronization solution for GNOME
Name:		conduit
Version:	0.3.17
Release:	4
License:	GPLv2+
Group:		Communications
Url:		http://www.conduit-project.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/conduit/0.3/%{name}-%{version}.tar.bz2
BuildRequires:	intltool
BuildRequires:	python-dbus
BuildRequires:	python-pygoocanvas
BuildRequires:	python-vobject
BuildRequires:	perl-XML-Parser
BuildRequires:	rarian
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(pygtk-2.0)
Requires:	gnome-python-desktop
Requires:	gnome-python-gconf
Requires:	python-gdata
Requires:	python-gobject
Requires:	python-pygoocanvas
Requires:	python-pyxml
Requires:	python-vobject
Requires:	python-webkitgtk
Suggests:	avahi-python
Suggests:	gnome-python-evolution
Suggests:	python-gpod
Suggests:	python-feedparser
Suggests:	python-twisted
Suggests:	ffmpeg
Suggests:	mencoder
BuildArch:	noarch

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

%files -f %{name}.lang
%doc AUTHORS NEWS README TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-client
%{py_puresitedir}/%{name}
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/org.%{name}.service
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_datadir}/gnome/help/%{name}
%{_datadir}/omf/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q

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
# redefinition of ACLOCAL is needed because conduit ships its own
# Awsum Hax0reD .m4 files and a normal aclocal uses the standard ones
# and breaks build. - AdamW 2007/10
ACLOCAL="aclocal -I ./m4" autoreconf
%configure2_5x
%make

%install
%makeinstall_std
# The whole .real bit is only needed for Firefox, and we use Webkit...
# - AdamW 2008/09
mv -f %{buildroot}%{_bindir}/%{name}.real %{buildroot}%{_bindir}/%{name}

# Causes -devel dependencies if present, and isn't really useful as
# there's nothing that builds against Conduit. Will re-introduce in a
# -devel package if it becomes useful in future. - AdamW 2008/03
rm -f %{buildroot}%{_datadir}/pkgconfig/%{name}.pc

%find_lang %{name}

