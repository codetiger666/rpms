#!/bin/bash

program_init(){
  cd $GITHUB_WORKSPACE
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/systemctl-scripts/nginx.service > nginx.service
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/default.conf > default.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/nginx.conf > nginx.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/stream.conf.example > stream.conf.example
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/ssl.conf.example > ssl.conf.example
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/proxy.conf > proxy.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/websocket.conf > websocket.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/real_ip_cloudflare.conf > real_ip_cloudflare.conf
  sudo curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/ssl.conf > ssl.conf
  sudo /bin/cp nginx.service nginx/debian/
  sudo /bin/cp default.conf nginx/debian/
  sudo /bin/cp nginx.conf nginx/debian/
  sudo /bin/cp stream.conf.example nginx/debian/
  sudo /bin/cp ssl.conf.example nginx/debian/
  sudo /bin/cp proxy.conf nginx/debian/
  sudo /bin/cp websocket.conf nginx/debian/
  sudo /bin/cp real_ip_cloudflare.conf nginx/debian/
  sudo /bin/cp ssl.conf nginx/debian/
  sudo wget https://github.com/nginx/nginx/releases/download/release-${project_version}/nginx-${project_version}.tar.gz
  sudo mkdir -p /opt/deb_build
  sudo /bin/cp nginx-${project_version}.tar.gz /opt/deb_build/nginx_${project_version}.orig.tar.gz
  sudo tar -xzf nginx-${project_version}.tar.gz -C /opt/deb_build/
  sudo /bin/cp -r nginx/debian/ /opt/deb_build/nginx-${project_version}/debian
  cat > changelog << EOF
nginx (100:${project_version}-1) stable; urgency=medium

  * Auto-built nginx ${project_version}

 -- codetiger666 <admin@111179.xyz>  $(date -R)
EOF
  sudo /bin/cp changelog /opt/deb_build/nginx-${project_version}/debian/changelog
  sudo chmod +x /opt/deb_build/nginx-${project_version}/debian/rules
}