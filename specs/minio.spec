Name:           minio
Version:        codetiger_version
Release:        1%{?dist}
Summary:        minio编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://dl.min.io/aistor/minio/release/minio
Source1:        minio.sh
Source2:        config
Source3:        minio.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/minio
%{__mkdir} -p %{buildroot}/usr/bin
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/bin/minio
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/minio/minio.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/minio/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/minio.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd minio || true
    chown -R minio:minio /usr/local/minio
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/minio.service ]; then
    %systemd_preun minio.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel minio || true
    groupdel minio || true
fi

# 文件列表
%files
%{_usr}/bin/minio
%{_usr}/local/minio/minio.sh
%{_usr}/lib/systemd/system/minio.service
%config(noreplace) %{_usr}/local/minio/config
%doc

%changelog