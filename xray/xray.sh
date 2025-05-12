#!/bin/bash
PROGRAM_PATH=$(dirname "$(realpath "$0")")
APP_NAME=xray
CONF=${PROGRAM_PATH}/config.json

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
    ${APP_NAME} -c $CONF > ${PROGRAM_PATH}/${APP_NAME}.log 2>&1 &
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
    $0 start
    ;;
*)
  echo "Usage: $0 {start|stop|status|restart}"
esac
# 正常退出程序
exit 0