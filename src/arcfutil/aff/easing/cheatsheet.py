# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import sin, pi

from .bezier import make_bezier

ease_in_sine = make_bezier((0.12, 0, 0.39, 0))
ease_out_sine = make_bezier((0.61, 1, 0.88, 1))
ease_in_out_sine = make_bezier((0.37, 0, 0.63, 1))

ease_in_quad = make_bezier((0.11, 0, 0.5, 0))
ease_out_quad = make_bezier((0.5, 1, 0.89, 1))
ease_in_out_quad = make_bezier((0.45, 0, 0.55, 1))

ease_in_cubic = make_bezier((0.32, 0, 0.67, 0))
ease_out_cubic = make_bezier((0.33, 1, 0.68, 1))
ease_in_out_cubic = make_bezier((0.65, 0, 0.35, 1))

ease_in_quart = make_bezier((0.5, 0, 0.75, 0))
ease_out_quart = make_bezier((0.25, 1, 0.5, 1))
ease_in_out_quart = make_bezier((0.76, 0, 0.24, 1))

ease_in_quint = make_bezier((0.64, 0, 0.78, 0))
ease_out_quint = make_bezier((0.22, 1, 0.36, 1))
ease_in_out_quint = make_bezier((0.83, 0, 0.17, 1))

ease_in_expo = make_bezier((0.7, 0, 0.84, 0))
ease_out_expo = make_bezier((0.16, 1, 0.3, 1))
ease_in_out_expo = make_bezier((0.87, 0, 0.13, 1))

ease_in_circ = make_bezier((0.55, 0, 1, 0.45))
ease_out_circ = make_bezier((0, 0.55, 0.45, 1))
ease_in_out_circ = make_bezier((0.85, 0, 0.15, 1))

ease_in_back = make_bezier((0.36, 0, 0.66, -0.56))
ease_out_back = make_bezier((0.34, 1.56, 0.64, 1))
ease_in_out_back = make_bezier((0.68, -0.6, 0.32, 1.6))


# 几个无法只用三阶贝塞尔曲线实现的缓动函数
# https://github.com/ai/easings.net
def ease_in_elastic(x: float) -> float:
    c4 = (2 * pi) / 3

    return 0 if x == 0 else (
        1 if x == 1 else -pow(2, 10 * x - 10) * sin((x * 10 - 10.75) * c4))


def ease_out_elastic(x: float) -> float:
    c4 = (2 * pi) / 3

    return 0 if x == 0 else (
        1 if x == 1 else (pow(2, -10 * x) * sin((x * 10 - 0.75) * c4) + 1))


def ease_in_out_elastic(x: float) -> float:
    c5 = (2 * pi) / 4.5

    return 0 if x == 0 else (
           1 if x == 1 else (
           -(pow(2, 20 * x - 10) * sin((20 * x - 11.125) * c5)) / 2 if x < 0.5 else (
           (pow(2, -20 * x + 10) * sin((20 * x - 11.125) * c5)) / 2 + 1)))


def ease_in_bounce(x: float) -> float:
    return 1 - ease_out_bounce(1 - x)


def ease_out_bounce(x: float) -> float:
    n1 = 7.5625
    d1 = 2.75

    if x < (1 / d1):
        return n1 * x * x
    elif x < (2 / d1):
        return n1 * (x - 1.5 / d1) ** 2 + 0.75
    elif x < (2.5 / d1):
        return n1 * (x - 2.25 / d1) ** 2 + 0.9375
    else:
        return n1 * (x - 2.625 / d1) ** 2 + 0.984375


def ease_in_out_bounce(x: float) -> float:
    return (1 - ease_out_bounce(1 - 2 * x)) / 2 if x < 0.5 else (1 + ease_out_bounce(2 * x - 1)) / 2
