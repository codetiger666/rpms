Name:           electerm
Version:        codetiger_version
Release:         1%{?dist}
Summary:        electerm编译
# 指定版本号覆盖版本
Epoch:          1

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/electerm/electerm-web/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        config
Source2:        electerm.sh
Source3:        electerm.service

Requires:       nodejs >= 2:20.18.3
Requires:       codetiger-util >= 1.0.0

# 禁用依赖推断
AutoReqProv:    no

%description
electerm编译

# 编译前准备
%prep
%setup -q

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd electerm -s /sbin/nologin || true
    chown -R electerm:electerm /usr/local/electerm
fi

# 安装
%install
npm config set legacy-peer-deps true
npm install
npm run build
%{__mkdir} -p %{buildroot}/usr/local/electerm/app
cp -ra * %{buildroot}/usr/local/electerm/app
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/local/electerm/config
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_usr}/local/electerm/electerm.sh
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/electerm.service

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/electerm.service ]; then
    %systemd_preun electerm.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel electerm || true
    groupdel electerm || true
fi


# 文件列表
%files
%{_usr}/local/electerm/app
%{_usr}/local/electerm/electerm.sh
%{_usr}/lib/systemd/system/electerm.service
%config(noreplace) %{_usr}/local/electerm/config
%doc

%changelog
