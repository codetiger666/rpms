Name:           uptime-kuma
Version:        codetiger_version
Release:         1%{?dist}
Summary:        uptime-kuma编译
# 指定版本号覆盖版本
Epoch:          1

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/louislam/uptime-kuma/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        config
Source2:        uptime-kuma.sh
Source3:        uptime-kuma.service

Requires:       nodejs >= 2:20.18.3
Requires:       codetiger-util >= 1.0.0

# 禁用依赖推断
AutoReqProv:    no

%description
uptime-kuma编译

# 编译前准备
%prep
%setup -q

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd uptime-kuma -s /sbin/nologin || true
    chown -R uptime-kuma:uptime-kuma /usr/local/uptime-kuma
fi

# 安装
%install
npm install
npm ci --production
npm run download-dist
%{__mkdir} -p %{buildroot}/usr/local/uptime-kuma/app
cp -ra * %{buildroot}/usr/local/uptime-kuma/app
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/local/uptime-kuma/config
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_usr}/local/uptime-kuma/uptime-kuma.sh
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/uptime-kuma.service

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/uptime-kuma.service ]; then
    %systemd_preun uptime-kuma.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel uptime-kuma || true
    groupdel uptime-kuma || true
fi


# 文件列表
%files
%{_usr}/local/uptime-kuma/app
%{_usr}/local/uptime-kuma/uptime-kuma.sh
%{_usr}/lib/systemd/system/uptime-kuma.service
%config(noreplace) %{_usr}/local/uptime-kuma/config
%doc

%changelog
