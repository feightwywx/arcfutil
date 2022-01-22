#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import sin
from typing import Callable, Literal, Union
from ..note import Timing
from ..note import NoteGroup
from ..easing import get_ease, get_easing_func


def timing_glitch(
        origin_t: int, dest_t: int, count: int, bpm_range: float, exact_bar: float = 4.00, zero_bar: float = 4.00
) -> NoteGroup:
    destgroup = NoteGroup()
    if count > 1:
        count -= 1
    stept = (dest_t - origin_t) / count
    t = origin_t
    exactbpm = -bpm_range
    while t < dest_t:
        exactbpm = -exactbpm
        destgroup.append(Timing(t, exactbpm, exact_bar))
        destgroup.append(Timing(t + 1, 0, zero_bar))
        t += stept
    return destgroup


# 出于兼容性考虑保留
def timing_easing_linear(
        origin_t: int, dest_t: int, origin_bpm: float, dest_bpm: float, count: int,  bar: float = 4.00
) -> NoteGroup:
    destgroup = NoteGroup()
    if count > 1:
        count -= 1
    stept = (dest_t - origin_t) / count
    stepbpm = (dest_bpm - origin_bpm) / count
    for i in range(count + 1):
        destgroup.append(Timing(int(origin_t + i * stept), origin_bpm + i * stepbpm, bar))
    return destgroup


def timing_easing(
        origin_t: int, dest_t: int, origin_bpm: float, dest_bpm: float, count: int,  bar: float = 4.00,
        mode: Union[Literal['s', 'b', 'si', 'so'], Callable] = 's', b_point: list=[1/3, 0, 2/3, 1]
) -> NoteGroup:
    destgroup = NoteGroup()
    deltat = dest_t - origin_t
    deltabpm = dest_bpm - origin_bpm
    stept = deltat / count

    if isinstance(mode, str):
        if mode in ['s', 'b', 'si', 'so']:
            mode = get_easing_func(mode, b_point)
        else:
            raise ValueError('Invalid mode:' + mode)
    elif isinstance(mode, Callable):
        pass
    else:
        raise ValueError('Invalid mode:' + mode)
    
    for i in range(count + 1):
            destgroup.append(Timing(
                int(origin_t + i * stept),
                origin_bpm + deltabpm * mode(i / count),
                bar
            ))

    return destgroup

def timing_easing_by_disp(
        start_t: int, stop_t: int, base_bpm: float, count: int, easing: Callable, bar: float = 4.00,
) -> NoteGroup:
    destgroup = NoteGroup()
    endur_t = stop_t - start_t
    stept = endur_t / count

    if not isinstance(easing, Callable):
        raise ValueError('Invalid mode:' + easing)
    
    def v(t: float):
        return (easing(t + 1e-6) - easing(t - 1e-6)) / (2e-6)
    # mode: x => float
    for i in range(count + 1):
        t_percent = (i * stept) / endur_t
        v_current = v(t_percent)
        bpm = v_current * base_bpm
        destgroup.append(Timing(
            int(start_t + i * stept),
            bpm,
            bar
        ))

    return destgroup
