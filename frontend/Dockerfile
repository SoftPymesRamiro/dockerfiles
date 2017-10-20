# Dockerfile para la creacion de imagen para un entorno python3 para correr pymesPlusV2 sobre ubuntu 16.04 LTS
FROM node:boron
LABEL maintainer="produccion10 <produccion10@softpymes.com.co>"
RUN apt-get update && apt install -y \
    nginx && mkdir ~/logs/ 

RUN npm install -g grunt-cli webpack apidoc

WORKDIR /usr/src/app

RUN git clone https://a7a3b81ab728465a6b54257f589f1d1f51b311b0@github.com/SoftPymesJavier/PymesPlus_V2
RUN chmod 600 /usr/src/app/PymesPlus_V2/
# RUN /usr/src/app/PymesPlus_V2 git checkout origin develop 
# RUN rm -rf ./PymesPlus_V2/pymes-plus-api/

# ADD PymesPlus_V2/package.json .
# RUN npm install

# ADD default-nginx /etc/nginx/sites-available/default
EXPOSE 80

# ADD PymesPlus_V2/ .
# ADD app-constant.js ./WebClient/components/app-constant.js

# RUN webpack --progress

CMD /usr/sbin/nginx -g "daemon off;"
