#!/bin/sh
tomcats=4
TOMCATGROUPHOME='/usr/local/tomcatgroup/LYWGroup'
function killTomcat()
{
   if [ $1 -ge 10 ] ; then
        tomcatInstance=tomcatA$1
   else
        tomcatInstance=tomcatA0$1
   fi
   tomcat=$TOMCATGROUPHOME/$tomcatInstance

    pidfile=/var/run/jsvc_${tomcatInstance}.pid
    if [ -e ${pidfile} ] ; then 
        echo "kill $tomcatInstance ..."
     	# kill -9 $(cat ${pidfile})
	${tomcat}/bin/jsvc -stop -pidfile $pidfile org.apache.catalina.startup.Bootstrap
        #echo "sleep 5s"
        #sleep 5s
    else
        echo "未找到${tomcatInstance}实例或已经停止，请检查！" 
    fi
}
if [ -n "$1" ] ; then
    killTomcat ${1}     
else   
    int=1
    while(( ${int} <= ${tomcats}))
    do
        killTomcat ${int}
        let "int++"
    done
fi
