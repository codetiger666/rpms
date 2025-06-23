#!/bin/bash
# 应用名称
APP_NAME=onedrive
# 应用运行目录
PROGRAM_PATH=$(dirname "$(realpath "$0")")

case "$1" in
start)
    if /usr/local/codetiger-util/common.sh findRun $APP_NAME $0 > /dev/null ; then
        echo "${APP_NAME} is runing..."
        exit 0
    fi
    ${APP_NAME} --confdir $PROGRAM_PATH/conf -m > $PROGRAM_PATH/$APP_NAME.log 2>&1 &
    echo $! > $PROGRAM_PATH/$APP_NAME.pid
    ;;
stop)
    if /usr/local/codetiger-util/common.sh findRun $APP_NAME $0 > /dev/null ; then
        /usr/local/codetiger-util/common.sh findRun ${APP_NAME} $0 | awk '{print $1}' | xargs -I {} kill {}
        rm $PROGRAM_PATH/$APP_NAME.pid
    fi
    ;;
status)
    /usr/local/codetiger-util/common.sh status ${APP_NAME} $0
    ;;
restart)
    $0 stop
    sleep 5
    $0 start
    ;;
*)
  echo "Usage: $0 {start|stop|status|restart}"
esac
# 正常退出程序
exit 0