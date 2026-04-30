Name:           octopus
Version:        codetiger_version
Release:        1%{?dist}
Summary:        Octopus Application

License:        Apache 2.0
URL:            https://github.com/bestruirui/octopus
Source0:        octopus
Source1:        octopus.sh
Source2:        config
Source3:        octopus.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description
Octopus is a modern application system.

%install
%{__mkdir} -p %{buildroot}/usr/local/octopus
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}/usr/bin/octopus
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/octopus/octopus.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/octopus/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/octopus.service

%files
%attr(755, -, -) /usr/bin/octopus
%attr(755, -, -) /usr/local/octopus/octopus.sh
%attr(644, -, -) /usr/local/octopus/config
%config(noreplace) /usr/local/octopus/config
%attr(644, -, -) %{_usr}/lib/systemd/system/octopus.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd octopus || true
    chown -R octopus:octopus /usr/local/octopus
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/octopus.service ]; then
    %systemd_preun octopus.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel octopus || true
    groupdel octopus || true
    systemctl daemon-reload
fi