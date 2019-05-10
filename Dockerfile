FROM oraclelinux:7

RUN yum -y install oraclelinux-release-el7 oracle-softwarecollection-release-el7 deltarpm
RUN yum -y install python36
RUN yum -y install python36-pip
RUN yum -y install maven30-maven
RUN yum -y install devtoolset-4-eclipse

COPY . /build/

SHELL ["/bin/bash", "-c"]
RUN source scl_source enable maven30 ; \
cd build/clonedcodecheckerplugin ; \
mvn clean package
RUN python36 /build/setup.py install
