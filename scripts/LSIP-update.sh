#! /bin/bash
echo "help:可通过传入日期找出该日期内的更新版本"
echo "example：./updatejar-lsip.sh 20160324"
bakdate=`date +%Y%m%d`
echo "请输入更新版本："
read version
#echo "本次构建版本为：$version  $version"_"${bakdate}
backuppath=/datafile/fileshare/LSIPJAR
projectpath=/lstore/LEAP/LSIP/WEB-INF
jar="V1.0.$version"_"${bakdate}"
if [ -n "$1" ]  
then  
    jar="V1.0.$version"_"${1}"  
fi

if [ -f "${backuppath}/${jar}.tar" ];then
   echo "OK"
else
   echo "未找到更新压缩包"${backuppath}/${jar}.tar
   exit 1
fi

rm -rf ${backuppath}/${jar}
echo "正在解压更新包..."
tar -zxvf ${backuppath}/${jar}.tar -C ${backuppath}
chmod 777 -R ${backuppath}/${jar}
\cp -rf ${backuppath}/${jar}/lib/* ${projectpath}/lib
echo "更新lib成功..."
\cp -rf ${backuppath}/${jar}/ResourceLib/* ${projectpath}/ResourceLib
echo "更新ResourceLib成功..."
