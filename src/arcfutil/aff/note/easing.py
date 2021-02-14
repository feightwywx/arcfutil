#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from functools import wraps
from math import sin
from math import cos
from math import pi


# def __checker(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         return func(*args, **kwargs)
#     return decorated


def linar(percent):
    return percent


def sine(percent):
    return sin(percent * (pi / 2))


def cosine(percent):
    return cos((percent * (pi / 2)) - (pi / 2))


def bezier(percent):
    t = percent
    return 3 * (1 - t) * pow(t, 2) + pow(t, 3)  # Bezier公式 0 0 1 1


# @__checker
def slicer(time, fromtime, totime, fromposition, toposition, easingtype='s'):
    t_offset = fromtime
    p_offset = fromposition
    time -= t_offset
    totime -= t_offset
    toposition -= p_offset

    if easingtype == 's':
        return toposition * linar(time / totime) + p_offset
    elif easingtype == 'si':
        return toposition * sine(time / totime) + p_offset
    elif easingtype == 'so':
        return toposition * cosine(time / totime) + p_offset
    elif easingtype == 'b':
        return toposition * bezier(time / totime) + p_offset
