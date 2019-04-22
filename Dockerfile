FROM centos:7

WORKDIR /app

COPY . /app

ENTRYPOINT [ "pwd" ]
CMD ["ls", 'laR']
