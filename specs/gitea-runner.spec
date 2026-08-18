Name:           gitea-runner
Version:        codetiger_version
Release:        1%{?dist}
Summary:        gitea-runner编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://gitea.com/gitea/runner/releases/download/v3.1.0/gitea-runner
Source1:        gitea-runner.sh
Source2:        config
Source3:        gitea-runner.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/gitea-runner
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/gitea-runner
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/gitea-runner/gitea-runner.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/gitea-runner/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/gitea-runner.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd gitea-runner
     usermod -aG docker gitea-runner
    chown -R gitea-runner:gitea-runner /usr/local/gitea-runner
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/gitea-runner.service ]; then
    %systemd_preun gitea-runner.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel gitea-runner
fi

# 文件列表
%files
%{_usr}/bin/gitea-runner
%{_usr}/local/gitea-runner/gitea-runner.sh
%{_usr}/lib/systemd/system/gitea-runner.service
%config(noreplace) %{_usr}/local/gitea-runner/config
%doc

%changelog