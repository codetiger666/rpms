program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/openlist.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://github.com/OpenListTeam/OpenList/releases/download/v${project_version}/openlist-linux-${ARCH}.tar.gz
  sudo /bin/cp specs/openlist.spec rpm/rpmbuild/SPECS/openlist.spec
  sudo sed -i "s/codetiger_arch/${ARCH}/g" specs/openlist.spec
  sudo /bin/cp openlist-linux-${ARCH}.tar.gz rpm/rpmbuild/SOURCES
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp openlist/openlist.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp openlist/config rpm/rpmbuild/SOURCES
  sudo /bin/cp openlist/config.json rpm/rpmbuild/SOURCES
  sudo /bin/cp services/openlist.service rpm/rpmbuild/SOURCES
}
