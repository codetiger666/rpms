Name:           openlist-api
Version:        codetiger_version
Release:        1%{?dist}
Summary:        openlist网盘Api服务

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/OpenListTeam/OpenList-APIPages/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        openlist-api.service
Source2:        openlist-api.sh
Source3:        .env

Requires:       codetiger-util >= 1.0.0
Requires:       nodejs

%description

# 编译前准备
%prep
%setup -q

# 安装
%install
npm install
npm install webpack webpack-cli
npx webpack --mode production
%{__mkdir} -p %{buildroot}/usr/local/openlist-api
cp dist/bundle.js %{buildroot}/usr/local/openlist-api/openlist-api.js
cp -ra public %{buildroot}/usr/local/openlist-api
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/lib/systemd/system/openlist-api.service
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/usr/local/openlist-api/openlist-api.sh
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}/usr/local/openlist-api/.env


# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd openlist-api -s /sbin/nologin || true
    chown -R openlist-api:openlist-api /usr/local/openlist-api
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/openlist-api.service ]; then
    %systemd_preun openlist-api.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel openlist-api || true
    groupdel openlist-api || true
fi

# 文件列表
%files
%{_usr}/local/openlist-api/openlist-api.sh
%{_usr}/local/openlist-api/openlist-api.js
%{_usr}/local/openlist-api/public
%config(noreplace) %{_usr}/local/openlist-api/.env
%{_usr}/lib/systemd/system/openlist-api.service
%doc

%changelog
