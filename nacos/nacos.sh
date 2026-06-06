#!/usr/bin/bash
PROGRAM_PATH=$(dirname "$(realpath "$0")")
source $PROGRAM_PATH/config
JAVA_HOME=/usr/local/jdk/21
JAVA_OPT="-Xms${JVM_XMS} -Xmx${JVM_XMX} \
-Dnacos.standalone=true -Dnacos.home=${PROGRAM_PATH} \
-Dloader.path=${PROGRAM_PATH}/plugins \
--add-opens=java.base/java.lang=ALL-UNNAMED \
--add-opens=java.base/java.lang.reflect=ALL-UNNAMED \
--add-opens=java.base/java.util=ALL-UNNAMED"
PROGRAM_OPT="--logging.config=${PROGRAM_PATH}/logback.xml \
--spring.config.additional-location=file:$PROGRAM_PATH/ \
nacos.nacos -m standalone"
APP_NAME=nacos-server

case "$1" in
start)
    if [ -f "$PROGRAM_PATH/$APP_NAME.pid" ]; then
        if  ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
            echo "${APP_NAME} is runing..."
            exit 0
        fi
    fi
    cd $PROGRAM_PATH
    ${JAVA_HOME}/bin/java ${JAVA_OPT} -jar ${APP_NAME}.jar ${PROGRAM_OPT} > ${PROGRAM_PATH}/${APP_NAME}.log 2>&1 &
    echo $! > $PROGRAM_PATH/$APP_NAME.pid
    ;;
stop)
    if [ -f "$PROGRAM_PATH/$APP_NAME.pid" ]; then
        if  ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
            ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep | awk '{print $2}' | xargs -I {} kill {}
            rm $PROGRAM_PATH/$APP_NAME.pid
        fi
    fi
    ;;
status)
    if [ -f "$PROGRAM_PATH/$APP_NAME.pid" ]; then
        if ps -ef | grep $(cat $PROGRAM_PATH/$APP_NAME.pid) | grep -v grep > /dev/null ; then
            echo "$APP_NAME is runing..."
        else
            echo "$APP_NAME is not runing..."
        fi
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