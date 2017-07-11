# coding=utf-8
#!/usr/bin/env python
#########################################################
# Referential module
# All credits by SoftPymes Plus
# 
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"



from .. import api
from flask import request
from ...models import DefaultValue


@api.route('/default_values/', methods=['GET'])
# /api/v1/default_values/ - Obtiene listado completo de valores por defecto
def default_values_list():
    """
    # /default_values/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all default values
    <b>Return:</b> json format
    """ 
    response = DefaultValue.get_default_values()
    return response


@api.route('/default_values/<int:default_value_id>', methods=['GET'])
# /api/v1/default_values/{default_value_id} - Obtiene un valor por defecto por id
def default_values_by_id(default_value_id):
    """
    # /default_values/<int:default_value_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> default_value_id <br>
    <b>Description:</b> Return default value for the given id
    <b>Return:</b> json format
    """  
    response = DefaultValue.get_default_value_by_id(default_value_id)
    return response


@api.route('/default_values/search', methods=['GET'])
# /api/v1/default_values/search - Obtiene listado de valores por defecto por busqueda
# /api/v1/default_values/search?by_branch=true&branch_id={branch_id}
#                                                   - Obtiene listado de valores por defecto por branchId
#  /api/v1/default_values/search?to_decimals=true&branch_id={branch_id}
#                                                   - Obtiene listado de decimales por defecto por branchId
def default_values_search():
    """
    # /default_values/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return default_values for the given id<br/>
    #?search all values <br/>
    #?search?by_branch=true&branch_id={branch_id}  according to branchId <br/>
    #?to_decimals=true&branch_id={branch_id} according to branchId with decimal<br/>
    <b>Return:</b> json format
    """ 
    ra = request.args.get
    by_branch = ra("by_branch")
    branch_id = ra("branch_id")
    to_decimals = ra("to_decimals")
    kwargs = dict(by_branch=by_branch, branch_id=branch_id, to_decimals=to_decimals)
    response = DefaultValue.get_default_values_by_search(**kwargs)
    return response


@api.route('/default_values/', methods=['POST'])
# /api/v1/default_values/ - Obtiene listado completo de valores por defecto
def post_default_values():
    """
    # /default_values/
    <b>Methods:</b> POST <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Set all default_values <br/>
    <b>Return:</b> json format
    """ 
    data = request.json
    response = DefaultValue.post_default_value(data)
    return response


@api.route('/default_values/<int:default_value_id>', methods=['PUT'])
# /api/v1/default_values/ - Obtiene listado completo de valores por defecto
def put_default_values(default_value_id):
    """
    # /default_values/
    <b>Methods:</b> PUT <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Change an default value and return all default values<br/>
    <b>Return:</b> json format
    """ 
    data = request.json
    response = DefaultValue.put_default_value(default_value_id, data)
    return response
