OPENSSL_VERSION=$(get_latest_version "release" "openssl/openssl")

program_init(){
  version=$(echo ${project_version} | sed 's/_/./g; s/P/p/')
  sudo sed -i "s/codetiger_version/${version}/g" specs/openssh.spec
  sudo sed -i "s/codetiger_openssl_version/$OPENSSL_VERSION/g" specs/openssh.spec
  sudo /bin/cp specs/openssh.spec rpm/rpmbuild/SPECS/openssh.spec
  sudo /bin/cp services/sshd.service rpm/rpmbuild/SOURCES
  sudo /bin/cp openssh/sshd_config rpm/rpmbuild/SOURCES
  wget https://github.com/openssh/openssh-portable/archive/refs/tags/${project_version}.tar.gz
  wget https://github.com/openssl/openssl/releases/download/openssl-${OPENSSL_VERSION}/openssl-${OPENSSL_VERSION}.tar.gz
  mkdir rpm/rpmbuild/SOURCES -p
  tar -xf ${project_version}.tar.gz
  mv openssh-portable-${project_version} openssh-${version}
  sudo /bin/cp openssh-${version}.tar.gz rpm/rpmbuild/SOURCES/openssh-${version}.tar.gz
  sudo /bin/cp openssl-${OPENSSL_VERSION}.tar.gz rpm/rpmbuild/SOURCES/openssl-${OPENSSL_VERSION}.tar.gz
}
