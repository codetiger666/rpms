Name:           xray
Version:        codetiger_version
Release:        1%{?dist}
Summary:        xray代理

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/XTLS/Xray-core/releases/download/%{name}-%{version}.tar.gz
Source1:        xray.sh
Source2:        config.json
Source3:        xray.service

%description
xray代理

# 编译前准备
%prep
%setup -q

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/xray
%{__mkdir} -p %{buildroot}/usr/bin
cp xray %{buildroot}/usr/bin
cp geoip.dat %{buildroot}/usr/local/xray
cp geosite.dat %{buildroot}/usr/local/xray
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}/usr/local/xray/xray.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}/usr/local/xray/config.json
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/xray.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd xray -s /sbin/nologin || true
    chown -R xray:xray /usr/local/xray
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/alist.service ]; then
    %systemd_preun alist.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel xray || true
    groupdel xray || true
fi

# 文件列表
%files
%{_usr}/bin/xray
%{_usr}/local/xray/xray.sh
%{_usr}/local/xray/geoip.dat
%{_usr}/local/xray/geosite.dat
%config(noreplace) %{_usr}/local/xray/config.json
%{_usr}/lib/systemd/system/xray.service
%doc

%changelog
