program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/xray.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64-v8a
  fi
  wget https://github.com/XTLS/Xray-core/releases/download/v${project_version}/Xray-linux-${ARCH}.zip -O xray.zip
  unzip -d xray-${project_version} xray.zip
  tar -zcvf xray-${project_version}.tar.gz xray-${project_version}
  sudo /bin/cp specs/xray.spec rpm/rpmbuild/SPECS/xray.spec
  sudo /bin/cp xray-${project_version}.tar.gz rpm/rpmbuild/SOURCES
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp xray/xray.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp xray/config.json rpm/rpmbuild/SOURCES
  sudo /bin/cp services/xray.service rpm/rpmbuild/SOURCES
}