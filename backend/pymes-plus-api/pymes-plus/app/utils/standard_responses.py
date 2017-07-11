# -*- coding: utf-8 -*-
#!/usr/bin/env python
#########################################################
# Utils module
# All credits by SoftPymes Plus
# 
# Date: 21-07-2016
#########################################################
__author__ = "SoftPymes"
__credits__ = [""]
__version__ = "1.0.1"




class StandardResponses(object):
	"""StandardResponses
		StandardResponses allow create spanish comon mensajes reponse to request
		from clients
	"""
	ok_creado_correctamente = 'Objeto creado correctamente'
	invalid_grant = 'Tu usuario o contraseña es incorrecto.'
	invalid_grant_change_password = 'Debes cambiar tu contraseña para continuar.'
	invalid_grant_create_first_user = 'Has iniciado desde un USUARIO INICIAL, ahora debes crear tu usuario ADMINISTRADOR.'
	bad_request_faltan_parametros = 'Faltan parametros en la consulta'
