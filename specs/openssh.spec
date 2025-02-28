# 自定义clients名称
%define client_name openssh-clients
Name:           openssh
Version:        codetiger_version
Release:        1%{?dist}
Summary:        openssh编译

License:        GPL
URL:            https://gybyt.cn
Source0:        https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1:        sshd.service
Source2:        sshd_config
Source3:        https://github.com/openssl/openssl/releases/download/openssl-codetiger_openssl_version/openssl-codetiger_openssl_version.tar.gz

BuildRequires:  zlib-devel gcc libselinux-devel
Requires: zlib libselinux

# 描述
%description
openssh编译

# 子包openssh-client定义
%package -n openssh-clients
Summary:      openssh-clients
Requires: openssh = %{version}

# 描述
%description -n openssh-clients
openssh-clients编译

# 子包openssh-server定义
%package -n openssh-server
Summary:      openssh-server
Requires: openssh-clients = %{version}

# 描述
%description -n openssh-server
openssh-server编译

%prep
%setup -q
cp %{SOURCE3} %{_builddir}
cd %{_builddir}
tar -xf %{SOURCE3}
cd openssl-codetiger_openssl_version
./config no-shared --prefix=/usr/local/ssh/openssl --openssldir=/usr/local/ssh/openssl
make -j6 && make install
#echo -e "/usr/local/ssh/openssl/lib64\n/usr/local/ssh/openssl/lib" > /etc/ld.so.conf.d/opensslcodetiger_openssl_version.conf
#/sbin/ldconfig

# 编译
%build
LDFLAGS="-L/usr/local/ssh/openssl/lib64 -L/usr/local/ssh/openssl/lib --static" && \
CFLAGS="-I/usr/local/ssh/openssl/include" && \
./configure \
  --prefix=/usr \
  --sysconfdir=/etc/ssh \
  --with-ssl-dir=/usr/local/ssh/openssl \
  --with-selinux
make -j6

# 安装
%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/etc/ssh/sshd_config
#mkdir -p %{buildroot}/usr/local/ssh
#/bin/cp -r /usr/local/ssh/openssl %{buildroot}/usr/local/ssh/openssl
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/sshd.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}/etc/ssh/sshd_config
#rm -rf /etc/ld.so.conf.d/opensslcodetiger_openssl_version.conf
#/sbin/ldconfig

# 安装后操作
%post -n openssh-server
if [ $1 == 1 ]; then
    if [ -e /etc/ssh/ssh_host_rsa_key ]; then
        chmod 0600 /etc/ssh/ssh_host_*_key
        chown -R root:root /etc/ssh
    else
        ssh-keygen -A
    fi
fi

# 卸载前准备
%preun -n openssh-server
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/sshd.service ]; then
    %systemd_preun sshd.service
    fi
fi

# 文件列表
%files
%defattr(-,root,root,0755)
/etc/ssh/moduli
%{_usr}/bin/ssh-keygen
%{_usr}/share/man/man1/ssh-keygen.1.gz
%{_usr}/share/man/man5/moduli.5.gz


# 子包openssh-server文件列表
%files -n openssh-server
%{_usr}/lib/systemd/system/sshd.service
%{_usr}/libexec/sftp-server
%{_usr}/libexec/ssh-keysign
%{_usr}/libexec/ssh-pkcs11-helper
%{_usr}/libexec/ssh-sk-helper
%{_usr}/libexec/sshd-session
%{_usr}/sbin/sshd
%{_usr}/share/man/man5/sshd_config.5.gz
%{_usr}/share/man/man8/sftp-server.8.gz
%{_usr}/share/man/man8/ssh-keysign.8.gz
%{_usr}/share/man/man8/ssh-pkcs11-helper.8.gz
%{_usr}/share/man/man8/ssh-sk-helper.8.gz
%{_usr}/share/man/man8/sshd.8.gz
%config(noreplace) /etc/ssh/sshd_config

# 子包openssh-client文件列表
%files -n openssh-clients
%{_usr}/bin/scp
%{_usr}/bin/sftp
%{_usr}/bin/ssh
%{_usr}/bin/ssh-add
%{_usr}/bin/ssh-agent
%{_usr}/bin/ssh-keyscan
%config(noreplace) /etc/ssh/ssh_config
%{_usr}/share/man/man1/scp.1.gz
%{_usr}/share/man/man1/sftp.1.gz
%{_usr}/share/man/man1/ssh-add.1.gz
%{_usr}/share/man/man1/ssh-agent.1.gz
%{_usr}/share/man/man1/ssh-keyscan.1.gz
%{_usr}/share/man/man1/ssh.1.gz
%{_usr}/share/man/man5/ssh_config.5.gz

# 文档
%doc

# 更改日志
%changelog
