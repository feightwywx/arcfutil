# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from typing import Callable
from .simple_easings import linear, sine, cosine
from .bezier import bezier

def slicer(time, fromtime, totime, fromposition, toposition, easingtype='s'):
    t_offset = fromtime
    p_offset = fromposition
    time -= t_offset
    totime -= t_offset
    toposition -= p_offset

    if isinstance(easingtype, str):
        if easingtype == 's':
            return toposition * linear(time / totime) + p_offset
        elif easingtype == 'si':
            return toposition * sine(time / totime) + p_offset
        elif easingtype == 'so':
            return toposition * cosine(time / totime) + p_offset
        elif easingtype == 'b':
            return toposition * bezier(time / totime) + p_offset
    elif isinstance(easingtype, Callable):
        return toposition * easingtype(time / totime) + p_offset
