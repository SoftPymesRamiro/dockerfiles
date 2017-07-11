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



from sqlalchemy import event, String, Integer, DateTime
import datetime
from ..exceptions import ValidationError


def validator(Base):
    """
    Validtador
    This class allow validate several user inputs
    eg. int, string, dates .etc.
    """
    def validate_int(value, column):
        """This function allow validate that input is a int value
        :param value: a string instance
        :param column: 

        :returns:int value in string
        :raises: AssertionError An error occurred wheter 
            in string not int representation.
        """
        if isinstance(value, str):
            print(value)
            value = int(value)
        elif value is None:
            value = None
        else:
            if not isinstance(value, int):
                raise AssertionError("Invalid field {0}".format(column))
        return value

    def validate_string(value, column):
        """
        This function allow validate that input is a string value
        :param value:
        :param column:
        """ 
        if value is None:
            value = None
        elif not isinstance(value, str):
            raise ValidationError("Invalid field {0}".format(column))
        return value

    def validate_datetime(value, column):
        """
        This function allow validate that input is a date value
        :param value:
        :param column:
        """ 
        if not isinstance(value, datetime.datetime) and not column.nullable:
            raise ValidationError("Invalid field {0}".format(column))
        elif value is None:
            value = None
        return value

    validators = {
        Integer: validate_int,
        String: validate_string,
        DateTime: validate_datetime,
    }

    # this event is called whenever an attribute
    # on a class is instrumented
    @event.listens_for(Base, 'attribute_instrument')
    def configure_listener(class_, key, inst):
        """
        this event is called whenever an attribute
        on a class is instrumented
        """
        if not hasattr(inst.property, 'columns'):
            return

        # this event is called whenever a "set"
        # occurs on that instrumented attribute
        @event.listens_for(inst, "set", retval=True)
        def set_(instance, value, oldvalue, initiator):
            """
            this event is called whenever a "set"
            occurs on that instrumented attribute
            """
            validator = validators.get(inst.property.columns[0].type.__class__)
            if validator:
                return validator(value, inst.property.columns[0])
            else:
                return value