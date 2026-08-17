OPENSSL_VERSION=$(get_latest_version "release" "openssl/openssl")

program_init(){
  sudo sed -i "s/codetiger_openssl_version/$(echo $OPENSSL_VERSION | sed 's/openssl-//' )/g" openssh/debian/rules
  sudo /bin/cp services/sshd.service openssh/debian/
  sudo /bin/cp openssh/sshd_config openssh/debian/
  wget https://github.com/openssh/openssh-portable/archive/refs/tags/V_$(echo ${project_version} | sed 's/\./_/g').tar.gz
  wget https://github.com/openssl/openssl/releases/download/${OPENSSL_VERSION}/${OPENSSL_VERSION}.tar.gz
  sudo mkdir -p /opt/deb_build
  tar -xf V_$(echo ${project_version} | sed 's/\./_/g').tar.gz
  mv openssh-portable-V_$(echo ${project_version} | sed 's/\./_/g') openssh-${project_version}
  tar -zcvf openssh-${project_version}.tar.gz openssh-${project_version}/
  sudo tar -xzf openssh-${project_version}.tar.gz -C /opt/deb_build/
  sudo tar -xzf ${OPENSSL_VERSION}.tar.gz -C /opt/deb_build/openssh-${project_version}
  ls -l /opt/deb_build/openssh-${project_version}/${OPENSSL_VERSION}
  sudo /bin/cp -r openssh/debian/ /opt/deb_build/openssh-${project_version}/debian
  sudo /bin/cp openssh-${project_version}.tar.gz /opt/deb_build/openssh_${project_version}.orig.tar.gz
  cat > changelog << EOF
openssh (2:${project_version}-1) stable; urgency=medium

  * Auto-built OpenSSH ${project_version}

 -- codetiger666 <admin@111179.xyz>  $(date -R)
EOF
  sudo /bin/cp changelog /opt/deb_build/openssh-${project_version}/debian/changelog
  sudo chmod +x /opt/deb_build/openssh-${project_version}/debian/rules
}
