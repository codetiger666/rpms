program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/moontvplus.spec
  git clone https://github.com/mtvpls/MoonTVPlus.git moontvplus-${project_version} --depth 1
  sudo /bin/cp specs/moontvplus.spec rpm/rpmbuild/SPECS/moontvplus.spec
  tar -czvf moontvplus-${project_version}.tar.gz moontvplus-${project_version}
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp moontvplus-${project_version}.tar.gz rpm/rpmbuild/SOURCES
  sudo /bin/cp moontvplus/moontvplus.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp moontvplus/config rpm/rpmbuild/SOURCES
  sudo /bin/cp services/moontvplus.service rpm/rpmbuild/SOURCES
}