Name:           openlist
Version:        codetiger_version
Release:        1%{?dist}
Summary:        openlist网盘

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/OpenListTeam/OpenList/releases/download/v%{version}/openlist-linux-codetiger_arch.tar.gz
Source1:        openlist.service
Source2:        openlist.sh
Source3:        config
Source4:        config.json

%description

# 编译前准备
%prep
rm -rf %{_builddir}/*
cp %{SOURCE0} %{_builddir}
tar -xf %{SOURCE0}


# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/openlist/data
%{__mkdir} -p %{buildroot}/usr/bin
cp openlist %{buildroot}/usr/bin
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/lib/systemd/system/openlist.service
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}/usr/local/openlist/openlist.sh
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}/usr/local/openlist/config
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}/usr/local/openlist/data/config.json


# 安装后操作
%post
if [ $1 == 1 ]; then
    groupadd -g 3000 -o openlist || true
    useradd -u 3000 -o openlist -g openlist -s /sbin/nologin || true
    chown -R openlist:openlist /usr/local/openlist
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/openlist.service ]; then
    %systemd_preun openlist.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel openlist || true
    groupdel openlist || true
fi

# 文件列表
%files
%{_usr}/bin/openlist
%{_usr}/local/openlist/openlist.sh
%config(noreplace) %{_usr}/local/openlist/config
%config(noreplace) %{_usr}/local/openlist/data/config.json
%{_usr}/lib/systemd/system/openlist.service
%doc

%changelog
