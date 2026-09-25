#!/bin/bash

program_init(){
  cd $GITHUB_WORKSPACE
  sudo /bin/cp services/redis.service redis/debian/
  wget https://github.com/redis/redis/archive/refs/tags/${project_version}.tar.gz -O redis-${project_version}.tar.gz
  sudo mkdir -p /opt/deb_build
  sudo tar -xzf redis-${project_version}.tar.gz -C /opt/deb_build/
  sudo /bin/cp -r redis/debian/ /opt/deb_build/redis-${project_version}/debian
  sudo /bin/cp redis-${project_version}.tar.gz /opt/deb_build/redis_${project_version}.orig.tar.gz
  cat > changelog << EOF
redis (${project_version}-1) stable; urgency=medium

  * Auto-built Redis ${project_version}

 -- codetiger666 <admin@111179.xyz>  $(date -R)
EOF
  sudo /bin/cp changelog /opt/deb_build/redis-${project_version}/debian/changelog
  sudo chmod +x /opt/deb_build/redis-${project_version}/debian/rules
}