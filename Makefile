#############################################################################
# Description:
# ------------
# This is an easily makefile file. The purpose is to
# provide an instant building by SoftPymes aplication
#
# Make Target:
# ------------
# init:
# 		run api server
#
# test:
#		run unit tests
#
# doc
#		generate API documentation
#
#############################################################################

build:
	rm -rf ./backend/PymesPlus_V2/
	mkdir ./backend/PymesPlus_V2/
	cp -r ./PymesPlus_V2/pymes-plus-api/ ./backend/PymesPlus_V2/
	cd ./backend/; \
	docker build -t softpymes-ubuntu-pymesplus_backend:v1 . 

run:
	docker run -p 5000:5000 -v /Users/produccion2/workspace/docker/backend/logs/:/root/logs/ -d softpymes-ubuntu-pymesplus_backend:v1