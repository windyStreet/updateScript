#!/bin/sh
tomcats=4 #tomcat实例数
function startTomcat(){
   if [ $1 -ge 10 ] ; then
	tomcatInstance=tomcatA$1
   else
	tomcatInstance=tomcatA0$1
   fi
   tomcat=/usr/local/tomcatgroup/LYWGroup/$tomcatInstance
   if [ -e ${tomcat} ]
   then
      echo "start $tomcatInstance ..."
      ${tomcat}/bin/jsvc -user tomcat -home /usr/local/jdk -Dcatalina.home=${tomcat}/ -Dcatalina.base=${tomcat}/ -Djava.io.tmpdir=${tomcat}/temp -Dfile.encoding=UTF-8 -Djava.net.preferIPv4Stack=true -Xms256m -Xmx3072m -Xgc:gencon -Xgcprio:pausetime -XpauseTarget200ms -XXkeepAreaRatio=50 -XXgcTrigger:10 -XXnoSystemGC -Xss128k -Djava.awt.headless=true -wait 10 -pidfile /var/run/jsvc_${tomcatInstance}.pid -outfile ${tomcat}/logs/catalina-$(date +"%Y_%m_%d_%H_%M_%S").out -cp /usr/local/jdk/lib/tools.jar:${tomcat}/bin/commons-daemon.jar:${tomcat}/bin/tomcat-juli.jar:${tomcat}/bin/bootstrap.jar org.apache.catalina.startup.Bootstrap &
  else 
     echo "未找到${tomcatInstance}实例，请检查是否正确！"
  fi
}
if [ -n "$1" ] 
then
   startTomcat $1
else
   int=1
   while(( $int<=$tomcats ))
   do
     startTomcat ${int}
     echo "sleep 3s"
     sleep 3s
     let "int++"
   done
fi
