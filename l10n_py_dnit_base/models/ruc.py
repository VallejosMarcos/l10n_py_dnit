"""Dígito verificador del RUC paraguayo (módulo 11, base 11).

Algoritmo oficial de la DNIT: se recorre el número de derecha a izquierda
multiplicando cada dígito por un factor creciente (2, 3, ... 11) que vuelve a
2 al superar la base. El verificador sale del resto de dividir la suma por 11.

Verificado contra constancias reales: 80009735-1, 1946520-3.
"""
import re

BASE = 11


def check_digit(number):
    """Devuelve el dígito verificador (0-9) de un RUC sin guion."""
    total = 0
    factor = 2
    for digit in reversed(str(number)):
        total += int(digit) * factor
        factor = factor + 1 if factor < BASE else 2
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def split(ruc):
    """Separa un RUC 'NNNNNNN-D' en (número, dígito). El guion es opcional;
    sin él, el último dígito se toma como verificador."""
    clean = re.sub(r"[^0-9]", "", ruc or "")
    if "-" in (ruc or ""):
        number, _, dv = ruc.partition("-")
        return re.sub(r"[^0-9]", "", number), re.sub(r"[^0-9]", "", dv)
    if len(clean) < 2:
        return clean, ""
    return clean[:-1], clean[-1]


def is_valid(ruc):
    """True si el RUC trae un dígito verificador correcto."""
    number, dv = split(ruc)
    if not number or not dv.isdigit():
        return False
    return check_digit(number) == int(dv)
