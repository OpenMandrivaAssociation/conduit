%define svn	0
%define rel	2

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
Version:	0.3.17
Release:	%{release}
License:	GPLv2
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.conduit-project.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/conduit/0.3/%{distname}

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
%{_iconsdir}/hicolor/*/*/*.png
%{_iconsdir}/hicolor/*/*/*.svg
%{_datadir}/gnome/help/%{name}
%{_datadir}/omf/%{name}



%changelog
* Sat Nov 06 2010 Jani Välimaa <wally@mandriva.org> 0.3.17-2mdv2011.0
+ Revision: 594338
- rebuild for python 2.7

  + Frederik Himpe <fhimpe@mandriva.org>
    - Update to new version 0.3.17
    - Remove systemgdata patch: integrated upstream
    - Remove check patch: not needed anymore

* Wed Nov 11 2009 Pascal Terjan <pterjan@mandriva.org> 0.3.16-1mdv2010.1
+ Revision: 464612
- Update to 0.3.16
- Drop P1, these are now default settings
- Update P0 and P2

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.3.15-3mdv2010.0
+ Revision: 437100
- rebuild

* Fri Dec 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.15-2mdv2009.1
+ Revision: 319504
- rediff systemgdata.patch
- drop python-sqlite require, it actually can use python 2.5's own internal
  module
- rebuild with python 2.6

* Tue Oct 21 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.15-1mdv2009.1
+ Revision: 296329
- new release 0.3.15

* Tue Sep 02 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.14-1mdv2009.0
+ Revision: 279281
- add a couple of useful suggests (RSS and Evo support)
- add check.patch to disable a couple of buildtime checks that should really
  be runtime checks and break on x86-64
- drop conduit.real, it's not needed (and breaks stuff) when using webkit
- require python-webkit and python-gobject
- replace webkit.patch with conf.patch: now also use GIO instead of gnomevfs
- new release 0.3.14

* Sun Aug 10 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.13.1-1mdv2009.0
+ Revision: 270398
- new release 0.3.13.1

* Mon Aug 04 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.13-1mdv2009.0
+ Revision: 263564
- drop python-libgmail dependencies (conduit doesn't use it any more)
- new release 0.3.13

* Sun Jul 20 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.12-1mdv2009.0
+ Revision: 239241
- new release 0.3.12

* Thu Jun 12 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.11.2-1mdv2009.0
+ Revision: 218276
- drop %%post and %%postun stuff now handled by triggers
- new release 0.3.11.2

* Sat May 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.10-1mdv2009.0
+ Revision: 200536
- rediff systemgdata.patch
- drop systemlibgmail.patch (seems upstream isn't using libgmail at all any more)
- new release 0.3.10

* Tue Mar 18 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.9-1mdv2008.1
+ Revision: 188648
- buildrequires python-dbus
- prettify svn conditionals
- new release 0.3.9

* Thu Mar 06 2008 Gustavo De Nardin <gustavodn@mandriva.com> 0.3.8-3mdv2008.1
+ Revision: 180283
- fixed missing Requires on gnome-python-gconf

* Mon Mar 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.8-2mdv2008.1
+ Revision: 178143
- fix #38339 (dependencies on -devel packages) by removing pkgconfig file. Will re-introduce in a -devel package in future if it actually becomes needed.

* Fri Feb 29 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.3.8-1mdv2008.1
+ Revision: 176942
- new version

* Thu Feb 14 2008 Thierry Vignaud <tv@mandriva.org> 0.3.7-1mdv2008.1
+ Revision: 167835
- fix no-buildroot-tag

  + Adam Williamson <awilliamson@mandriva.org>
    - add systemgdata.patch and systemlibgmail.patch: use system copies of two python modules instead of internal copies
    - new release 0.3.7

* Mon Feb 04 2008 Colin Guthrie <cguthrie@mandriva.org> 0.3.6-1mdv2008.1
+ Revision: 162048
- new version 0.3.6

* Tue Jan 15 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.5-1mdv2008.1
+ Revision: 153296
- minor spec clean
- adjust the noarch adaptations for upstream changes
- drop mozpath.patch (merged upstream)
- new release 0.3.5

* Sun Jan 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.3.4-3mdv2008.1
+ Revision: 146105
- requires python-pyxml (#36442)

* Mon Oct 22 2007 Adam Williamson <awilliamson@mandriva.org> 0.3.4-2mdv2008.1
+ Revision: 101295
- add conduit-0.3.4-mozpath.patch , from upstream SVN, to (hackily) find the Mozilla location so the internal browser works

* Tue Oct 16 2007 Adam Williamson <awilliamson@mandriva.org> 0.3.4-1mdv2008.1
+ Revision: 99074
- correct buildrequires (no longer needs imagemagick, now needs gnome-doc-utils)
- adjust file list
- found a good fix for the borked autotools stuff
- drop various icon stuff in spec as upstream now does icons correctly
- drop a superfluous substitution
- new release 0.3.4
- use automake only...autoreconf is failing
- new release 0.3.4

* Thu Sep 06 2007 Adam Williamson <awilliamson@mandriva.org> 0.3.3-2mdv2008.0
+ Revision: 80571
- add some requires
- add a comment

* Wed Aug 22 2007 Adam Williamson <awilliamson@mandriva.org> 0.3.3-1mdv2008.0
+ Revision: 68804
- Import conduit

