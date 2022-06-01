FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y nginx gunicorn python3 python3-pip
WORKDIR /opt/dsd
ADD . /opt/dsd
COPY nginx-vhost.conf /etc/nginx/sites-available/default
RUN find . -name requirements.txt -exec pip install -r {} \;
EXPOSE 80
VOLUME /opt/dsd
ENTRYPOINT /opt/dsd/start.sh
