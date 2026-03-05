program_init(){
  sudo sed -i "s/codetiger_version/$(echo "$project_version" | sed -E 's/^RELEASE\.//; s/Z$//; s/T//; s/-//g')/g" specs/minio.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://github.com/pgsty/minio/releases/download/${project_version}/minio_$(echo "$project_version" | sed -E 's/^RELEASE\.//; s/Z$//; s/T//; s/-//g').0.0_linux_${ARCH}.tar.gz -O mini.tar.gz
  sudo mkdir -p minioBin
  sudo tar -xf mini.tar.gz -C minioBin
  sudo /bin/cp minio/minio.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp minioBin/minio rpm/rpmbuild/SOURCES/minio
  sudo /bin/cp minio/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/minio.spec rpm/rpmbuild/SPECS/minio.spec
  sudo /bin/cp services/minio.service rpm/rpmbuild/SOURCES
}