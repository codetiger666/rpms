program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/nacos.spec
  wget https://github.com/alibaba/nacos/releases/download/${project_version}/nacos-server-${project_version}.tar.gz -O nacos-server-${project_version}.tar.gz
  tar -xf nacos-server-${project_version}.tar.gz
  sudo /bin/cp nacos/nacos.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/target/nacos-server.jar rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/application.properties rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/logback.xml rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/nacos.spec rpm/rpmbuild/SPECS/nacos.spec
  sudo /bin/cp services/nacos.service rpm/rpmbuild/SOURCES
}