OPENSSL_VERSION=$(get_latest_version "release" "openssl/openssl")

program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/openssh.spec
  sudo sed -i "s/codetiger_openssl_version/$(echo $OPENSSL_VERSION | sed 's/openssl-//' )/g" specs/openssh.spec
  sudo /bin/cp specs/openssh.spec rpm/rpmbuild/SPECS/openssh.spec
  sudo /bin/cp services/sshd.service rpm/rpmbuild/SOURCES
  sudo /bin/cp openssh/sshd_config rpm/rpmbuild/SOURCES
  wget https://github.com/openssh/openssh-portable/archive/refs/tags/V_$(echo ${project_version} | sed 's/\./_/g').tar.gz
  wget https://github.com/openssl/openssl/releases/download/${OPENSSL_VERSION}/${OPENSSL_VERSION}.tar.gz
  mkdir rpm/rpmbuild/SOURCES -p
  tar -xf V_$(echo ${project_version} | sed 's/\./_/g').tar.gz
  mv openssh-portable-V_$(echo ${project_version} | sed 's/\./_/g') openssh-${project_version}
  tar -zcvf openssh-${project_version}.tar.gz openssh-${project_version}/
  sudo /bin/cp openssh-${project_version}.tar.gz rpm/rpmbuild/SOURCES/openssh-${project_version}.tar.gz
  sudo /bin/cp ${OPENSSL_VERSION}.tar.gz rpm/rpmbuild/SOURCES/${OPENSSL_VERSION}.tar.gz
}
