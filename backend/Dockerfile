# Dockerfile para la creacion de imagen para un entorno python3 para correr pymesPlusV2 sobre ubuntu 16.04 LTS
FROM ubuntu:16.04
MAINTAINER produccion10 <produccion10@softpymes.com.co>
RUN apt-get update && apt install -y \
	python3 \
	python3-pip \
	python3-dev \
	build-essential \
	git git-core \
	locales \
	&& mkdir ~/logs/ && mkdir ~/.fonts
ENV LANG C.UTF-8

WORKDIR /root/app/

RUN pip3 install --upgrade pip
ADD pymes-plus-api/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD . .
RUN cp -R pymes-plus-api/fonts/* ~/.fonts/ 

EXPOSE 5000
CMD [ "python3", "/root/app/pymes-plus-api/pymes-plus/run.py" ]