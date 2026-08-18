#!/bin/bash

# 应用运行目录
PROGRAM_PATH=$(dirname "$(realpath "$0")")

if pgrep -f 'onedrive --confdir' > /dev/null; then
    echo "当前进程存活" > ${PROGRAM_PATH}/watch.log
else
    echo "当前进程未存活，重新拉起" > ${PROGRAM_PATH}/watch.log
    systemctl restart onedrive
fi