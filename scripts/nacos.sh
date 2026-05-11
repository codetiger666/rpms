program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/nacos.spec
  wget https://github.com/alibaba/nacos/releases/download/${project_version}/nacos-server-${project_version}.tar.gz -O nacos-server-${project_version}.tar.gz
  nacos_api_legacy_adapter_tag_version=$(curl -sfL "https://api.github.com/repos/nacos-group/nacos-api-legacy-adapter/releases/latest" | jq -r '.tag_name')
  nacos_api_legacy_adapter_version=$(echo ${nacos_api_legacy_adapter_tag_version} | awk -F. '{print $1"."$2"."$3}')
  wget https://github.com/nacos-group/nacos-api-legacy-adapter/releases/download/${nacos_api_legacy_adapter_tag_version}/nacos-api-legacy-adapter-${nacos_api_legacy_adapter_version}.jar -O nacos-api-legacy-adapter-${nacos_api_legacy_adapter_version}.jar
  tar -xf nacos-server-${project_version}.tar.gz
  sudo /bin/cp nacos/nacos.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp -ra nacos/plugins rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos-api-legacy-adapter-${nacos_api_legacy_adapter_version}.jar rpm/rpmbuild/SOURCES/plugins
  sudo /bin/cp nacos/target/nacos-server.jar rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/application.properties rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/logback.xml rpm/rpmbuild/SOURCES
  sudo /bin/cp nacos/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/nacos.spec rpm/rpmbuild/SPECS/nacos.spec
  sudo /bin/cp services/nacos.service rpm/rpmbuild/SOURCES
}