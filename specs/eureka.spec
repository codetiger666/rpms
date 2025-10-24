Name:           eureka
Version:        codetiger_version
Release:        1%{?dist}
Summary:        eureka编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/codetiger666/eureka-server/releases/download/%{Version}/eureka-server.jar
Source1:        eureka.sh
Source2:        config
Source3:        eureka.service

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/eureka
%{__install} -p -D -m 0644 %{SOURCE0}  %{buildroot}/usr/local/eureka/eureka-server.jar
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/eureka/eureka.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/eureka/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/eureka.service
# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd eureka || true
    chown -R eureka:eureka /usr/local/eureka
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/eureka.service ]; then
    %systemd_preun eureka.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel eureka || true
    groupdel eureka || true
fi

# 文件列表
%files
%{_usr}/local/eureka/eureka.sh
%{_usr}/local/eureka/eureka-server.jar
%{_usr}/lib/systemd/system/eureka.service
%config(noreplace) %{_usr}/local/eureka/config
%doc

%changelog