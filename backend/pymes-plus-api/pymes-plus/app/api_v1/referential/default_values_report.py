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
from ...models import DefaultValueReport


@api.route('/default_values_report/search', methods=['GET'])
# /api/v1/default_values/search - Obtiene listado de valores por defecto por busqueda
def default_values_report_search():
    """
    # /default_values_report/search?branch_id={branch_id}&short_word={short_word}
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return default_values_report by params<br/>
    #?default_value_id={default_value_id}&short_word={short_word} return list of document forms <br/>
    <b>Return:</b> json format
    """

    ra = request.args.get
    short_word = ra("short_word")
    branch_id = ra("branch_id")
    kwargs = dict(short_word=short_word, branch_id=branch_id)
    response = DefaultValueReport.get_default_value_report_by_search(**kwargs)
    return response
