# -*- coding: utf-8 -*-
#########################################################
# Flask create_app() factory.
# 
# This create_app from app with Blueprint (modular flask) 
#
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


import os
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .decorators import json
from dotenv import Dotenv
from .utils import validator

dotenv_path = Dotenv(os.path.join(os.getcwd(), ".env"))
os.environ.update(dotenv_path)

db_setup = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(
    os.environ.get("USERNAME"),
    os.environ.get("PASSWORD"),
    os.environ.get("HOST"),
    os.environ.get("PORT"),
    os.environ.get("DATABASE")
)

engine = create_engine(db_setup, echo=True)
Session = sessionmaker(bind=engine, expire_on_commit=True, autoflush=False)
session = Session()

Base = declarative_base()


def create_app(app):
    """This function create an application instance.
       :param app: flask instance over create blueprint instance
       :type app: Flask instance. 
    """
    Base.metadata.create_all(engine)
    
    # register blueprints
    from .api_v1 import api as api_blueprint
    from .api_v1.security import api_security
    from .api_v1.auth import api_auth

    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(api_security, url_prefix="/api_security/v1")
    app.register_blueprint(api_auth, url_prefix="/oauth")

    validator(Base)

    # register an after request handler
    @app.after_request
    def after_request(rv):
        headers = getattr(g, 'headers', {})
        rv.headers.extend(headers)
        return rv

    # authentication token route
    # from .auth import auth
    # from .decorators import crossdomain

    # @app.route('/get-auth-token', methods=['GET', 'POST'])
    # @crossdomain(origin='*', headers=['Access-Control-Allow-Origin','Access-Control-Allow-Headers','Access-Control-Allow-Methods'])
    # @auth.login_required
    # @json
    # def get_auth_token():
    #     return {'token': g.user.generate_auth_token(g.user)}

    @app.route('/get_connection_state')
    @json
    def get_connection_state():
        return {"state": True}, 200, {}

    return app
