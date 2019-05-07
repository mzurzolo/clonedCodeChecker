FROM oraclelinux:7

COPY . /home/travis

RUN yum -y install oraclelinux-release-el7 oracle-softwarecollection-release-el7
RUN yum -y install python36 python36-pip maven30-maven
RUN cd /home/travis/clonedcodecheckerplugin ; /opt/rh/maven30/root/usr/bin/mvn dependency:purge-local-repository clean validate initialize verify
RUN cd /home/travis ; pip install .
