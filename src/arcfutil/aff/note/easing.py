#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import sin
from math import cos
from math import pi


def linar(percent):
    return percent


def sine(percent):
    return sin(percent * (pi / 2))


def cosine(percent):
    return cos((percent * (pi / 2)) + pi) + 1


# 参照了Webkit的贝塞尔缓动实现
# https://trac.webkit.org/browser/trunk/Source/WebCore/platform/graphics/UnitBezier.h
def bezier(percent, p1x: float = 1/3, p1y: float = 0, p2x: float = 2/3, p2y: float = 1) -> float:
    cx = 3.0 * p1x;
    bx = 3.0 * (p2x - p1x) - cx;
    ax = 1.0 - cx -bx;
    cy = 3.0 * p1y;
    by = 3.0 * (p2y - p1y) - cy;
    ay = 1.0 - cy - by;

    def solve_curve_x(x: float) -> float:
        t2 = x
        for i in range(8):
            x2 = ((ax * t2 + bx) * t2 + cx) * t2 - x
            if abs(x2) < 1e-6:
                return t2
            d2 = (3.0 * ax * t2 + 2.0 * bx) * t2 + cx
            if abs(d2) < 1e-6:
                break
            t2 = t2 - x2 / d2
        
        t0 = 0.0
        t1 = 1.0
        t2 = x

        if t2 < t0:
            return t0
        if t2 > t1:
            return t1

        while t0 < t1:
            x2 = ((ax * t2 + bx) * t2 + cx) * t2
            if abs(x2 - x) < 1e-6:
                return t2
            if x > x2:
                t0 = t2
            else:
                t1 = t2
            t2 = (t1 - t0) * 0.5 + t0

        return t2
    
    t = solve_curve_x(percent)
        
    return ((ay * t + by) * t + cy) * t


def get_ease(percent: float, type: str, b_point: list = [1/3, 0, 2/3, 1]) -> float:
    if type == 's':
        return percent
    elif type == 'si':
        return sine(percent)
    elif type == 'so':
        return cosine(percent)
    elif type == 'b':
        return bezier(percent, b_point[0], b_point[1], b_point[2], b_point[3])


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
