program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/new-api.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=-arm64
  fi
  sudo sed -i "s/codetiger_arch/${ARCH}/g" specs/new-api.spec
  wget https://github.com/QuantumNous/new-api/releases/download/v${project_version}/new-api${ARCH}-v${project_version} -O new-api-bin
  sudo /bin/cp specs/new-api.spec rpm/rpmbuild/SPECS/new-api.spec
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp new-api-bin rpm/rpmbuild/SOURCES/new-api
  sudo /bin/cp services/new-api.service rpm/rpmbuild/SOURCES
  sudo /bin/cp new-api/new-api.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp new-api/.env rpm/rpmbuild/SOURCES
}
