program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/curl.spec
  wget https://curl.se/download/curl-${project_version}.tar.gz
  sudo /bin/cp specs/curl.spec rpm/rpmbuild/SPECS/curl.spec
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp curl-${project_version}.tar.gz rpm/rpmbuild/SOURCES/curl-${project_version}.tar.gz
}