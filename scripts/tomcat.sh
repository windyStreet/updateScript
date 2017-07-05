#!/bin/sh

method=""
node=""
projectname=""
version=""
updatetime=""
jdk=/usr/local/jdk
#-m stop -i node
#-m start -i node
#-m killpid -i node
#-m replaceResource -p projectname -t 20170413 -v 19

TOMCATGROUPHOME=/usr/local/tomcatgroup
backuppath=/datafile/fileshare/YXYBBJAR
projectpath=/usr/longrise/LEAP/YXYBB/WEB-INF
projcetLibPath=${projectpath}/lib
projectResourceLibPath=${projectpath}/ResourceLib
projectResourcesPath=${projectpath}/ResourceLib.TMP/YXYBB/LEAP/
pidfile=""

function check_projectName()
{
    if [ -z "${projectname}" ] || [ "${projectname}" ==  "" ] ; then
        echo "not set the project name"
        echo "add the par : -t project name"
        exit -1
    fi
}

function check_time()
{
    if [ -z "${updatetime}" ] || [ "${updatetime}" ==  "" ] ; then
        echo "not set the update time"
        echo "add the par : -t update time"
        exit -1
    fi
}
function check_version()
{
    if [ -z "${version}" ] || [ "${version}" ==  "" ] ; then
        echo "not set the update version"
        echo "add the par : -v update version"
        exit -1
    fi
}
function check_node()
{
    if [ -z "${node}" ] || [ "${node}" ==  "" ] ; then
        echo "not set the tomcat tag"
        echo "add the par : -i tomcat tag"
        exit -1
    fi
}


function check_pid() {
    if [ -f ${pidfile} ];then
        pid=`cat ${pidfile}`
        if [ -n ${pid} ]; then
            running=`ps -p ${pid}|grep -v "PID TTY" |wc -l`
            return ${running}
        fi
    fi
}

#关闭tomcat
function stop() 
{
    check_node
    if [ ${node} -ge 10 ] ; then
        tomcatInstance=tomcatA${node}
    else
        tomcatInstance=tomcatA0${node}
    fi
    echo "stop ${tomcatInstance}"
    tomcat=${TOMCATGROUPHOME}/${tomcatInstance}
    pidfile=/var/run/jsvc_${tomcatInstance}.pid
    if [ -e ${pidfile} ] ; then
	${tomcat}/bin/jsvc -stop -pidfile ${pidfile} org.apache.catalina.startup.Bootstrap
    else
        echo "未找到${tomcatInstance}实例或已经停止，请检查！"
    fi
}

#启动tomcat
function start()
{
    check_node
    if [ ${node} -ge 10 ] ; then
        tomcatInstance=tomcatA${node}
    else
	tomcatInstance=tomcatA0${node}
    fi

    tomcat=${TOMCATGROUPHOME}/${tomcatInstance}
    echo ${tomcat}
    if [ -e ${tomcat} ] ; then
        echo "start $tomcatInstance ..."
        ${tomcat}/bin/jsvc \
        -user tomcat \
        -home ${jdk} -Dcatalina.home=${tomcat}/ \
        -Dcatalina.base=${tomcat}/ \
        -Djava.io.tmpdir=${tomcat}/temp \
        -Dfile.encoding=UTF-8 \
        -Djava.net.preferIPv4Stack=true \
        -Xms256m \
        -Xmx3072m \
        -Xgc:gencon \
        -Xgcprio:pausetime \
        -XpauseTarget200ms \
        -XXkeepAreaRatio=50 \
        -XXgcTrigger:10 \
        -XXnoSystemGC \
        -Xss128k \
        -Djava.awt.headless=true \
        -wait 10 \
        -pidfile /var/run/jsvc_${tomcatInstance}.pid \
        -outfile ${tomcat}/logs/catalina-$(date +"%Y_%m_%d_%H_%M_%S").out \
        -cp /usr/local/jdk/lib/tools.jar:${tomcat}/bin/commons-daemon.jar:${tomcat}/bin/tomcat-juli.jar:${tomcat}/bin/bootstrap.jar \
        org.apache.catalina.startup.Bootstrap &
    else
        echo "未找到${tomcatInstance}实例，请检查是否正确！"
    fi
}

#替换资源
function replaceResource()
{
    check_version
    check_time

    jar="V1.0.${version}"_"${updatetime}"

    if [ -f "${backuppath}/${jar}.tar" ];then
       echo "OK"
    else
       echo "未找到更新压缩包"${backuppath}/${jar}.tar
       exit 1
    fi
    rm -rf ${backuppath}/${jar}
    echo "正在解压更新包..."
    tar -zxvf ${backuppath}/${jar}.tar -C ${backuppath}
    chmod 755 -R ${backuppath}/${jar}
    \cp -rf ${backuppath}/${jar}/lib/* ${projcetLibPath}
    echo "更新lib成功..."
    \cp -rf ${backuppath}/${jar}/ResourceLib/* ${projectResourceLibPath}
    echo "更新ResourceLib成功..."
    \cp -rf ${backuppath}/${jar}/other/*  ${projectResourcesPath}
    echo "更新Resource静态资源成功..."

}

function killPid()
{
    check_node

    if [ ${node} -ge 10 ] ; then
        tomcatInstance=tomcatA${node}
    else
        tomcatInstance=tomcatA0${node}
    fi

    tomcat=${TOMCATGROUPHOME}/${tomcatInstance}
    pidfile=/var/run/jsvc_${tomcatInstance}.pid

    if [ -f ${pidfile} ];then
      pid=`cat ${pidfile}`
      kill ${pid}
      rm -rf ${pidfile}
    fi

    pidlists=()
    i=0
    num=`ps -ef|grep -v grep |grep ${tomcatInstance}|wc -l`
    if [[ "$num" -ge 1 ]];then
        pidList=`ps -ef|grep -v grep |grep ${tomcatInstance}|awk '{print $2}'`
        for s in ${pid}List
        do
           pidlists[${i}]=${s}
           let i++
        done
        temp=0
        for(( i=0;i<$num;i++)){
          for(( j=i+1;j<$num;j++)){
            if [[ ${pidlists[i]} -lt ${pidlists[j]} ]];then
              temp=${pidlists[i]}
              pidlists[i]=${pidlists[j]}
              pidlists[j]=${temp}
            fi
          }
        }
        for s in ${pidlists[@]}
        do
           kill -9 ${s}
        done
    fi
}

function help()
{
    echo "-m:method[stop,start,killPid,replaceResource,help]"
    echo "-i:tomcat node tag"
    echo "-p:project name"
    echo "-t:time"
    echo "-v:version"
}

while getopts ":m:i:p:t:v:h" opt
do
        case ${opt} in
                h ) help
                    ;;
                m ) method=$OPTARG
                    ;;
                i ) node=$OPTARG
                    ;;
                p ) projectname=$OPTARG
                    ;;
                t ) updatetime=$OPTARG
                    ;;
                v ) version=$OPTARG
                    ;;
                ? ) help
                    exit 1;;
        esac
done

if [ "$method" == "stop" ] ; then
    stop
elif [ "$method" == "start" ] ; then
    start
elif [ "$method" == "killPid" ] ; then
    killPid
elif [ "$method" == "replaceResource" ] ; then
    replaceResource
elif [ "$method" == "help" ] ; then
    help
else
    help
    exit 1
fi
