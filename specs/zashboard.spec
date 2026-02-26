Name:           zashboard
Version:        codetiger_version
Release:        1%{?dist}
Summary:        zashboard编译

License:        GPL
URL:            https://gybyt.cn

Requires:       codetiger-util >= 1.0.0
Source0:        zashboard
    
# 禁用依赖推断
AutoReqProv:    no

%description

# 安装
%install
%{__mkdir} -p %{buildroot}/home/wwwroot
/bin/cp -ra %{SOURCE0} %{buildroot}/home/wwwroot

# 文件列表
%files
/home/wwwroot/zashboard
%doc

%changelog