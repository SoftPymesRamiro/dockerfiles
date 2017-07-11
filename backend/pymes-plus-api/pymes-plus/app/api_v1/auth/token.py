# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# All rights by SoftPymes Plus
#
# Auth module
# Allow the access to Sofpymes by token key
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from . import api_auth
from ...auth import auth
from ...decorators import json
from flask import g, request
from ...models import User
from ... import session
from ...utils import CryptoTools, StandardResponses
from ...exceptions import ValidationError
from sqlalchemy import func


@api_auth.route('/token', methods=['GET', 'POST'])
@json
def get_auth_token():
    """Allow store a NON basic access authentication 
        is a method for an HTTP user agent to provide a 
        <b>user name</b> and <b>password </b>when 
        making a request. <br>
        <b>Description (ES):</b> Almacena en variable 
        global el usuario que se esta logeando 
        (para ser usado en toda la aplicacion) <b>g.user = user</b> 
        Validacion para verificar el usuario que 
        por primer vez se logea y ademas que viene de
        la anterior version.

    # /token <br>
    GET: Returns HTTP 200 on success; body is payload with token.
         Returns HTTP 401 bad.
    """
    try:
        username = request.json['username']
        password = request.json['password']

        user = User.find_user(username, password) ## busqueda del usuario

        if user is None:
            user_old_password = CryptoTools.encrypt_pymes_plus(str(password), str(username).upper().ljust(8, 'F'))
            user_id = session.query(User).filter(User.userName.ilike('%'+username+'%'),
                                                 User.oldPassword == user_old_password).first()

            if user_id is not None:
                raise ValidationError(['invalid_grant_migrated', StandardResponses.invalid_grant_change_password, user_id.userId])
            if session.query(User).first() is None and str(username).upper() == 'USUARIOINICIAL' \
                    and password == '12345':
                raise ValidationError(['invalid_grant_CreateFirstUser', StandardResponses.invalid_grant_create_first_user])
            raise ValidationError(['invalid_grant', StandardResponses.invalid_grant])

        if user and user.changePasswordOnNextLogin:
            raise ValidationError(['invalid_grant_ChangePassword', StandardResponses.invalid_grant_change_password,
                                   user.userId])

        if user and not user.state:
            raise ValidationError(['invalid_grant_state', StandardResponses.invalid_grant])

        return {'token': user.generate_auth_token(user)}

    except KeyError as e:

        raise ValidationError('Invalid user: missing ' + e.args[0])
