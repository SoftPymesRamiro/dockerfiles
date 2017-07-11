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
from ...models import Zone
from ...decorators import authorize


@api.route('/zone/', methods=['GET'])
def get_zones():
    """
    # /api/v1/zone/
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return all zones <br/>
    <b>Return:</b> json format
    """
    response = Zone.get_zones()
    return response


@api.route('/zone/company/<int:company_id>', methods=['GET'])
def zone_company_by_id(company_id):
    """
    # /api/v1/zone/company/<int:company_id>
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> company_id <br>
    <b>Description:</b> Return all zones for to give company_id<br/>
    <b>Return:</b> JSON format
    """
    response = Zone.get_zone_by_company(company_id)
    return response

