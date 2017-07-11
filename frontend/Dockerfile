# Dockerfile para la creacion de imagen para un entorno python3 para correr pymesPlusV2 sobre ubuntu 16.04 LTS
FROM node:boron
MAINTAINER produccion10 <produccion10@softpymes.com.co>
RUN apt-get update && apt install -y \
    nginx && mkdir ~/logs/ 

RUN npm install -g grunt-cli webpack apidoc

WORKDIR /usr/src/app

ADD PymesPlus_V2/package.json .
RUN npm install

ADD default-nginx /etc/nginx/sites-available/default
EXPOSE 80

ADD PymesPlus_V2/ .
ADD app-constant.js ./WebClient/components/app-constant.js
RUN webpack --progress

CMD /usr/sbin/nginx -g "daemon off;"
