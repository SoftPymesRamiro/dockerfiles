# Dockerfile para la creacion de imagen para un entorno python3 para correr pymesPlusV2 sobre ubuntu 16.04 LTS
FROM node:boron
MAINTAINER produccion10 <produccion10@softpymes.com.co>
RUN apt-get update && apt install -y \
    nginx \
	&& mkdir ~/app/ && mkdir ~/logs/ 

RUN npm install -g grunt-cli webpack apidoc

ADD PymesPlus_V2/package.json /root/app/
RUN cd /root/app/ && npm install

ADD default-nginx /etc/nginx/sites-available/default

ADD PymesPlus_V2/ /root/app/
ADD app-constant.js /root/app/WebClient/components/app-constant.js
ADD run.sh /root/app/
RUN chmod +x ~/app/run.sh

EXPOSE 80
ENTRYPOINT  ["/root/app/run.sh"]  

CMD ["bash"]
