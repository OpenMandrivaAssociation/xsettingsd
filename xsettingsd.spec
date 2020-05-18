Summary:	Provides settings to X11 applications via the XSETTINGS specification
Name:		xsettingsd
Version:	1.0.0
Release:	2
Group:		Graphical desktop/Other
License:	BSD
Url:		https://github.com/derat/xsettingsd
Source0:	https://github.com/derat/xsettingsd/archive/v%{version}.tar.gz
BuildRequires:	scons
BuildRequires:	pkgconfig(x11)
Conflicts:	xsettings-kde

%description
xsettingsd is a daemon that implements the XSETTINGS specification.
It is intended to be small, fast, and minimally dependent on other
libraries.  It can serve as an alternative to gnome-settings-daemon for
users who are not using the GNOME desktop environment but who still run
GTK+ applications and want to configure things such as themes, font
antialiasing/hinting, and UI sound effects.

%prep
%autosetup -p1

%build
%set_build_flags
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" %scons xsettingsd dump_xsettings

%install
for file in %{name} dump_xsettings; do
    install -Dpm 0755 $file %{buildroot}%{_bindir}/$file
    install -Dpm 0644 $file.1 %{buildroot}%{_mandir}/man1/$file.1
done

# (tpg) add autostart file
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
cat << EOF > %{buildroot}%{_sysconfdir}/xdg/autostart/xsettingsd.desktop
[Desktop Entry]
Exec=xsettingsd
Name=Provides settings to X11 applications
X-KDE-StartupNotify=false
X-KDE-autostart-after=kdesktop
X-KDE-autostart-phase=1
Type=Service
OnlyShowIn=KDE;LXQt;
EOF

%files
%doc COPYING README
%{_sysconfdir}/xdg/autostart/xsettingsd.desktop
%{_bindir}/%{name}
%{_bindir}/dump_xsettings
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/dump_xsettings.1.*
