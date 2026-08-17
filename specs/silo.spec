Name:           silo
Version:        codetiger_version
Release:        1%{?dist}
Summary:        silo编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/pgsty/silo
Source1:        silo.sh
Source2:        config
Source3:        silo.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/silo
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/silo
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/silo/silo.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/silo/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/silo.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    groupadd -g 3000 -o silo || true
    useradd -u 3000 -o silo -g silo -s /sbin/nologin || true
    chown -R silo:silo /usr/local/silo
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/silo.service ]; then
    %systemd_preun silo.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel silo || true
    groupdel silo || true
fi

# 文件列表
%files
%{_usr}/bin/silo
%{_usr}/local/silo/silo.sh
%{_usr}/lib/systemd/system/silo.service
%config(noreplace) %{_usr}/local/silo/config
%doc

%changelog