Name:           rustfs
Version:        codetiger_version
Release:        1%{?dist}
Summary:        rustfs编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/rustfs/rustfs/releases/download/rustfs
Source1:        rustfs.sh
Source2:        config
Source3:        rustfs.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/rustfs
%{__mkdir} -p %{buildroot}/usr/local/rustfs/data
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/rustfs
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/rustfs/rustfs.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/rustfs/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/rustfs.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    groupadd -g 3000 -o rustfs || true
    useradd -u 3000 -o rustfs -g rustfs -s /sbin/nologin || true
    chown -R rustfs:rustfs /usr/local/rustfs
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/rustfs.service ]; then
    %systemd_preun rustfs.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel rustfs || true
    groupdel rustfs || true
fi

# 文件列表
%files
%{_usr}/bin/rustfs
%{_usr}/local/rustfs/rustfs.sh
%{_usr}/lib/systemd/system/rustfs.service
%config(noreplace) %{_usr}/local/rustfs/config
%doc

%changelog