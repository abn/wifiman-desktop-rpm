%global _hardened_build 1
%define _build_id_links none
%define debug_package %{nil}

Name:     wifiman-desktop
Version:  0.3.0
Release:  0
Summary:  Discover devices and access Teleport VPNs
License:  MIT
Vendor:   Ubiquiti Inc. <monitoring@wifiman.com>
URL:      https://wifiman.com/

%ifarch x86_64
Source0:  https://desktop.wifiman.com/wifiman-desktop-%{version}-linux-amd64.deb
%endif

%ifarch aarch64
Source0:  https://desktop.wifiman.com/wifiman-desktop-%{version}-linux-arm64.deb
%endif

Patch0:   0001-fix-desktop-exec.patch
Patch1:   0002-fix-service-exec.patch

BuildRequires: binutils
BuildRequires: desktop-file-utils
BuildRequires: gzip
BuildRequires: systemd-units
BuildRequires: tar
BuildRequires: xz

Requires: gtk3
Requires: libsecret
Requires: libuuid
Requires: at-spi2-core
Requires: xdg-utils
Requires: libXtst
Requires: %{_libdir}/libXss.so.1
Requires: nss
Requires: libnotify
Requires: wireguard-tools
Requires: systemd

Recommends: libappindicator-gtk3

%description
WiFiman is here to save your home or office network from sluggish surfing, endless buffering, and congested data channels.
With this free-to-use (and ad-free) app you can:

- Detect and connect to all available Wi-Fi networks devices instantly.
- Scan network subnet for details on available devices, using Bonjour, SNMP, NetBIOS, and Ubiquiti discovery protocols.
- Conduct download/upload speed tests, store results, compare network performance, and share your insights with others.
- Relocate your access points (APs) to nearby data channels to instantly increase signal strength and reduce traffic volume.
- Connect remotely to your UniFi network via Teleport VPN.

%prep
%setup -cT
ar x %{SOURCE0}
tar xf data.tar.xz
%patch -P 0 -p0
%patch -P 1 -p0

%build

%install
install -D opt/WiFiman\ Desktop/service/wifiman-desktop.service %{buildroot}/%{_unitdir}/%{name}.service

rm -f opt/WiFiman\ Desktop/service/wifiman-desktop.service
rm -rf opt/WiFiman\ Desktop/scripts

install -d %{buildroot}/opt
cp -R opt/WiFiman\ Desktop %{buildroot}/opt/wifiman-desktop

rm -rf usr/share/doc
cp -R usr/share %{buildroot}/%{_datarootdir}

# this should really be using user runtime dir, but this seems to be hardcoded in the electron app
install -d -m 777 %{buildroot}/opt/wifiman-desktop/tmp

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
%systemd_post %{name}.service
%{__ln_s} -f /opt/wifiman-desktop/service/.env %{_sysconfdir}/%{name}
%{__ln_s} -f /opt/wifiman-desktop/wifiman-desktop %{_bindir}/wifiman-desktop
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database /usr/share/mime &>/dev/null
update-desktop-database /usr/share/applications &>/dev/null

%preun
pkill -SIGTERM -f /opt/wifiman-desktop/wifiman-desktop || :
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

case "$1" in
  0) # last one out put out the lights
    rm -f %{_sysconfdir}/%{name}
    rm -f %{_bindir}/wifiman-desktop
    rm -rf /opt/wifiman-desktop
  ;;
esac

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root,-)
%dir %attr(777, root, root) /opt/wifiman-desktop/tmp
%attr(644, root, root) /opt/wifiman-desktop/assets/devices/*.png
%attr(644, root, root) /opt/wifiman-desktop/assets/uidb.json
%attr(644, root, root) /opt/wifiman-desktop/locales/*.pak
%attr(644, root, root) /opt/wifiman-desktop/resources/app.asar
%attr(644, root, root) /opt/wifiman-desktop/service/.env
%attr(755, root, root) /opt/wifiman-desktop/service/wg
%attr(755, root, root) /opt/wifiman-desktop/service/wg-quick
%attr(755, root, root) /opt/wifiman-desktop/service/wifiman-desktopd
%attr(755, root, root) /opt/wifiman-desktop/service/wireguard-go
%attr(755, root, root) /opt/wifiman-desktop/chrome-sandbox
%attr(755, root, root) /opt/wifiman-desktop/chrome_crashpad_handler
%attr(644, root, root) /opt/wifiman-desktop/*.dat
%attr(755, root, root) /opt/wifiman-desktop/lib*.so
%attr(755, root, root) /opt/wifiman-desktop/lib*.so.*
%attr(644, root, root) /opt/wifiman-desktop/LICENSE*
%attr(644, root, root) /opt/wifiman-desktop/*.bin
%attr(644, root, root) /opt/wifiman-desktop/*.pak
%attr(644, root, root) /opt/wifiman-desktop/*.json
%attr(755, root, root) /opt/wifiman-desktop/wifiman-desktop
%attr(644, root, root) %{_datadir}/applications/%{name}.desktop
%attr(644, root, root) %{_datadir}/icons/hicolor/*/apps/%{name}.png
%attr(644, root, root) %{_unitdir}/%{name}.service

%changelog
