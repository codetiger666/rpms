Name:           copilot-proxies
Version:        codetiger_version
Release:        1%{?dist}
Summary:        copilot-proxies编译

License:        GPL
URL:            https://gybyt.cn
Source0:        wget https://gitee.com/ripperTs/github-copilot-proxies/releases/download/v%{version}/copilot-proxies
Source1:        copilot-proxies.sh
Source2:        .env
Source3:        copilot-proxies.service
    
Requires:       codetiger-util >= 1.0.1

%description


# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/copilot-proxies
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/copilot-proxies
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/copilot-proxies/copilot-proxies.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/copilot-proxies/.env
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/copilot-proxies.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd copilot-proxies || true
    chown -R copilot-proxies:copilot-proxies /usr/local/copilot-proxies
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/copilot-proxies.service ]; then
    %systemd_preun copilot-proxies.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel copilot-proxies || true
    groupdel copilot-proxies || true
fi

# 文件列表
%files
%{_usr}/bin/copilot-proxies
%{_usr}/local/copilot-proxies/copilot-proxies.sh
%{_usr}/lib/systemd/system/copilot-proxies.service
%config(noreplace) %{_usr}/local/copilot-proxies/.env
%doc

%changelog