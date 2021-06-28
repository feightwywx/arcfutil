#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from ..note import Timing
from ..note import NoteGroup


def timing_glitch(origin_t: int, dest_t: int, count: int, bpm_range: float) -> NoteGroup:
    destgroup = NoteGroup()
    count -= 1
    stept = (dest_t - origin_t) / count
    t = origin_t
    exactbpm = -bpm_range
    while t < dest_t:
        exactbpm = -exactbpm
        destgroup.append(Timing(t, exactbpm))
        destgroup.append(Timing(t + 1, 0))
        t += stept
    return destgroup


def timing_easing_linear(origin_t: int, dest_t: int, origin_bpm: float, dest_bpm: float, count: int) -> NoteGroup:
    destgroup = NoteGroup()
    count -= 1
    stept = (dest_t - origin_t) / count
    stepbpm = (dest_bpm - origin_bpm) / count
    for i in range(count + 1):
        destgroup.append(Timing(int(origin_t + i * stept), origin_bpm + i * stepbpm))
    return destgroup
