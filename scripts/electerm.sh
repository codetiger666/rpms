program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/electerm.spec
  git clone https://github.com/electerm/electerm-web.git --dept=1 electerm-${project_version}
  tar -zcvf electerm-${project_version}.tar.gz electerm-${project_version}
  sudo /bin/cp specs/electerm.spec rpm/rpmbuild/SPECS/electerm.spec
  sudo /bin/cp electerm-${project_version}.tar.gz rpm/rpmbuild/SOURCES
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp electerm/electerm.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp electerm/config rpm/rpmbuild/SOURCES
  sudo /bin/cp services/electerm.service rpm/rpmbuild/SOURCES
}