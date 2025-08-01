#!/bin/bash
PROGRAM_PATH=$(dirname "$(realpath "$0")")
APP_NAME=openlist

source $PROGRAM_PATH/config

case "$1" in
start)
    if  ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
        echo "${APP_NAME} is runing..."
        exit 0
    fi
    cd $WORK_PATH
    ${APP_NAME} server > ${PROGRAM_PATH}/${APP_NAME}.log 2>&1 &
    echo $! > $PROGRAM_PATH/$APP_NAME.pid
    ;;
stop)
    if ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
        ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
        rm $PROGRAM_PATH/$APP_NAME.pid
    fi
    ;;
status)
    if ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
        echo "$APP_NAME is runing..."
    else
        echo "$APP_NAME is not runing..."
    fi
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
