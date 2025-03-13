program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/nodejs.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=x64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://nodejs.org/dist/v${project_version}/node-v${project_version}-linux-${ARCH}.tar.gz -O node-v${project_version}-linux-${ARCH}.tar.gz
  tar -xf node-v${project_version}-linux-${ARCH}.tar.gz
  rm -rf node-v${project_version}-linux-${ARCH}/share
  rm -rf node-v${project_version}-linux-${ARCH}/*.md
  rm -rf node-v${project_version}-linux-${ARCH}/LICENSE
  mv node-v${project_version}-linux-${ARCH} nodejs-${project_version}
  tar -zcvf nodejs-${project_version}.tar.gz nodejs-${project_version}
  sudo /bin/cp specs/nodejs.spec rpm/rpmbuild/SPECS/nodejs.spec
  sudo /bin/cp nodejs-${project_version}.tar.gz rpm/rpmbuild/SOURCES
}