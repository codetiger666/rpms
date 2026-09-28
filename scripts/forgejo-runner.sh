program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/forgejo-runner.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://code.forgejo.org/forgejo/runner/releases/download/v${project_version}/forgejo-runner-${project_version}-linux-${ARCH} -O forgejo-runner-bin
  sudo chmod +x forgejo-runner-bin
  sudo /bin/cp forgejo-runner-bin rpm/rpmbuild/SOURCES/forgejo-runner
  sudo /bin/cp forgejo-runner/config rpm/rpmbuild/SOURCES
  sudo /bin/cp forgejo-runner/forgejo-runner.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp services/forgejo-runner.service rpm/rpmbuild/SOURCES
}