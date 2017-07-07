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
	&& mkdir ~/app/ && mkdir ~/logs/ && mkdir ~/.fonts
ENV LANG C.UTF-8
RUN pip3 install --upgrade pip
ADD PymesPlus_V2/pymes-plus-api/requirements.txt /root/app/requirements.txt
RUN pip3 install -r ~/app/requirements.txt
ADD run.sh /root/app/
ADD .env /root/app/
ADD PymesPlus_V2/pymes-plus-api/ /root/app/
RUN cp ~/app/fonts/* ~/.fonts/ && chmod +x ~/app/run.sh

EXPOSE 5000

ENTRYPOINT  ["/root/app/run.sh"]  

CMD ["bash"]
