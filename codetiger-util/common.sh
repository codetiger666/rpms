#!/bin/bash

find_run_command() {
    ps -ef | grep -v $0 | grep -v $1 | grep -vE "ps|grep|systemd --user|sd-pam|awk|xargs|systemctl" | awk '{ print $2, $8, $9, $10 }' | grep $2
}

case "$1" in
    findRun)
        find_run_command $3 $2
        ;;
    status)
        if find_run_command $3 $2 > /dev/null ; then
            echo -e "\033[32m${2} is running...\033[0m"
            exit 1
        else
            echo -e "\033[31m${2} is not running...\033[0m"
            exit 0
        fi
        ;;
    *)
        echo -e "请输入正确的参数:"
        echo -e "$0 findRun <应用名称> - 查找运行中的应用进程"
        echo -e "$0 status <应用名称> - 获取应用运行状态"
        exit 1
        ;;
esac