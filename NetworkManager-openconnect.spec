%define nm_version          1:0.7.0-0.11.svn4229
%define dbus_version        1.1
%define gtk2_version        2.10.0
%define openconnect_version 0.99

%define svn_snapshot        svn9

Summary:   NetworkManager VPN integration for openconnect
Name:      NetworkManager-openconnect
Version:   0.7.0
Release:   3.%{svn_snapshot}%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       http://www.gnome.org/projects/NetworkManager/
# Created from the git mirror of GNOME SVN:
# git-clone git://git.infradead.org/network-manager-openconnect.git
# cd network-manager-openconnect
# git-archive --format=tar --prefix=NetworkManager-openconnect-0.7.0/ daf365e \
#                 | gzip -9 > NetworkManager-0.7.0.svn9.tar.gz
Source:    %{name}-%{version}.%{svn_snapshot}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel             >= %{gtk2_version}
BuildRequires: dbus-devel             >= %{dbus_version}
BuildRequires: NetworkManager-devel   >= %{nm_version}
BuildRequires: NetworkManager-glib-devel >= %{nm_version}
BuildRequires: GConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libglade2-devel
BuildRequires: intltool gettext
BuildRequires: gnome-common
BuildRequires: autoconf automake libtool

Requires: NetworkManager   >= %{nm_version}
Requires: openconnect      >= %{openconnect_version}

Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(pre): %{_sbindir}/useradd
Requires(pre): %{_sbindir}/groupadd


%description
This package contains software for integrating the openconnect VPN software
with NetworkManager and the GNOME desktop

%prep
%setup -q

%build
sh autogen.sh
%configure --enable-more-warnings=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la
rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.a

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%{_sbindir}/groupadd -r nm-openconnect &>/dev/null || :
%{_sbindir}/useradd  -r -s /sbin/nologin -d / -M \
                     -c 'NetworkManager user for OpenConnect' \
                     -g nm-openconnect nm-openconnect &>/dev/null || :

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
      %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS ChangeLog COPYING
%{_libdir}/NetworkManager/lib*.so*
%{_sysconfdir}/dbus-1/system.d/nm-openconnect-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openconnect-service.name
%{_libexecdir}/nm-openconnect-service
%{_libexecdir}/nm-openconnect-service-openconnect-helper
%dir %{_datadir}/gnome-vpn-properties/openconnect
%{_datadir}/gnome-vpn-properties/openconnect/nm-openconnect-dialog.glade

%changelog
* Sun Dec 21 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-3.svn9
- Update from GNOME SVN (translations, review feedback merged)

* Wed Dec 17 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-2.svn3
- Review feedback

* Tue Dec 16 2008 David Woodhouse <David.Woodhouse@intel.com> 0.7.0-1.svn3
- Change version numbering to match NetworkManager