program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/openlist-api.spec
  git clone https://github.com/OpenListTeam/OpenList-APIPages.git openlist-api-${project_version}
  tar -zcvf openlist-api-${project_version}.tar.gz openlist-api-${project_version}
  sudo /bin/cp specs/openlist-api.spec rpm/rpmbuild/SPECS/openlist-api.spec
  sudo /bin/cp openlist-api-${project_version}.tar.gz rpm/rpmbuild/SOURCES
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp openlist-api/openlist-api.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp openlist-api/.env rpm/rpmbuild/SOURCES
  sudo /bin/cp services/openlist-api.service rpm/rpmbuild/SOURCES
}
