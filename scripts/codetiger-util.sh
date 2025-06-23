program_init(){
  sudo /bin/cp codetiger-util/common.sh rpm/rpmbuild/SOURCES
  sudo /bin/cp specs/codetiger-util.spec rpm/rpmbuild/SPECS/codetiger-util.spec
}