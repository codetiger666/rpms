Name:           redis
Version:        codetiger_version
Release:        1%{?dist}
Summary:        redis编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/redis/redis/archive/%{name}-%{version}.tar.gz
Source1:        redis.service

BuildRequires:  gcc make

# 描述
%description
redis自编译

# 编译前准备
%prep
%setup -q -n %{name}-%{version}

# 编译
%build
make USE_SYSTEMD=yes MALLOC=jemalloc -j6

# 安装
%install
make install PREFIX=%{buildroot}/usr
%{__mkdir} -p %{buildroot}/etc/redis
%{__install} -p -D -m 0644 redis.conf %{buildroot}/etc/redis/redis.conf
%{__install} -p -D -m 0644 sentinel.conf %{buildroot}/etc/redis/sentinel.conf
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/lib/systemd/system/redis.service

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd redis -s /sbin/nologin || true
    mkdir -p /etc/redis
    mkdir -p /var/log/redis
    mkdir -p /var/lib/redis
    chown -R redis:redis /var/log/redis
    chown -R redis:redis /var/lib/redis
fi

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/redis.service ]; then
    %systemd_preun redis.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel redis || true
    groupdel redis || true
fi

# 文件列表
%files
%defattr(-,root,root,0755)
/usr/bin/redis-server
/usr/bin/redis-cli
/usr/bin/redis-sentinel
/usr/bin/redis-benchmark
/usr/bin/redis-check-aof
/usr/bin/redis-check-rdb
%config(noreplace) /etc/redis/redis.conf
%config(noreplace) /etc/redis/sentinel.conf
%{_usr}/lib/systemd/system/redis.service
# 文档
%doc

# 更改日志
%changelog