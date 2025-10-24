program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/eureka.spec
  wget https://github.com/codetiger666/eureka-server/releases/download/${project_version}/eureka-server.jar -O eureka-server.jar
  sudo /bin/cp eureka/eureka.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp eureka-server.jar rpm/rpmbuild/SOURCES
  sudo /bin/cp eureka/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/eureka.spec rpm/rpmbuild/SPECS/eureka.spec
  sudo /bin/cp services/eureka.service rpm/rpmbuild/SOURCES
}