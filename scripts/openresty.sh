PERLVERSION=5.32
if [ "${os_release}" -gt "9" ]; then
  PERLVERSION=5.40
fi

program_init(){
  cd rpm
  git clone https://github.com/nicholaschiasson/ngx_upstream_jdomain.git
  git clone https://github.com/GUI/nginx-upstream-dynamic-servers.git
  cd $GITHUB_WORKSPACE
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/systemctl-scripts/nginx.service > nginx.service
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/default.conf > default.conf
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/nginx.conf > nginx.conf
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/stream.conf.example > stream.conf.example
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/ssl.conf.example > ssl.conf.example
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/proxy.conf > proxy.conf
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/websocket.conf > websocket.conf
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/ssl.conf > ssl.conf
  curl https://raw.githubusercontent.com/codetiger666/linux/master/scripts/linux/nginx/real_ip_cloudflare.conf > real_ip_cloudflare.conf
  sudo /bin/cp nginx.service rpm/rpmbuild/SOURCES
  sudo /bin/cp default.conf rpm/rpmbuild/SOURCES
  sudo /bin/cp nginx.conf rpm/rpmbuild/SOURCES
  sudo /bin/cp stream.conf.example rpm/rpmbuild/SOURCES
  sudo /bin/cp ssl.conf.example rpm/rpmbuild/SOURCES
  sudo /bin/cp proxy.conf rpm/rpmbuild/SOURCES
  sudo /bin/cp websocket.conf rpm/rpmbuild/SOURCES
  sudo /bin/cp real_ip_cloudflare.conf rpm/rpmbuild/SOURCES
  sudo /bin/cp ssl.conf rpm/rpmbuild/SOURCES
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/openresty.spec
  sudo sed -i "s/codetiger_perl_version/${PERLVERSION}/g" specs/openresty.spec
  wget https://openresty.org/download/openresty-${project_version}.tar.gz
  sudo /bin/cp openresty-${project_version}.tar.gz rpm/rpmbuild/SOURCES/
}