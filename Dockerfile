FROM oraclelinux:7

COPY . /home/travis

RUN yum -y install oracle-software-collections-release python36 python36-pip python34 python34-pip rh-eclipse46
RUN ls -la home/travis
