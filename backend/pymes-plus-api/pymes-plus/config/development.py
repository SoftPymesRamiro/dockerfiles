# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# TEST Auth module
#
# To execute this test run python auth_test.py on 
# the Terminal. 
# Reading the defined test you'll see that we should
# expect
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


import os

username = "root"
password = "PymesDBPSW1"
host = "192.168.80.70"
port = "3306"
database = 'pymesplusdb'

basedir = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(basedir, '../data-dev.sqlite')

DEBUG = True
IGNORE_AUTH = True
SECRET_KEY = 'top-secret!'
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#                           'sqlite:///' + db_path

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
        username=username,
        password=password,
        host=host,
        port=port,
        database=database
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
