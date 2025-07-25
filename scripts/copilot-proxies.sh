program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/copilot-proxies.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://gitee.com/ripperTs/github-copilot-proxies/releases/download/v${project_version}/copilot-proxies-linux-${ARCH} -O copilot-proxies-bin
  sudo /bin/cp specs/copilot-proxies.spec rpm/rpmbuild/SPECS/copilot-proxies.spec
  mkdir rpm/rpmbuild/SOURCES -p
  sudo /bin/cp copilot-proxies-bin rpm/rpmbuild/SOURCES/copilot-proxies
  sudo /bin/cp services/copilot-proxies.service rpm/rpmbuild/SOURCES
  sudo /bin/cp copilot-proxies/copilot-proxies.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp copilot-proxies/.env rpm/rpmbuild/SOURCES
}