FROM centos:7

COPY . /home/project
RUN yum -y install epel-release
RUN yum -y install python36
RUN ls /home/project
