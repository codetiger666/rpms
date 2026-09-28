Name:           forgejo-runner
Version:        codetiger_version
Release:        1%{?dist}
Summary:        forgejo-runner编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://code.forgejo.org/forgejo/runner/releases/download/v%{version}/forgejo-runner
Source1:        forgejo-runner.sh
Source2:        config
Source3:        forgejo-runner.service

    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/forgejo-runner
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/forgejo-runner
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/forgejo-runner/forgejo-runner.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/forgejo-runner/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/forgejo-runner.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd forgejo-runner
    usermod -aG docker forgejo-runner
    chown -R forgejo-runner:forgejo-runner /usr/local/forgejo-runner
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/forgejo-runner.service ]; then
    %systemd_preun forgejo-runner.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel forgejo-runner
fi

# 文件列表
%files
%{_usr}/bin/forgejo-runner
%{_usr}/local/forgejo-runner/forgejo-runner.sh
%{_usr}/lib/systemd/system/forgejo-runner.service
%config(noreplace) %{_usr}/local/forgejo-runner/config
%doc

%changelog