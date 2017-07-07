#!/bin/bash -l
#$ -S /bin/bash
echo $1

if [ $1 == "build" ]; then
    echo "Obteniendo la ultima versión"
    cd PymesPlus_V2
    git pull origin develop
    cd ..

    echo "En contrucción backend"
    rm -rf backend/PymesPlus_V2/
	mkdir backend/PymesPlus_V2/
	cp -r PymesPlus_V2/pymes-plus-api/ ./backend/PymesPlus_V2/pymes-plus-api/
	cd backend/
	docker build -t softpymes-ubuntu-pymesplus_backend:v1 . 
    cd ..
    rm -rf backend/PymesPlus_V2/
    echo "Contenedor Backend Contruido"
    
    echo "En contrucción Frontend"
    rm -rf frontend/PymesPlus_V2/
    mkdir frontend/PymesPlus_V2/
    cp -r PymesPlus_V2/ frontend/PymesPlus_V2/
    rm -rf frontend/PymesPlus_V2/pymes-plus-api/
    cd frontend/
    docker build -t softpymes-ubuntu-pymesplus_frontend:v1 .
    cd ..
    rm -rf frontend/PymesPlus_V2/
    echo "Contenedor frontend Contruido"

    echo "iniciando..."
    docker run -p 5000:5000 -v /Users/produccion2/workspace/docker/backend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_backend:v1
    docker run -p 80:80 -v /Users/produccion2/workspace/docker/frontend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_frontend:v1 bash
fi  

if [ $1 == "build_back" ]; then

    echo "En contrucción backend"
    rm -rf backend/PymesPlus_V2/
	mkdir backend/PymesPlus_V2/
	cp -r PymesPlus_V2/pymes-plus-api/ ./backend/PymesPlus_V2/pymes-plus-api/
	cd backend/
	docker build -t softpymes-ubuntu-pymesplus_backend:v1 . 
    cd ..
    rm -rf backend/PymesPlus_V2/
    echo "Contenedor Backend Contruido"

    echo "iniciando..."
    docker run -p 5000:5000 -v /Users/produccion2/workspace/docker/backend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_backend:v1

fi

if [ $1 == "build_front" ]; then
    echo "En contrucción Frontend"
    rm -rf frontend/PymesPlus_V2/
    mkdir frontend/PymesPlus_V2/
    cp -r PymesPlus_V2/ frontend/PymesPlus_V2/
    rm -rf frontend/PymesPlus_V2/pymes-plus-api/
    cd frontend/
    docker build -t softpymes-ubuntu-pymesplus_frontend:v1 .
    cd ..
    rm -rf frontend/PymesPlus_V2/
    echo "Contenedor frontend Contruido"

    echo "iniciando..."
    docker run -p 80:80 -v /Users/produccion2/workspace/docker/frontend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_frontend:v1 bash
fi 

if [ $1 == "run" ]; then
    echo "Corriendo"
    docker run -p 5000:5000 -v /Users/produccion2/workspace/docker/backend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_backend:v1
    docker run -p 80:80 -v /Users/produccion2/workspace/docker/frontend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_frontend:v1 bash
fi
 

if [ $1 == "clear" ]; then
    echo "clearing"
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)
fi
 