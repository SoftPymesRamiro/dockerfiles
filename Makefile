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

init:
	rm -rf PymesPlus_V2/
	git clone https://github.com/SoftPymesJavier/PymesPlus_V2.git
	cd ./PymesPlus_V2/
	git checkout develop

build:
	rm -rf ./backend/PymesPlus_V2/
	cp -r ./PymesPlus_V2/pymes-plus-api/ ./backend/pymes-plus-api/

	rm -rf ./frontend/PymesPlus_V2/
	mkdir ./frontend/PymesPlus_V2/
	cp -r ./PymesPlus_V2/ ./frontend/PymesPlus_V2/
	rm -rf ./backend/PymesPlus_V2/pymes-plus-api/

	docker-compose build

	rm -rf backend/pymes-plus-api/
	rm -rf frontend/PymesPlus_V2/

run:
	docker-compose up