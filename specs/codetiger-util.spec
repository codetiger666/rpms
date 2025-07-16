Name:           codetiger-util
Version:        1.0.1
Release:        1%{?dist}
Summary:        codeitger util编译
# 指定版本号覆盖版本
Epoch:          1

License:        GPL
URL:            https://gybyt.cn
Source0:        common.sh
# 禁用依赖推断
AutoReqProv:    no

%description
codeitger工具类

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/codetiger-util
%{__install} -p -D -m 0755 %{SOURCE0}  %{buildroot}/usr/local/codetiger-util/common.sh

# 文件列表
%files
%{_usr}/local/codetiger-util/common.sh
%doc

%changelog
