import math as m
import random as r


def OTP_generator():
    string = '0123456789abcdefghijklmnopqrstuvwxyz'
    OTP: str = ""  # noqa
    var_length = len(string)
    for i in range(6):
        OTP += string[m.floor(r.random() * var_length)]

    return OTP
