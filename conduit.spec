%define svn	0
%define rel	3

%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dirname		%name-%version
%endif

Summary:	Synchronization solution for GNOME
Name:		conduit
Version:	0.3.15
Release:	%{release}
License:	GPLv2
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.conduit-project.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/conduit/0.3/%{distname}

# ATTENTION: be careful with these patches when doing a version bump
# Upstream includes its own copies of these Python modules and uses
# very recent versions: if our package is older than the version
# upstream includes, and you cannot bump our package, it's probably
# best to disable the appropriate patch rather than using our older
# copy of the module - AdamW 2008/02

# Use system python-gdata
Patch0:		conduit-0.3.15-systemgdata.patch
# Use webkit, not gtkmozembed and GIO, not gnomevfs - recommended by
# upstream - AdamW 2008/09
Patch1:		conduit-0.3.14-conf.patch
# Disable a couple of checks which don't seem to work on x86-64 as
# written and really shouldn't be run at build time anyway - AdamW
# 2008/09
Patch2:		conduit-0.3.14-check.patch
BuildRequires:	python-pygoocanvas
BuildRequires:	pygtk2.0-devel
BuildRequires:	python-vobject
BuildRequires:	python-dbus
BuildRequires:	python
BuildRequires:	perl-XML-Parser
BuildRequires:	dbus-devel
BuildRequires:	intltool
BuildRequires:	gnome-doc-utils
%if %svn
BuildRequires:	gnome-common
%endif
BuildArch:	noarch
Requires:	python-pygoocanvas
Requires:	python-vobject
Requires:	python-pyxml
Requires:	python-webkitgtk
Requires:	gnome-python-desktop
Requires:	gnome-python-gconf
Requires:	python-gdata
Requires:	python-gobject
Suggests:	avahi-python
Suggests:	python-twisted
Suggests:	python-gpod
Suggests:	python-feedparser
Suggests:	gnome-python-evolution
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
%setup -q -n %{dirname}
%patch0 -p1 -b .gdata
%patch1 -p1 -b .conf
%patch2 -p1 -b .check

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
# The whole .real bit is only needed for Firefox, and we use Webkit...
# - AdamW 2008/09
mv -f %{buildroot}%{_bindir}/%{name}.real %{buildroot}%{_bindir}/%{name}

# Causes -devel dependencies if present, and isn't really useful as
# there's nothing that builds against Conduit. Will re-introduce in a
# -devel package if it becomes useful in future. - AdamW 2008/03
rm -f %{buildroot}%{_datadir}/pkgconfig/%{name}.pc

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS NEWS README TODO
%{_bindir}/%{name}
%{_bindir}/%{name}-client
%{py_puresitedir}/%{name}
%{_prefix}/lib/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/org.%{name}.service
%{_datadir}/gnome/autostart/%{name}-autostart.desktop
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_datadir}/gnome/help/%{name}
%{_datadir}/omf/%{name}

