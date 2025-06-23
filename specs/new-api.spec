Name:           new-api
Version:        codetiger_version
Release:        1%{?dist}
Summary:        New Api编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/QuantumNous/new-api/releases/download/v%{version}/new-api
Source1:        new-api.sh
Source2:        .env
Source3:        new-api.service


Requires:       codetiger-util >= 1.0.0

%description


# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/new-api
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/new-api
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/new-api/new-api.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/new-api/.env
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/new-api.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd new-api -s /sbin/nologin || true
    chown -R new-api:new-api /usr/local/new-api
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/new-api.service ]; then
    %systemd_preun new-api.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel new-api || true
    groupdel new-api || true
fi

# 文件列表
%files
%{_usr}/bin/new-api
%{_usr}/local/new-api/new-api.sh
%{_usr}/lib/systemd/system/new-api.service
%config(noreplace) %{_usr}/local/new-api/.env
%doc

%changelog