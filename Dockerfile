FROM oraclelinux:7

COPY . /home/travis

RUN yum -y install oraclelinux-release-el7 oracle-softwarecollection-release-el7
RUN yum -y install python36 python36-pip rh-maven35-maven rh-maven35-plexus-classworlds
RUN cd /home/travis/clonedcodecheckerplugin ; /opt/rh/rh-maven35/root/usr/bin/mvn dependency:purge-local-repository clean validate initialize verify
RUN cd /home/travis ; pip install .
