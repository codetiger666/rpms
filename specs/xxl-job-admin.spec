Name:           xxl-job-admin
Version:        codetiger_version
Release:        1%{?dist}
Summary:        xxl-job-admin编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/codetiger666/xxl-job/releases/download/%{Version}/xxl-job-admin.jar
Source1:        xxl-job-admin.sh
Source2:        config
Source3:        xxl-job-admin.service
Source4:        logback.xml

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/xxl-job-admin
%{__install} -p -D -m 0644 %{SOURCE0}  %{buildroot}/usr/local/xxl-job-admin/xxl-job-admin.jar
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/xxl-job-admin/xxl-job-admin.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/xxl-job-admin/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/xxl-job-admin.service
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_usr}/local/xxl-job-admin/logback.xml
# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd xxl-job-admin || true
    chown -R xxl-job-admin:xxl-job-admin /usr/local/xxl-job-admin
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/xxl-job-admin.service ]; then
    %systemd_preun xxl-job-admin.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel xxl-job-admin || true
    groupdel xxl-job-admin || true
fi

# 文件列表
%files
%{_usr}/local/xxl-job-admin/xxl-job-admin.sh
%{_usr}/local/xxl-job-admin/xxl-job-admin.jar
%{_usr}/lib/systemd/system/xxl-job-admin.service
%config(noreplace) %{_usr}/local/xxl-job-admin/config
%doc

%changelog