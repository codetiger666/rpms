program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/octopus.spec
  
  # 根据架构确定下载URL
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=x86_64
  elif [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  # 从GitHub发布页面下载octopus二进制文件
  wget https://github.com/bestruirui/octopus/releases/download/v${project_version}/octopus-linux-${ARCH}.zip -O octopus.zip
  sudo mkdir -p octopusDir
  sudo unzip octopus.zip -d octopusDir
  sudo /bin/cp octopus/octopus.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp octopusDir/octopus rpm/rpmbuild/SOURCES/octopus
  sudo /bin/cp octopus/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/octopus.spec rpm/rpmbuild/SPECS/octopus.spec
  sudo /bin/cp services/octopus.service rpm/rpmbuild/SOURCES
}