program_init(){
  sudo sed -i "s/codetiger_version/$(echo "$project_version" | sed -E 's/^RELEASE\.//; s/Z$//; s/T//; s/-//g')/g" specs/silo.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://github.com/pgsty/minio/releases/download/${project_version}/silo_$(echo "$project_version" | sed -E 's/^RELEASE\.//; s/Z$//; s/T//; s/-//g').0.0_linux_${ARCH}.tar.gz -O silo.tar.gz
  sudo mkdir -p siloBin
  sudo tar -xf silo.tar.gz -C siloBin
  sudo /bin/cp silo/silo.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp siloBin/silo rpm/rpmbuild/SOURCES/silo
  sudo /bin/cp silo/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/silo.spec rpm/rpmbuild/SPECS/silo.spec
  sudo /bin/cp services/silo.service rpm/rpmbuild/SOURCES
}