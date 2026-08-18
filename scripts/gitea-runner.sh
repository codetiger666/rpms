program_init(){
  sudo sed -i "s/codetiger_version/$(echo "$project_version" | sed -E 's/^RELEASE\.//; s/Z$//; s/T//; s/-//g')/g" specs/gitea-runner.spec
  ARCH=amd64
  if [ "${project_arch}" = "x86_64" ]; then
    ARCH=amd64
  fi
  if [ "${project_arch}" = "aarch64" ]; then
    ARCH=arm64
  fi
  wget https://gitea.com/gitea/runner/releases/download/v${project_version}/gitea-runner-${project_version}-linux-${ARCH} -O gitea-runner-bin
  sudo chmod +x gitea-runner-bin
  sudo /bin/cp gitea-runner-bin rpm/rpmbuild/SOURCES/gitea-runner
  sudo /bin/cp gitea-runner/config rpm/rpmbuild/SOURCES
  sudo /bin/cp gitea-runner/gitea-runner.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp services/gitea-runner.service rpm/rpmbuild/SOURCES
}