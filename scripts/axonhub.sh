program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/axonhub.spec
  
  # 根据架构确定下载URL
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  elif [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  
  # 从GitHub发布页面下载axonhub二进制文件
  wget https://github.com/looplj/axonhub/releases/download/v${project_version}/axonhub_${project_version}_linux_${ARCH}.zip -O axonhub.zip
  sudo mkdir -p axonhubDir
  sudo unzip axonhub.zip -d axonhubDir  
  sudo /bin/cp axonhub/axonhub.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp axonhubDir/axonhub rpm/rpmbuild/SOURCES/axonhub
  sudo /bin/cp axonhub/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/axonhub.spec rpm/rpmbuild/SPECS/axonhub.spec
  sudo /bin/cp services/axonhub.service rpm/rpmbuild/SOURCES
}