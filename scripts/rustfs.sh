program_init(){
  wget https://github.com/rustfs/rustfs/releases/download/${project_version}/rustfs-linux-${project_arch}-musl-v${project_version}.zip -O rustfs.zip
  sudo sed -i "s/codetiger_version/${project_version//-/.}/g" specs/rustfs.spec
  unzip rustfs.zip -d ./rustfsBinDir
  sudo /bin/cp rustfs/rustfs.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp rustfsBinDir/rustfs rpm/rpmbuild/SOURCES/rustfs
  sudo /bin/cp rustfs/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/rustfs.spec rpm/rpmbuild/SPECS/rustfs.spec
  sudo /bin/cp services/rustfs.service rpm/rpmbuild/SOURCES
}