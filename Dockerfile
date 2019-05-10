FROM oraclelinux:7

COPY . /build/

RUN yum -y install oraclelinux-release-el7 oracle-softwarecollection-release-el7 deltarpm
RUN yum -y install python36
RUN yum -y install python36-pip
RUN yum -y install maven30-maven
RUN yum -y install devtoolset-4-eclipse
RUN scl enable maven30 sh && cd /build/clonedcodecheckerplugin/ && source /root/.bashrc && mvn clean package ; cd .. ; python36 setup.py install
