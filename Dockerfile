FROM centos:7

WORKDIR /app

COPY . /app

CMD ["ls", 'laR']
