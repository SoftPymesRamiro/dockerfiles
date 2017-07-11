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
from ...models import Contact
from ...decorators import json
from ... import session


@api.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):

    """
        @api {delete} /contacts/contactsId Remove Contacts
        @apiName Delete
        @apiGroup Referential.Contacts
        @apiParam {Number} contactsId contacts identifier
        @apiDescription Delete a contacts according to id
        @apiSuccessExample {json} Success
           HTTP/1.1 204 No Content
        @apiErrorExample {json} Error-Response
            HTTP/1.1 500 Internal Server Error
        """
    response = Contact.delete_contact(contact_id)
    return response
