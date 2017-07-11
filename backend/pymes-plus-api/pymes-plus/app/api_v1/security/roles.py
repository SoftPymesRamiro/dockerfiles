# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# Securyty module
# 
# Roles -> create, read, update and delete
# Date: 19-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"


from .. import api
from ...models import Rol, Option
from flask import request, jsonify
from ...decorators import authorize


@api.route('/profiles/', methods=['GET'])
def get_profiles():
    """
    # /profiles
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return  all roles <br/>
    <b>Return:</b> JSON format
    """
    search = request.args.get('search')
    if search is not None:
        roles = Rol.get_roles_by_search(search)
        return jsonify(data=roles if roles is not None else {})
    profile_list = Rol.get_roles()
    return profile_list


@api.route('/profiles/<int:role_id>', methods=['GET'])
def get_options_by_role_id(role_id):
    """
    # /profiles/<int:role_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> role_id: rol id <br>
    <b>Description:</b> Return  profile according rol id <br/>
    <b>Return:</b> JSON format
    """
    option = Option()
    result = option.get_options_by_rol_id(role_id)
    return jsonify(data=[i.export_data() for i in result])


@api.route('/profiles/', methods=['POST'])
@authorize('profiles', 'c')
def post_profile():
    """
    # /profiles/>
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> <br>
    <b>Description:</b> Save profile<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    result = Option.save_profile(data)
    result = jsonify(result)
    result.status_code = 201
    return result


@api.route('/profiles/<int:profile_id>', methods=['PUT'])
@authorize('profiles', 'u')
def put_profile(profile_id):
    """
    # /profiles/<int:profile_id>
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> profile_id: profile id <br>
    <b>Description:</b> Update profile<br/>
    <b>Return:</b> JSON format
    """
    data = request.json
    result = Option.update_profile(profile_id, data)
    return jsonify(result)


@api.route('/profiles/<int:profile_id>', methods=['DELETE'])
@authorize('profiles', 'd')
def delete_profile(profile_id):
    """
    # /profiles/<int:profile_id>
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> profile_id: profile id <br>
    <b>Description:</b> Delete profile<br/>
    <b>Return:</b> JSON format
    """
    result = Option.delete_profile(profile_id)
    return jsonify(result)


@api.route('/options/', methods=['GET'])
def get_options():
    """
    # /options
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> all_role_option_tree <br>
    <b>Description:</b> Return  all options's system <br/>
    <b>Return:</b> JSON format
    <b>Sample:</b><br/>
        /options/?all_role_option_tree : obtiene todos los roles seteados en false<br/>
    """
    all_role_option_tree = request.args.get('all_role_option_tree')

    result = None
    if all_role_option_tree is not None:
        option = Option()
        result = option.all_role_option_on_tree()
    if result is not None:
        return jsonify(data=[i.export_data() for i in result])
