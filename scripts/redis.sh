program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/redis.spec
  sudo /bin/cp specs/redis.spec rpm/rpmbuild/SPECS/redis.spec
  sudo /bin/cp services/redis.service rpm/rpmbuild/SOURCES
  wget https://github.com/redis/redis/archive/refs/tags/${project_version}.tar.gz -O redis-${project_version}.tar.gz
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp redis-${project_version}.tar.gz rpm/rpmbuild/SOURCES/
}