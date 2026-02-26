program_init(){
  sudo sed -i "s/codetiger_version/${project_version//-/.}/g" specs/zashboard.spec
  wget https://github.com/Zephyruso/zashboard/releases/download/v${project_version}/dist-cdn-fonts.zip -O zashboard.zip
  unzip zashboard.zip -d ./zashboard
  sudo mkdir -p rpm/rpmbuild/SOURCES/zashboard
  sudo /bin/cp -ra zashboard/dist/* rpm/rpmbuild/SOURCES/zashboard
  sudo /bin/cp specs/zashboard.spec rpm/rpmbuild/SPECS/zashboard.spec
}