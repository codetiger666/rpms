#!/bin/bash

program_init(){
  cd /opt
  sudo git clone https://github.com/nicholaschiasson/ngx_upstream_jdomain.git
  sudo git clone https://github.com/GUI/nginx-upstream-dynamic-servers.git
  cd $GITHUB_WORKSPACE
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/systemctl-scripts/nginx.service > nginx.service
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/default.conf > default.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/nginx.conf > nginx.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/stream.conf.example > stream.conf.example
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/ssl.conf.example > ssl.conf.example
  sudo /bin/cp nginx.service openresty/debian/
  sudo /bin/cp default.conf openresty/debian/
  sudo /bin/cp nginx.conf openresty/debian/
  sudo /bin/cp stream.conf.example openresty/debian/
  sudo /bin/cp ssl.conf.example openresty/debian/
  sudo wget https://openresty.org/download/openresty-${project_version}.tar.gz
  sudo mkdir -p /opt/deb_build
  sudo /bin/cp openresty-${project_version}.tar.gz /opt/deb_build/openresty_${project_version}.orig.tar.gz
  sudo tar -xzf openresty-${project_version}.tar.gz -C /opt/deb_build/
  sudo /bin/cp -r openresty/debian/ /opt/deb_build/openresty-${project_version}/debian
  cat > changelog << EOF
openresty (${project_version}-1) stable; urgency=medium

  * Auto-built OpenResty ${project_version} with jdomain and dynamic-servers modules

 -- codetiger666 <admin@111179.xyz>  $(date -R)
EOF
  sudo /bin/cp changelog /opt/deb_build/openresty-${project_version}/debian/changelog
  sudo chmod +x /opt/deb_build/openresty-${project_version}/debian/rules
}