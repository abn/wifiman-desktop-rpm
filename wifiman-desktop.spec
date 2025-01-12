%global _hardened_build 1
%define _build_id_links none
%define debug_package %{nil}

Name:     wifiman-desktop
Version:  1.1.0
Release:  1
Summary:  Discover devices and access Teleport VPNs
License:  MIT
Vendor:   Ubiquiti Inc. <monitoring@wifiman.com>
URL:      https://wifiman.com/

Source1:  https://desktop.ea.wifiman.com/wifiman-desktop-%{version}-amd64.deb

BuildRequires: binutils
BuildRequires: desktop-file-utils
BuildRequires: gzip
BuildRequires: systemd-units
BuildRequires: tar
BuildRequires: xz

Requires: net-tools
Requires: iw
Requires: systemd
Requires: libappindicator-gtk3
Requires: webkit2gtk4.0
Requires: gtk3

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

%build
ar x %{SOURCE1}
tar xf data.tar.gz

%install
install -m 0755 -vd %{buildroot}%{_datadir}
cp -R usr/share/* %{buildroot}%{_datadir}/

install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp usr/bin/wi-fiman-desktop %{buildroot}%{_bindir}/

install -m 0755 -vd %{buildroot}%{_prefix}/lib/wi-fiman-desktop
install -m 0755 -vp usr/lib/wi-fiman-desktop/wg %{buildroot}%{_prefix}/lib/wi-fiman-desktop/
install -m 0755 -vp usr/lib/wi-fiman-desktop/wg-quick %{buildroot}%{_prefix}/lib/wi-fiman-desktop/
install -m 0755 -vp usr/lib/wi-fiman-desktop/wifiman-desktopd %{buildroot}%{_prefix}/lib/wi-fiman-desktop/
install -m 0755 -vp usr/lib/wi-fiman-desktop/wireguard-go %{buildroot}%{_prefix}/lib/wi-fiman-desktop/
install -m 0644 -vp usr/lib/wi-fiman-desktop/wifiman-desktop.service %{buildroot}%{_prefix}/lib/wi-fiman-desktop/%{name}.service
install -m 0644 -vp usr/lib/wi-fiman-desktop/.env %{buildroot}%{_prefix}/lib/wi-fiman-desktop/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/wi-fiman-desktop.desktop

%post
cp %{_prefix}/lib/wi-fiman-desktop/%{name}.service %{_unitdir}/%{name}.service
%systemd_post %{name}.service

update-mime-database /usr/share/mime &> /dev/null || :
update-desktop-database /usr/share/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%preun
pkill -SIGTERM -f %{_bindir}/wi-fiman-desktop &> /dev/null || :
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
  rm -f %{_unitdir}/%{name}.service
fi
%systemd_postun_with_restart %{name}.service

if [ $1 -eq 0 ] ; then
  update-mime-database /usr/share/mime &> /dev/null || :
  update-desktop-database /usr/share/applications &> /dev/null || :

  touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

# Only perform cleanup if this is a complete removal, not just an upgrade
if [ $1 -eq 0 ]; then
    rm -rf %{_prefix}/lib/wi-fiman-desktop/
    for homedir in /home/*; do
        if [ -d "$homedir/.local/share/ui.wifiman.desktop/" ]; then
            echo "Removing $homedir/.local/share/ui.wifiman.desktop/assets/devices/"
            rm -rf "$homedir/.local/share/ui.wifiman.desktop/assets/devices/"
        fi
    done
fi

%files
%defattr(-,root,root,-)
%dir %attr(755, root, roo) %{_prefix}/lib/wi-fiman-desktop
%attr(644, root, root) %{_prefix}/lib/wi-fiman-desktop/.env
%attr(755, root, root) %{_prefix}/lib/wi-fiman-desktop/wg
%attr(755, root, root) %{_prefix}/lib/wi-fiman-desktop/wg-quick
%attr(755, root, root) %{_prefix}/lib/wi-fiman-desktop/wifiman-desktopd
%attr(644, root, root) %{_prefix}/lib/wi-fiman-desktop/wifiman-desktop.service
%attr(755, root, root) %{_prefix}/lib/wi-fiman-desktop/wireguard-go
%attr(755, root, root) %{_bindir}/wi-fiman-desktop
%attr(644, root, root) %{_datadir}/applications/wi-fiman-desktop.desktop
%attr(644, root, root) %{_datadir}/icons/hicolor/*/apps/wi-fiman-desktop.png

%changelog
* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-3
- spec: include all arch debs in srpm (arun.neelicattu@gmail.com)

* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-2
- tito: fetch sources for build (arun.neelicattu@gmail.com)

* Thu Sep 05 2024 Arun Babu Neelicattu <arun.neelicattu@gmail.com> 0.3.0-1
- Release 0.30.0 package built with tito
