program_init(){
  sudo sed -i "s/codetiger_version/${project_version}/g" specs/xxl-job-admin.spec
  wget https://github.com/codetiger666/xxl-job/releases/download/${project_version}/xxl-job-admin-${project_version}.jar -O xxl-job-admin.jar
  sudo /bin/cp xxl-job-admin/xxl-job-admin.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp xxl-job-admin.jar rpm/rpmbuild/SOURCES
  sudo /bin/cp xxl-job-admin/config rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/xxl-job-admin.spec rpm/rpmbuild/SPECS/xxl-job-admin.spec
  sudo /bin/cp services/xxl-job-admin.service rpm/rpmbuild/SOURCES
}