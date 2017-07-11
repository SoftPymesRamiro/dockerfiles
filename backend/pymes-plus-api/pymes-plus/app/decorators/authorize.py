from flask import g, abort
from functools import wraps


def authorize(option, value):
    def wrapper(func):
        @wraps(func)
        def authorize_and_call(*args, **kwargs):
            from ..models.security.rol_option import RolOption
            try:
                last_branch_id = g.user['last_branch_id']
                user_id = g.user['sub']
                if RolOption.is_authorized(option, value, user_id, last_branch_id):
                    # print('inside authorization as {0} with {1}'.format(self.option, self.value))
                    return func(*args, **kwargs)
                else:
                    abort(403)
            except AttributeError as e:
                # Solo debe entrar aqui cuando es firstlogin y el usuario esta cambiando la contraseña
                if g.is_authenticate is None:
                    return func(*args, **kwargs)
        return authorize_and_call
    return wrapper


def authorize_without_user(option, value):
    def wrapper(func):
        @wraps(func)
        def authorize_and_call(*args, **kwargs):
            from ..models.security.rol_option import RolOption
            last_branch_id = g.user['last_branch_id']
            user_id = g.user['sub']
            if RolOption.is_authorized(option, value, user_id, last_branch_id):
                # print('inside authorization as {0} with {1}'.format(self.option, self.value))
                return func(*args, **kwargs)
            else:
                abort(403)
        return authorize_and_call
    return wrapper