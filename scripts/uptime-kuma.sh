program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/uptime-kuma.spec
  wget https://github.com/louislam/uptime-kuma/archive/refs/tags/${project_version}.tar.gz -O uptime-kuma-${project_version}.tar.gz
  sudo /bin/cp specs/uptime-kuma.spec rpm/rpmbuild/SPECS/uptime-kuma.spec
  sudo /bin/cp uptime-kuma-${project_version}.tar.gz rpm/rpmbuild/SOURCES
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp uptime-kuma/uptime-kuma.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp uptime-kuma/config rpm/rpmbuild/SOURCES
  sudo /bin/cp services/uptime-kuma.service rpm/rpmbuild/SOURCES
}