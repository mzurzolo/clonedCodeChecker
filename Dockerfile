FROM oraclelinux:7

COPY . /home/travis

RUN yum -y install oracle-softwarecollection-release-el7 oraclelinux-developer-release-el7 oraclelinux-release-el7 oracle-softwarecollection-release-el7 oracle-epel-release-el7 oracle-release
RUN yum -y install python36 python36-pip python34 python34-pip devtoolset-4-eclipse rh-maven35 rh-eclipse46

RUN mvn -f /home/travis/clonedcodecheckerplugin dependency:purge-local-repository clean validate initialize verify
RUN pip install /home/travis
