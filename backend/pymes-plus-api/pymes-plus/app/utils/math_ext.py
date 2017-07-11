import math
from decimal import Decimal


def _round(d, decimal=0):
    """
    Rounds using arithmetic (5 rounds up) symmetrical (up is away from zero) rounding
    :param d: decimal number to be rounded
    :param decimal: The number of significant fractional digits (precision) in the return value.
    :return: The number nearest d with precision equal to decimals.
    """""
    p = 10 ** decimal
    d = Decimal(d)
    if decimal == 0:
        return int(math.floor((d * p) + Decimal(math.copysign(0.5, d))) / p)

    return float(math.floor((d * p) + Decimal(math.copysign(0.5, d))))/p
