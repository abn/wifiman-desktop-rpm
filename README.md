[![Copr Build Status](https://copr.fedorainfracloud.org/coprs/abn/wifiman-desktop/package/wifiman-desktop/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/abn/wifiman-desktop/)

# RPM Package: wifiman-desktop

This repository holds the RPM package source for [wifiman-desktop](https://www.ui.com/download/app/wifiman-desktop).

> WiFiman is here to save your home or office network from sluggish surfing, endless buffering, and congested data 
> channels.

> [!NOTE]  
> This is a wrapper package of the WiFiman Desktop releases for Ubuntu available [here](https://www.ui.com/download/app/wifiman-desktop)
> and is in no way affliated with or maintained by [Ubiquity Inc](https://ui.com/) for any application support or questions please see
> [here](https://help.ui.com/hc/en-us).


## Usage
You can use this package by enabling the copr repository at [abn/wifiman-desktop](https://copr.fedorainfracloud.org/coprs/abn/wifiman-desktop/) as described [here](https://fedorahosted.org/copr/wiki/HowToEnableRepo).

```sh
dnf copr enable abn/wifiman-desktop
dnf install wifiman-desktop
```

Once installed you can enable and start the daemon using the following command, then launch the application.

```sh
systemctl enable --now wifiman-desktop.service
```
