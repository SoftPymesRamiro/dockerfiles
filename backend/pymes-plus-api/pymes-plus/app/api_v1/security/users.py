# -*- coding: utf-8 -*-
from flask import request, jsonify
from . import api_security
from ...models import User
from ...decorators import json, authorize
from ...auth import auth_token


@api_security.route("/users/<int:user_id>", methods=["GET"])
@json
def get_user(user_id):
    """
    # /users/<int:user_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> user_id <br>
    <b>Description:</b> Return User accordig to user_id<br/>
    <b>Return:</b> JSON format
    """
    user = User.get_user(user_id)
    if user is None:
        return {}, 404, {}
    return user, 200, {}


@api_security.route("/users/", methods=["GET"])
def get_users():
    """
    # /users/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return All users <br/>
    <b>Return:</b> JSON format<br/>
    <b>Sample:</b><br/>
        /users/ : obtiene todo los usuarios<br/>
        /users?light=1 : obtiene todos los usuarios pero no con todos los campos<br/>
        /users?can_create_anonymous_user : devulve si el usuario puede crear usuarios anonimos<br/>
        /users?search=xyz : busca por username y firstname + lastname<br/>
    """
    # Metodo para listar los usuarios
    # Ejemplos:
    # /users/ : obtiene todo los usuarios
    # /users?light=1 : obtiene todos los usuarios pero no con todos los campos
    # /users?can_create_anonymous_user : devulve si el usuario puede crear usuarios anonimos
    # /users?search=xyz : busca por username y firstname + lastname
    # :return:
    light = request.args.get("light")
    can_create_anonymous_users = request.args.get("can_create_anonymous_users")
    search = request.args.get("search")

    user_list = User.get_users(light=light, 
        can_create_anonymous_users=can_create_anonymous_users, search=search)

    if user_list is not None:
        return jsonify(data=user_list)
    else:
        res = jsonify()
        res.status_code = 401
        return res


@api_security.route("/users/my_user", methods=["GET"])
@auth_token.login_required
@json
def my_user():
    """
    # /users/my_user
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return current user <br/>
    <b>Return:</b> JSON format<br/>
    """
    result = User.get_my_user()
    return result


@api_security.route("/users/", methods=['POST'])
@authorize('users', 'c')
@json
def new_user():
    """
    # /users/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Create a new user <br/>
    <b>Return:</b> JSON format<br/>
    """

    ##
    # Metodo para creacion de usaurios
    # :return:
    ##
    result = User.new_user(request.json)
    return result
    # except ValidationError as err:
    #     return {"error": str(err)}, 400, {}
    # except KeyError as err:
    #     return {"error": str(err)}, 400, {}
    # raise ValidationError(err)


@api_security.route("/users/<int:id>", methods=["PUT"])
@authorize('users', 'u')
@auth_token.login_required
@json
def update_user(id):
    """
    # /users/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Update users <br/>
    <b>Return:</b> JSON format<br/>
    <b>Sample:</b><br/>
        /users/1 : actualiza todo el usuario<br/>
        /users/1?changePassword=1 : actualiza contraseña para usuario inicial<br/>
        /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado<br/>
    """

    # """
    #     Metodo para actulizar usarios
    #     Ejemplo:
    #         /users/1 : actualiza todo el usuario
    #         /users/1?theme=1 : actualiza solo el tema del usuario
    #         /users/1?branchId=123 : actualiza la ultima sucursal visitada por el cliente
    #         /users/1?changePassword=1 : actualiza contraseña para usuario inicial
    #         /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado
    #     :param id: id de usuario
    #     :return:
    # """
    change_password = request.args.get("changePassword")
    change_password_old_user = request.args.get("changePasswordOldUser")
    data = request

    result = User.update_user(id, data, change_password=change_password,
                              change_password_old_user=change_password_old_user)

    return result


@api_security.route("/users/<int:id>/theme", methods=["PUT"])
@auth_token.login_required
@json
def update_user_theme(id):
    """
    # /users/
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Update user's theme <br/>
    <b>Return:</b> JSON format<br/>
    <b>Sample:</b><br/>
        /users/1/theme : actualiza solo el tema del usuario<br/>
    """

    # """
    #     Metodo para actulizar usarios
    #     Ejemplo:
    #         /users/1 : actualiza todo el usuario
    #         /users/1?theme=1 : actualiza solo el tema del usuario
    #         /users/1?branchId=123 : actualiza la ultima sucursal visitada por el cliente
    #         /users/1?changePassword=1 : actualiza contraseña para usuario inicial
    #         /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado
    #     :param id: id de usuario
    #     :return:
    # """
    data = request

    result = User.update_user_theme(id, data)

    return result


@api_security.route("/users/<int:id>/branches/<int:branch_id>", methods=["PUT"])
@auth_token.login_required
@json
def update_user_last_branch(id, branch_id):
    """
    # /users/
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Update last branch's id <br/>
    <b>Return:</b> JSON format<br/>
    <b>Sample:</b><br/>
        /users/1/branches/12 : actualiza la ultima sucuarsal usada por el cliente<br/>
    """

    # """
    #     Metodo para actulizar usarios
    #     Ejemplo:
    #         /users/1 : actualiza todo el usuario
    #         /users/1?theme=1 : actualiza solo el tema del usuario
    #         /users/1?branchId=123 : actualiza la ultima sucursal visitada por el cliente
    #         /users/1?changePassword=1 : actualiza contraseña para usuario inicial
    #         /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado
    #     :param id: id de usuario
    #     :return:
    # """

    result = User.update_user_branch(id, branch_id)

    return result


@api_security.route("/users/<int:id>/process_date", methods=["PUT"])
@auth_token.login_required
@json
def update_user_process_date(id):
    """
    # /users/
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Update user's process date <br/>
    <b>Return:</b> JSON format<br/>
    <b>Sample:</b><br/>
        /users/1 : actualiza todo el usuario<br/>
        /users/1?theme=1 : actualiza solo el tema del usuario<br/>
        /users/1?changePassword=1 : actualiza contraseña para usuario inicial<br/>
        /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado<br/>
    """

    # """
    #     Metodo para actulizar usarios
    #     Ejemplo:
    #         /users/1 : actualiza todo el usuario
    #         /users/1?theme=1 : actualiza solo el tema del usuario
    #         /users/1?branchId=123 : actualiza la ultima sucursal visitada por el cliente
    #         /users/1?changePassword=1 : actualiza contraseña para usuario inicial
    #         /users/1?changePasswordOldUser=1 : actualiza contraseña para usuario migrado
    #     :param id: id de usuario
    #     :return:
    # """
    process_date = request.args.get("processDate")

    result = User.update_user_process_date(id, process_date=process_date)

    return result


@api_security.route("/users/<int:user_id>", methods=["DELETE"])
@authorize('users', 'd')
@auth_token.login_required
@json
def delete_user(user_id):
    """
    # /users/
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Delete a user according to identifier<br/>
    <b>Return:</b> JSON format<br/>
    """
    result = User.delete_user(user_id)
    return result


@api_security.route("/branches/<int:branch_id>/users/<int:user_id>/options")
@auth_token.login_required
def get_options(branch_id, user_id):
    """
    # /branches/<int:branch_id>/users/<int:user_id>/options
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> branch_id, user_id <br>
    <b>Description:</b> Return options according to user_id and branch_id<br/>
    <b>Return:</b> JSON format
    """
    result = User.get_options(user_id, branch_id)
    if result is not None:
        d = {}
        for r in result:
            d[r.option.code] = r.export_data_custom()
        res = jsonify(d)
        return res
    else:
        res = jsonify()
        res.status_code = 404
        return res
