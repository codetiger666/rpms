program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/forgejo.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  sudo sed -i "s/codetiger_arch/${ARCH}/g" specs/forgejo.spec
  wget https://codeberg.org/forgejo/forgejo/releases/download/v${project_version}/forgejo-${project_version}-linux-${ARCH}
  sudo /bin/cp specs/forgejo.spec rpm/rpmbuild/SPECS/forgejo.spec
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp forgejo-${project_version}-linux-${ARCH} rpm/rpmbuild/SOURCES/forgejo
  sudo /bin/cp services/forgejo.service rpm/rpmbuild/SOURCES
  sudo /bin/cp forgejo/forgejo.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp forgejo/config rpm/rpmbuild/SOURCES
}