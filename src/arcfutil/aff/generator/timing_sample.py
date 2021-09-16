#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import sin
from ..note import Timing
from ..note import NoteGroup
from ..note.easing import bezier
from ..note.easing import sine
from ..note.easing import cosine


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
        mode='s', b_point: list=[1/3, 0, 2/3, 1]
) -> NoteGroup:
    destgroup = NoteGroup()
    if count > 1:
        count -= 1
    deltat = dest_t - origin_t
    deltabpm = dest_bpm - origin_bpm
    stept = deltat / count

    if mode == 's':
        stepbpm = (dest_bpm - origin_bpm) / count
        for i in range(count + 1):
            destgroup.append(Timing(int(origin_t + i * stept), origin_bpm + i * stepbpm, bar))
    elif mode == 'b':
        for i in range(count + 1):
            destgroup.append(Timing(
                int(origin_t + i * stept),
                origin_bpm + deltabpm * bezier(i / count, b_point[0], b_point[1], b_point[2], b_point[3]),
                bar
            ))
    elif mode == 'si':
        for i in range(count + 1):
            destgroup.append(Timing(
                int(origin_t + i * stept),
                origin_bpm + deltabpm * sine(i / count),
                bar
            ))
    elif mode == 'so':
        for i in range(count + 1):
            destgroup.append(Timing(
                int(origin_t + i * stept),
                origin_bpm + deltabpm * cosine(i / count),
                bar
            ))
    else:
        raise ValueError('Invalid mode:' + mode)

    return destgroup
