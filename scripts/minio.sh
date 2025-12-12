program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/minio.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://dl.min.io/server/minio/release/linux-${ARCH}/archive/minio.RELEASE.2025-04-22T22-12-26Z -O minioBin
  sudo /bin/cp minio/minio.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp minioBin rpm/rpmbuild/SOURCES/minio
  sudo /bin/cp minio/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/minio.spec rpm/rpmbuild/SPECS/minio.spec
  sudo /bin/cp services/minio.service rpm/rpmbuild/SOURCES
}