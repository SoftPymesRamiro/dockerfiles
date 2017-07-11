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
from ...models import UserBranchRole
from ...decorators import authorize


@api.route('/user_branch_roles/<int:branch_roles_id>', methods=['DELETE'])
@authorize('users', 'd')
def delete_user_branch_role(branch_roles_id):
    """
    # /user_branch_roles/
    <b>Methods:</b> DELETE <br>
    <b>Arguments:</b> branch_roles_id <br>
    <b>Description:</b> Delete all roles according to id<br/>
    <b>Return:</b> JSON format
    """
    result = UserBranchRole.delete_user_branch_role(branch_roles_id)
    return result
