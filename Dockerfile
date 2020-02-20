FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential openssl libpcre3 libpcre3-dev
COPY . /passwd_manager
WORKDIR /passwd_manager
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ./generate-certificate.sh
CMD ./setup.sh