# 自定义clients名称
%define client_name openssh-clients
%define __brp_check_rpaths %{nil}

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
Requires: openssh-openssl-libs = %{version}-%{release}

# 描述
%description -n openssh-clients
openssh-clients编译

# 子包openssh-server定义
%package -n openssh-server
Summary:      openssh-server
Requires: openssh-clients = %{version}-%{release}

# 描述
%description -n openssh-server
openssh-server编译

# 子包openssl libs定义
%package -n openssh-openssl-libs
Summary:      OpenSSL libraries for openssh
Provides: openssh-openssl-libs = %{version}-%{release}

%description -n openssh-openssl-libs
Custom OpenSSL libraries bundled with openssh

%prep
%setup -q
cp %{SOURCE3} %{_builddir}
cd %{_builddir}
tar -xf %{SOURCE3}
cd openssl-codetiger_openssl_version

# 根据架构自动选择库目录 (x86_64=lib, aarch64=lib64)
%if "%{_lib}" == "lib64"
OPENSSL_LIBDIR=lib64
%else
OPENSSL_LIBDIR=lib
%endif

# 编译OpenSSL为共享库，支持跨架构
./config --prefix=/usr/local/ssh/openssl \
    --openssldir=/usr/local/ssh/openssl \
    --libdir=/usr/local/ssh/openssl/$OPENSSL_LIBDIR \
    shared \
    zlib
make -j$(nproc)
make install_sw

# 编译
%build
# 根据架构自动选择库目录
%if "%{_lib}" == "lib64"
OPENSSL_LIBDIR=lib64
%else
OPENSSL_LIBDIR=lib
%endif

export CPPFLAGS="-I/usr/local/ssh/openssl/include"
export LDFLAGS="-L/usr/local/ssh/openssl/$OPENSSL_LIBDIR -Wl,-rpath,/usr/local/ssh/openssl/$OPENSSL_LIBDIR"
export CFLAGS="$CPPFLAGS"

./configure \
  --prefix=/usr \
  --sysconfdir=/etc/ssh \
  --with-ssl-dir=/usr/local/ssh/openssl \
  --with-selinux
make -j$(nproc)

# 安装
%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/etc/ssh/sshd_config

# 根据架构自动选择库目录
%if "%{_lib}" == "lib64"
OPENSSL_LIBDIR=lib64
%else
OPENSSL_LIBDIR=lib
%endif

# 从/usr/local/ssh/openssl目录复制库到RPM包
mkdir -p %{buildroot}/usr/local/ssh/openssl/$OPENSSL_LIBDIR
mkdir -p %{buildroot}/usr/local/ssh/openssl/include

# 只复制so文件（共享库），保留符号链接(-P参数)
cp -P /usr/local/ssh/openssl/$OPENSSL_LIBDIR/libcrypto.so* %{buildroot}/usr/local/ssh/openssl/$OPENSSL_LIBDIR/
cp -P /usr/local/ssh/openssl/$OPENSSL_LIBDIR/libssl.so* %{buildroot}/usr/local/ssh/openssl/$OPENSSL_LIBDIR/
cp -r /usr/local/ssh/openssl/include/openssl %{buildroot}/usr/local/ssh/openssl/include/

%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/sshd.service
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}/etc/ssh/sshd_config

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
%{_usr}/libexec/sshd-auth
%config(noreplace) /etc/ssh/ssh_config
%{_usr}/share/man/man1/scp.1.gz
%{_usr}/share/man/man1/sftp.1.gz
%{_usr}/share/man/man1/ssh-add.1.gz
%{_usr}/share/man/man1/ssh-agent.1.gz
%{_usr}/share/man/man1/ssh-keyscan.1.gz
%{_usr}/share/man/man1/ssh.1.gz
%{_usr}/share/man/man5/ssh_config.5.gz

# 子包openssh-openssl-libs文件列表
%files -n openssh-openssl-libs
%dir /usr/local/ssh/openssl
%dir /usr/local/ssh/openssl/%{_lib}
%dir /usr/local/ssh/openssl/include
/usr/local/ssh/openssl/%{_lib}/libcrypto.so*
/usr/local/ssh/openssl/%{_lib}/libssl.so*
/usr/local/ssh/openssl/include/openssl/

# 文档
%doc

# 更改日志
%changelog
