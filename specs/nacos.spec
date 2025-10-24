Name:           nacos
Version:        codetiger_version
Release:        1%{?dist}
Summary:        nacos编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/alibaba/nacos/releases/download/%{Version}/nacos-server.jar
Source1:        nacos.sh
Source2:        config
Source3:        nacos.service
Source4:        application.properties
Source5:        logback.xml

Requires:       codetiger-util >= 1.0.0
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/nacos
%{__install} -p -D -m 0644 %{SOURCE0}  %{buildroot}/usr/local/nacos/nacos-server.jar
%{__install} -p -D -m 0755 %{SOURCE1} %{buildroot}%{_usr}/local/nacos/nacos.sh
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_usr}/local/nacos/config
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/nacos.service
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_usr}/local/nacos/application.properties
%{__install} -p -D -m 0644 %{SOURCE5} %{buildroot}%{_usr}/local/nacos/logback.xml
# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd nacos || true
    chown -R nacos:nacos /usr/local/nacos
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/nacos.service ]; then
    %systemd_preun nacos.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel nacos || true
    groupdel nacos || true
fi

# 文件列表
%files
%{_usr}/local/nacos/nacos.sh
%{_usr}/local/nacos/nacos-server.jar
%{_usr}/lib/systemd/system/nacos.service
%config(noreplace) %{_usr}/local/nacos/config
%config(noreplace) %{_usr}/local/nacos/application.properties
%config(noreplace) %{_usr}/local/nacos/logback.xml
%doc

%changelog