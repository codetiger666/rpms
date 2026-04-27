Name:           axonhub
Version:        codetiger_version
Release:        1%{?dist}
Summary:        AxonHub AI Gateway System

License:        Apache 2.0
URL:            https://github.com/looplj/axonhub
Source0:        axonhub
Source1:        axonhub.sh
Source2:        config
Source3:        axonhub.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description
AxonHub is a modern AI gateway system that provides intelligent routing and management for AI services.

%install
%{__mkdir} -p %{buildroot}/usr/local/axonhub
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0} %{buildroot}/usr/bin/axonhub
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/axonhub/axonhub.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/axonhub/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/axonhub.service

%files
%attr(755, -, -) /usr/bin/axonhub
%attr(755, -, -) /usr/local/axonhub/axonhub.sh
%attr(644, -, -) /usr/local/axonhub/config
%config(noreplace) /usr/local/axonhub/config
%attr(644, -, -) %{_usr}/lib/systemd/system/axonhub.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd axonhub || true
    chown -R axonhub:axonhub /usr/local/axonhub
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/axonhub.service ]; then
    %systemd_preun axonhub.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel axonhub || true
    groupdel axonhub || true
    systemctl daemon-reload
fi