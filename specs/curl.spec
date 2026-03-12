Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: codetiger_version
Release: 1%{?dist}
License: MIT
Source: https://curl.se/download/%{name}-%{version}.tar.gz

Provides: curl-full = %{version}-%{release}
Provides: webclient
URL: https://curl.se/
BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn2-devel
BuildRequires: libnghttp2-devel
BuildRequires: libpsl-devel
BuildRequires: libssh-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: openssl-devel
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: sed
BuildRequires: zlib-devel

BuildRequires: perl

# hostname(1) is used by the test-suite but it is missing in armv7hl buildroot
BuildRequires: hostname

# nghttpx (an HTTP/2 proxy) is used by the upstream test-suite
BuildRequires: nghttp2


# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl%{?_isa} >= %{version}-%{release}

# require at least the version of libpsl that we were built against,
# to ensure that we have the necessary symbols available (#1631804)
%global libpsl_version %(pkg-config --modversion libpsl 2>/dev/null || echo 0)

# require at least the version of libssh that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh_version %(pkg-config --modversion libssh 2>/dev/null || echo 0)

# require at least the version of openssl-libs that we were built against,
# to ensure that we have the necessary symbols available (#1462184, #1462211)
# (we need to translate 3.0.0-alpha16 -> 3.0.0-0.alpha16 and 3.0.0-beta1 -> 3.0.0-0.beta1 though)
%global openssl_version %({ pkg-config --modversion openssl 2>/dev/null || echo 0;} | sed 's|-|-0.|')

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks. 

%package -n libcurl
Summary: A library for getting files from web servers
Requires: libpsl%{?_isa} >= %{libpsl_version}
Requires: libssh%{?_isa} >= %{libssh_version}
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl-full = %{version}-%{release}
Provides: libcurl-full%{?_isa} = %{version}-%{release}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Requires: libcurl%{?_isa} = %{version}-%{release}

Provides: curl-devel = %{version}-%{release}
Provides: curl-devel%{?_isa} = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.

%package -n curl-minimal
Summary: Conservatively configured build of curl for minimal installations
Provides: curl = %{version}-%{release}
Conflicts: curl
RemovePathPostfixes: .minimal

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl%{?_isa} >= %{version}-%{release}

%description -n curl-minimal
This is a replacement of the 'curl' package for minimal installations.  It
comes with a limited set of features compared to the 'curl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%package -n libcurl-minimal
Summary: Conservatively configured build of libcurl for minimal installations
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl = %{version}-%{release}
Provides: libcurl%{?_isa} = %{version}-%{release}
Conflicts: libcurl%{?_isa}
RemovePathPostfixes: .minimal
# needed for RemovePathPostfixes to work with shared libraries
%undefine __brp_ldconfig

%description -n libcurl-minimal
This is a replacement of the 'libcurl' package for minimal installations.  It
comes with a limited set of features compared to the 'libcurl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}  --libdir=%{_libdir} --with-openssl --with-nghttp2 --enable-websockets --with-zlib --enable-shared --enable-static \
--enable-ipv6 --enable-symbol-hiding --enable-threaded-resolver --with-gssapi --with-ssl --with-brotli --with-libidn2 --with-libssh --with-ldap \
--enable-ldaps --with-ca-bundle=/etc/pki/tls/certs/ca-bundle.crt
make -j6


# 安装
%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_libdir}/libcurl.la

%files
%{_usr}/bin/curl
%{_usr}/bin/wcurl

%files -n libcurl
%{_libdir}/libcurl.so
%{_libdir}/libcurl.so.4
%{_libdir}/libcurl.so.4.[0-9].[0-9]

%files -n libcurl-devel
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/libcurl.a
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/*curl.1*
%{_datadir}/aclocal/libcurl.m4

%files -n curl-minimal
%{_bindir}/curl
%{_mandir}/man1/curl.1*

%files -n libcurl-minimal
%license COPYING
%{_libdir}/libcurl.so.4
%{_libdir}/libcurl.so.4.[0-9].[0-9]

%changelog
