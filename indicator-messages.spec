#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_with	static_libs	# static library
#
Summary:	Messaging Menu
Summary(pl.UTF-8):	Messaging Menu - menu narzędzi do komunikacji
Name:		indicator-messages
Version:	12.10.5
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://launchpad.net/indicator-messages
Source0:	https://launchpad.net/indicator-messages/12.10/%{version}/+download/%{name}-%{version}.tar.gz
# Source0-md5:	e7d6da8e9a88d9c45a8ff80af07eb958
URL:		https://launchpad.net/indicator-messages
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.33.10
BuildRequires:	gtk-doc >= 1.18
BuildRequires:	gtk+3-devel >= 3.5.18
BuildRequires:	gobject-introspection-devel >= 1.32.0
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libindicator-gtk3-devel >= 0.3.19
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gtk+3 >= 3.5.18
Requires:	libindicator-gtk3 >= 0.3.19
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Messaging Menu from Ubuntu.

%description -l pl.UTF-8
Messaging Menu - menu narzędzi do komunikacji pochodzące z Ubuntu.

%package libs
Summary:	Messaging Menu client library
Summary(pl.UTF-8):	Biblioteka kliencka Messaging Menu
Group:		Libraries
Requires:	glib2-devel >= 1:2.33.10

%description libs
Messaging Menu client library.

%description libs -l pl.UTF-8
Biblioteka kliencka Messaging Menu (menu narzędzi do komunikacji).

%package devel
Summary:	Header files for Messaging Menu library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Messaging Menu
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.33.10

%description devel
Header files for Messaging Menu library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Messaging Menu.

%package static
Summary:	Static Messaging Menu library
Summary(pl.UTF-8):	Statyczna biblioteka Messaging Menu
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Messaging Menu library.

%description static -l pl.UTF-8
Statyczna biblioteka Messaging Menu.

%package apidocs
Summary:	API documentation for Messaging Menu library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Messaging Menu
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Messaging Menu library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Messaging Menu.

%prep
%setup -q

%{__sed} -i -e 's/-Werror //' src/Makefile.am

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{?with_apidocs:--enable-gtk-doc} \
	--disable-silent-rules \
	%{?with_static_libs:--enable-static} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/indicators3/*/*.la
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libmessaging-menu.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS
%attr(755,root,root) %{_libdir}/indicators3/7/libmessaging.so
%attr(755,root,root) %{_libexecdir}/indicator-messages-service
%{_datadir}/dbus-1/services/indicator-messages.service
%{_datadir}/glib-2.0/schemas/com.canonical.indicator.messages.gschema.xml
%{_iconsdir}/hicolor/*x*/categories/applications-chat-panel.png
%{_iconsdir}/hicolor/*x*/categories/applications-email-panel.png
%{_iconsdir}/hicolor/*x*/categories/applications-microblogging-panel.png
%{_iconsdir}/hicolor/*x*/status/application-running.png
%{_iconsdir}/hicolor/*x*/status/indicator-messages.png
%{_iconsdir}/hicolor/*x*/status/indicator-messages-new.png
%{_iconsdir}/hicolor/scalable/categories/applications-chat-panel.svg
%{_iconsdir}/hicolor/scalable/categories/applications-email-panel.svg
%{_iconsdir}/hicolor/scalable/status/application-running.svg
%{_iconsdir}/hicolor/scalable/status/indicator-messages.svg
%{_iconsdir}/hicolor/scalable/status/indicator-messages-new.svg

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmessaging-menu.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmessaging-menu.so.0
%{_libdir}/girepository-1.0/MessagingMenu-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmessaging-menu.so
%{_includedir}/messaging-menu
%{_datadir}/gir-1.0/MessagingMenu-1.0.gir
%{_pkgconfigdir}/messaging-menu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmessaging-menu.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/messaging-menu
%endif
