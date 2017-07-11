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

from .. import api
from flask import request
from ...models import IVA

@api.route('/iva/', methods=['GET'])
# /api/v1/iva/ - Obtiene listado completo de iva
def ivas_list():
    """
    # /iva/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all iva values<br/>
    <b>Return:</b> JSON format
    """
    response = IVA.get_iva()
    return response


@api.route('/iva/search', methods=['GET'])
# /api/v1/iva/search - Obtiene listado de IVAs por busqueda
# /api/v1/iva/search?to_items=true - iva de compra y de venta
def ivas_search():
    """
    # /iva/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return iva according a search pattern<br/>
    #search/ all ivas by search <br/>
    #search?to_items=true  iva purchase and iva sale values<br/>
    <b>Return:</b> JSON format
    """ 
    ra = request.args.get
    to_items = ra('to_items')
    args = (to_items,)
    response = IVA.get_iva_by_search(*args)
    return response
