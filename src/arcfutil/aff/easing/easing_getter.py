# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from typing import Callable
from .simple_easings import sine, cosine, linear
from . import cheatsheet
from .bezier import bezier, make_bezier


def get_ease(percent: float, type: str, b_point: list = [1 / 3, 0, 2 / 3, 1]) -> float:
    if type == "s":
        return percent
    elif type == "si":
        return sine(percent)
    elif type == "so":
        return cosine(percent)
    elif type == "b":
        return bezier(percent, b_point[0], b_point[1], b_point[2], b_point[3])
    # sine
    elif type == "ease_in_sine":
        return cheatsheet.ease_in_sine(percent)
    elif type == "ease_out_sine":
        return cheatsheet.ease_out_sine(percent)
    elif type == "ease_in_out_sine":
        return cheatsheet.ease_in_out_sine(percent)
    # quad
    elif type == "ease_in_quad":
        return cheatsheet.ease_in_quad(percent)
    elif type == "ease_out_quad":
        return cheatsheet.ease_out_quad(percent)
    elif type == "ease_in_out_quad":
        return cheatsheet.ease_in_out_quad(percent)
    # cubic
    elif type == "ease_in_cubic":
        return cheatsheet.ease_in_cubic(percent)
    elif type == "ease_out_cubic":
        return cheatsheet.ease_out_cubic(percent)
    elif type == "ease_in_out_cubic":
        return cheatsheet.ease_in_out_cubic(percent)
    # quart
    elif type == "ease_in_quart":
        return cheatsheet.ease_in_quart(percent)
    elif type == "ease_out_quart":
        return cheatsheet.ease_out_quart(percent)
    elif type == "ease_in_out_quart":
        return cheatsheet.ease_in_out_quart(percent)
    # quint
    elif type == "ease_in_quint":
        return cheatsheet.ease_in_quint(percent)
    elif type == "ease_out_quint":
        return cheatsheet.ease_out_quint(percent)
    elif type == "ease_in_out_quint":
        return cheatsheet.ease_in_out_quint(percent)
    # expo
    elif type == "ease_in_expo":
        return cheatsheet.ease_in_expo(percent)
    elif type == "ease_out_expo":
        return cheatsheet.ease_out_expo(percent)
    elif type == "ease_in_out_expo":
        return cheatsheet.ease_in_out_expo(percent)
    # circ
    elif type == "ease_in_circ":
        return cheatsheet.ease_in_circ(percent)
    elif type == "ease_out_circ":
        return cheatsheet.ease_out_circ(percent)
    elif type == "ease_in_out_circ":
        return cheatsheet.ease_in_out_circ(percent)
    # back
    elif type == "ease_in_back":
        return cheatsheet.ease_in_back(percent)
    elif type == "ease_out_back":
        return cheatsheet.ease_out_back(percent)
    elif type == "ease_in_out_back":
        return cheatsheet.ease_in_out_back(percent)
    # elastic
    elif type == "ease_in_elastic":
        return cheatsheet.ease_in_elastic(percent)
    elif type == "ease_out_elastic":
        return cheatsheet.ease_out_elastic(percent)
    elif type == "ease_in_out_elastic":
        return cheatsheet.ease_in_out_elastic(percent)
    # bounce
    elif type == "ease_in_bounce":
        return cheatsheet.ease_in_bounce(percent)
    elif type == "ease_out_bounce":
        return cheatsheet.ease_out_bounce(percent)
    elif type == "ease_in_out_bounce":
        return cheatsheet.ease_in_out_bounce(percent)


def get_easing_func(type: str, b_point: list = [1 / 3, 0, 2 / 3, 1]) -> Callable:
    if type == "s":
        return linear
    elif type == "si":
        return sine
    elif type == "so":
        return cosine
    elif type == "b":
        return make_bezier(b_point)
    # sine
    elif type == "ease_in_sine":
        return cheatsheet.ease_in_sine
    elif type == "ease_out_sine":
        return cheatsheet.ease_out_sine
    elif type == "ease_in_out_sine":
        return cheatsheet.ease_in_out_sine
    # quad
    elif type == "ease_in_quad":
        return cheatsheet.ease_in_quad
    elif type == "ease_out_quad":
        return cheatsheet.ease_out_quad
    elif type == "ease_in_out_quad":
        return cheatsheet.ease_in_out_quad
    # cubic
    elif type == "ease_in_cubic":
        return cheatsheet.ease_in_cubic
    elif type == "ease_out_cubic":
        return cheatsheet.ease_out_cubic
    elif type == "ease_in_out_cubic":
        return cheatsheet.ease_in_out_cubic
    # quart
    elif type == "ease_in_quart":
        return cheatsheet.ease_in_quart
    elif type == "ease_out_quart":
        return cheatsheet.ease_out_quart
    elif type == "ease_in_out_quart":
        return cheatsheet.ease_in_out_quart
    # quint
    elif type == "ease_in_quint":
        return cheatsheet.ease_in_quint
    elif type == "ease_out_quint":
        return cheatsheet.ease_out_quint
    elif type == "ease_in_out_quint":
        return cheatsheet.ease_in_out_quint
    # expo
    elif type == "ease_in_expo":
        return cheatsheet.ease_in_expo
    elif type == "ease_out_expo":
        return cheatsheet.ease_out_expo
    elif type == "ease_in_out_expo":
        return cheatsheet.ease_in_out_expo
    # circ
    elif type == "ease_in_circ":
        return cheatsheet.ease_in_circ
    elif type == "ease_out_circ":
        return cheatsheet.ease_out_circ
    elif type == "ease_in_out_circ":
        return cheatsheet.ease_in_out_circ
    # back
    elif type == "ease_in_back":
        return cheatsheet.ease_in_back
    elif type == "ease_out_back":
        return cheatsheet.ease_out_back
    elif type == "ease_in_out_back":
        return cheatsheet.ease_in_out_back
    # elastic
    elif type == "ease_in_elastic":
        return cheatsheet.ease_in_elastic
    elif type == "ease_out_elastic":
        return cheatsheet.ease_out_elastic
    elif type == "ease_in_out_elastic":
        return cheatsheet.ease_in_out_elastic
    # bounce
    elif type == "ease_in_bounce":
        return cheatsheet.ease_in_bounce
    elif type == "ease_out_bounce":
        return cheatsheet.ease_out_bounce
    elif type == "ease_in_out_bounce":
        return cheatsheet.ease_in_out_bounce
