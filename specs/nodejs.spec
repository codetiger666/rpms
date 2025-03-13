Name:           nodejs
Version:        codetiger_version
Release:        1%{?dist}
Summary:        nodejs编译
# 指定版本号覆盖版本
Epoch:          2

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/XTLS/Xray-core/releases/download/%{name}-%{version}.tar.gz
# 禁用依赖推断
AutoReqProv:    no

%description
nodejs编译

# 编译前准备
%prep
%setup -q

# 安装
%install
%{__mkdir} -p %{buildroot}/usr
cp -ra bin %{buildroot}/usr
cp -ra lib %{buildroot}/usr
cp -ra include %{buildroot}/usr

# 文件列表
%files
%{_usr}/bin/node
%{_usr}/bin/corepack
%{_usr}/bin/npm
%{_usr}/bin/npx
%{_usr}/lib/node_modules
%{_usr}/include/node
%doc

%changelog
