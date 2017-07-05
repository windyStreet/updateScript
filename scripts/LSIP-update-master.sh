#! /bin/bash
backuppath=/datafile/fileshare/LSIPJAR
projectpath=/lstore/LEAP/LSIP/WEB-INF

if [ -n "$1" ] ; then
    version=$1
else
   echo "未指定版本"
   return 1
fi

if [ -n "$2" ] ; then
   updatetime=$2
else
    echo "未指定更新时间"
    return 1
fi

jar="V1.0.$version"_"$updatetime"

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
