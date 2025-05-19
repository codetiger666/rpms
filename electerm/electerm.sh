#!/bin/bash
# 应用名称
APP_NAME=electerm
# 应用运行目录
PROGRAM_PATH=$(dirname "$(realpath "$0")")

source $PROGRAM_PATH/config

find_run_command() {
    ps -ef | grep ${APP_NAME} | grep -v $0 | grep -vE "ps|grep|systemd --user|sd-pam|awk|xargs|systemctl"
}

get_status() {
    if find_run_command > /dev/null ; then
        return 1
    else
        return 0
    fi
}

case "$1" in
start)
    get_status
    if [ $? -eq 1 ]; then
        echo "${APP_NAME} is runing..."
        exit 0
    fi
    cd ${PROGRAM_PATH}/app
    NODE_ENV=production PORT=${WORK_PORT} DB_PATH=${WORK_DATA} HOST=${WORK_HOST} SERVER_SECRET=${APP_SECRET} SERVER_PASS=${APP_PASS} ENABLE_AUTH=1 node ${PROGRAM_PATH}/app/src/app/app.js --$APP_NAME > $PROGRAM_PATH/$APP_NAME.log 2>&1 &
    echo $! > $PROGRAM_PATH/$APP_NAME.pid
    ;;
stop)
    get_status
    if [ $? -eq 1 ]; then
        find_run_command | awk '{print $2}' | xargs -I {} kill {}
        rm $PROGRAM_PATH/$APP_NAME.pid
        rm $PROGRAM_PATH/$APP_NAME.log
    fi
    ;;
status)
    get_status
    if [ $? -eq 1 ]; then
        echo "${APP_NAME} is runing..."
    else
        echo "${APP_NAME} is not runing..."
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