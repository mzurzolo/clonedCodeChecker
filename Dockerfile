FROM oraclelinux:7

COPY . /home/travis

RUN yum -y install oraclelinux-release-el7 oracle-softwarecollection-release-el7
RUN yum -y install python36 python36-pip maven30-maven

RUN mvn -f /home/travis/clonedcodecheckerplugin dependency:purge-local-repository clean validate initialize verify
RUN pip install /home/travis
