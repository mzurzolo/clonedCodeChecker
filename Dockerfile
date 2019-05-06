FROM oraclelinux:7

yum -y install python36 python36-setuptools python34 python34-setuptools devtoolset-4-eclipse

COPY . /home/travis
