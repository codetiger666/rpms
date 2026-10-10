Name:           moontvplus
Version:        codetiger_version
Release:         1%{?dist}
Summary:        moontvplus编译
# 指定版本号覆盖版本
Epoch:          1

License:        GPL
URL:            https://gybyt.cn
Source0:        https://github.com/mtvpls/MoonTVPlus/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        config
Source2:        moontvplus.sh
Source3:        moontvplus.service

Requires:       nodejs >= 2:20.18.3
BuildRequires:  nodejs >= 2:20.18.3
BuildRequires:  gcc-c++
BuildRequires:  python3
BuildRequires:  make
BuildRequires:  libtool

# 禁用依赖推断
AutoReqProv:    no

%description
moontvplus编译

# 编译前准备
%prep
%setup -q

%build
corepack enable || true
corepack prepare pnpm@latest --activate || true
pnpm install --frozen-lockfile
pnpm run build
rm -rf node_modules
pnpm install --prod

# 安装后操作
%post
if [ $1 == 1 ]; then
    useradd moontvplus -s /sbin/nologin || true
    chown -R moontvplus:moontvplus /usr/local/moontvplus
fi

# 安装
%install
%{__mkdir} -p %{buildroot}/usr/local/moontvplus/app
cp -ra ./ %{buildroot}/usr/local/moontvplus/app
%{__mkdir} -p %{buildroot}/usr/local/moontvplus/data
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_usr}/local/moontvplus/config
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_usr}/local/moontvplus/moontvplus.sh
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_usr}/lib/systemd/system/moontvplus.service

# 卸载前准备
%preun
if [ $1 == 0 ]; then
    if [ -f /usr/lib/systemd/system/moontvplus.service ]; then
    %systemd_preun moontvplus.service
    fi
fi

# 卸载后步骤
%postun
if [ $1 == 0 ]; then
    userdel moontvplus || true
    groupdel moontvplus || true
fi


# 文件列表
%files
%{_usr}/local/moontvplus/app
%{_usr}/local/moontvplus/moontvplus.sh
%{_usr}/lib/systemd/system/moontvplus.service
%config(noreplace) %{_usr}/local/moontvplus/config
%dir %{_usr}/local/moontvplus/data
%ghost %{_usr}/local/moontvplus/data/moontv.db
%doc

%changelog