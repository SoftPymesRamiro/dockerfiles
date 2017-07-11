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



from datetime import datetime
import math
from decimal import *
from .math_ext import _round
from ..exceptions import InternalServerError


def convert_string_to_date(data):
    """
    This function allow transform a String value( with date format) 
    to Date value, used in import models

    Convierte un string a datetime
    (se utiliza generalmente en los import_data de los modelos)

    :param data: date value in string format
    :type data: string
    :return: date object
    :raise: ValueError
    :exception: An occurs when input data is null or not contains datetime
    """
    try:
        # se valida que esta cadena de entrada no sea nulo
        return None if data is None else datetime.strptime(str(data), '%a, %d %b %Y %H:%M:%S %Z')
    except Exception as e:
        return None if data is None else datetime.strptime(str(data), '%Y-%m-%dT%H:%M:%S.%fZ')


def number_to_text(value):
    num_to_text = ''
    value = math.trunc(value)

    if value == 0:
        num_to_text = 'CERO'
    elif value == 1:
        num_to_text = 'UNO'
    elif value == 2:
        num_to_text = 'DOS'
    elif value == 3:
        num_to_text = 'TRES'
    elif value == 4:
        num_to_text = 'CUATRO'
    elif value == 5:
        num_to_text = 'CINCO'
    elif value == 6:
        num_to_text = 'SEIS'
    elif value == 7:
        num_to_text = 'SIETE'
    elif value == 8:
        num_to_text = 'OCHO'
    elif value == 9:
        num_to_text = 'NUEVE'
    elif value == 10:
        num_to_text = 'DIEZ'
    elif value == 11:
        num_to_text = 'ONCE'
    elif value == 12:
        num_to_text = 'DOCE'
    elif value == 13:
        num_to_text = 'TRECE'
    elif value == 14:
        num_to_text = 'CATORCE'
    elif value == 15:
        num_to_text = 'QUINCE'
    elif value < 20:
        num_to_text = 'DIECI{0}'.format(number_to_text(value - 10))
    elif value == 20:
        num_to_text = 'VEINTE'
    elif value < 30:
        segunda_cifra = ''
        if value % 20 == 1:
            segunda_cifra = 'UN'
        else:
            segunda_cifra = number_to_text(value % 20)

        num_to_text = 'VEINTI{0}'.format(segunda_cifra)
    elif value == 30:
        num_to_text = 'TREINTA'
    elif value == 40:
        num_to_text = 'CUARENTA'
    elif value == 50:
        num_to_text = 'CINCUENTA'
    elif value == 60:
        num_to_text = 'SESENTA'
    elif value == 70:
        num_to_text = 'SETENTA'
    elif value == 80:
        num_to_text = 'OCHENTA'
    elif value == 90:
        num_to_text = 'NOVENTA'
    elif value < 100:
        segunda_cifra = ''
        if value % 10 == 1:
            segunda_cifra = 'UN'
        else:
            segunda_cifra = number_to_text(value % 10)

        num_to_text = '{0} Y {1}'.format(number_to_text(math.trunc(value / 10) * 10),
                                         segunda_cifra)

    elif value == 100:
        num_to_text = 'CIEN'
    elif value < 200:
        num_to_text = 'CIENTO {0}'.format(number_to_text(value - 100))
    elif value == 200 or value == 300 or value == 400 or value == 600 or value == 800:
        num_to_text = '{0}CIENTOS'.format(number_to_text(value / 100))
    elif value == 500:
        num_to_text = 'QUINIENTOS'
    elif value == 700:
        num_to_text = 'SETECIENTOS'
    elif value == 900:
        num_to_text = 'NOVECIENTOS'
    elif value < 1000:
        num_to_text = '{0} {1}'.format(number_to_text(math.trunc(value / 100) * 100),
                                       number_to_text(value % 100))
    elif value == 1000:
        num_to_text = 'MIL'
    elif value < 2000:
        num_to_text = 'MIL {0}'.format(number_to_text(value % 1000))
    elif value < 1000000:
        num_to_text = '{0} MIL'.format(number_to_text(value / 1000))
        if value % 1000 > 0:
            num_to_text = '{0} {1}'.format(num_to_text, number_to_text(value % 1000))
    elif value == 1000000:
        num_to_text = 'UN MILLÓN'
    elif value < 2000000:
        num_to_text = 'UN MILLÓN {0}'.format(number_to_text(value % 1000000))
    elif value < 1000000000000:
        num_to_text = '{0} MILLONES'.format(number_to_text(math.trunc(value / 1000000)))
        if (value - math.trunc(value / 1000000) * 1000000) > 0:
            num_to_text = '{0} {1}'.format(num_to_text,
                                           number_to_text(value - math.trunc(value / 1000000)
                                                                               * 1000000))
    elif value == 1000000000000:
        num_to_text = 'UN BILLÓN'
    elif value < 2000000000000:
        num_to_text = 'UN BILLÓN {0}'.format(number_to_text(value - (math.trunc(value / 1000000000000)
                                                                      * 1000000000000)))
    else:
        num_to_text = '{0} BILLONES'.format(number_to_text(math.trunc(value / 1000000000000)))
        if (value - math.trunc(value / 1000000000000) * 1000000000000) > 0:
            num_to_text = '{0} {1}'.format(num_to_text, number_to_text(value - math.trunc(value / 1000000000000)
                                                                       * 1000000000000))
    return num_to_text


def total_to_letter(total, currency, post_fijo_monto_letras):
    cantidad = Decimal(total)
    entero = int(math.trunc(cantidad))
    decimales = int(_round((cantidad - entero) * 100, 2))
    dec = 'CON {0}/100'.format(fill_from_left(str(decimales), '0', 2))
    res = '{0} '.format(number_to_text(Decimal(entero)))
    if not (entero == 0):
        if (entero % 1000000) == 0:
            res = '{0} DE '.format(res)

    res = '{0} {1} {2} {3}'.format(res, get_currency(currency.upper()), dec,
                                   post_fijo_monto_letras.upper())
    return res


def fill_from_left(strg, fill, size):
    filled_string = strg
    while len(filled_string) < size:
        filled_string = '{0}{1}'.format(fill, filled_string)
    return filled_string


def get_currency(currency):
    curr = currency.split()

    if len(curr):
        for idx, c in enumerate(curr):
            if c[-1] == 'A' or c[-1] == 'E' or c[-1] == 'I' or c[-1] == 'O' or c[-1] == 'U':
                curr[idx] = '{0}S'.format(curr[idx])
            else:
                curr[idx] = '{0}ES'.format(curr[idx])
    return ' '.join(curr)


def format_decimal_values(value, decimals):
    """
    Allow format decimal values to split values by commas,
    :param value: value decimal
    :param decimals: decimal to round
    :return: string with formatted value
    """
    import locale
    # locale.setlocale(locale.LC_ALL, '')
    return locale.format("%.{0}f".format(decimals),
                         _round(value if value else 0, decimals), grouping=True)


def format_cc_or_nit(value):
    """
    Allow format third's identification number e.g (9,999,999)
    :param value: text with identification number
    :return: formated string
    """
    try:
        return '{0}'.format('{:,}'.format(int(value)))
    except Exception as e:
        raise InternalServerError(e)
