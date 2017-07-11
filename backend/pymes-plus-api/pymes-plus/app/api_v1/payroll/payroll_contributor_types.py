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

from flask import request, jsonify, Response
import json
from .. import api
from ...models import PayrollContributorType
from ...decorators import json
from ... import session


@api.route('/payroll_contributor_types/search', methods=['GET'])
def get_payroll_contributor_types_search():
    """
    # /payroll_contributor_subtypes/search
    <b>Methods:</b> GET <br>
    <b>Arguments:</b> None <br>
    <b>Description:</b> Return size method found in search pattern<br/>
    <b>Return:</b> JSON format
    """
    ra = request.args.get
    simple = ra("simple")

    kwargs = dict(simple=simple)

    response = PayrollContributorType.get_payroll_contributor_types_by_search(**kwargs)

    return response