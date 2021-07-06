#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from ..note import Arc
from ..note import NoteGroup
from random import randint


def arc_crease_line(
        base: Arc,
        x_range: float,
        y_range: float,
        count: int,
        mode='m'
) -> NoteGroup:
    """
    :param base:
    :param x_range:
    :param y_range:
    :param count:
    :param mode: 'm' for regarding base arc as median,
                 'b' for regarding base arc as border.
    :return:
    """
    each_len = (base.totime - base.time) / count
    arclist = NoteGroup(base[::each_len])
    currentx = base.fromx
    currenty = base.fromy
    if mode == 'm':
        for each in arclist:
            each.fromx = currentx
            each.fromy = currenty
            each.tox += x_range
            each.toy += y_range
            x_range = -x_range
            y_range = -y_range
            currentx = each.tox
            currenty = each.toy
    elif mode == 'b':
        for i in range(1, len(arclist), 2):
            arclist[i].fromx += x_range
            arclist[i - 1].tox += x_range
            arclist[i].fromy += y_range
            arclist[i - 1].toy += y_range
    else:
        raise ValueError('Invalid mode:' + mode)
    return arclist


def arc_rain(original_t: int, dest_t: int, step: int):
    def max_x(y: int) -> int:
        return int(-0.5 * y + 200)

    def min_x(y: int) -> int:
        return int(0.5 * y)

    destgroup = NoteGroup()

    for current_time in range(original_t, dest_t, step):
        rand_y = randint(0, 100)
        rand_x = randint(min_x(rand_y), max_x(rand_y))
        destgroup.append(Arc(
            current_time,
            current_time + step,
            (rand_x - 50) / 100,
            (rand_x - 50) / 100,
            's',
            rand_y / 100,
            rand_y / 100,
            0,
            True
        ))
    return destgroup


def arc_slice_by_count(arc: Arc, count: int, start: int = None, stop: int = None):
    start = start if start is not None else arc.time
    stop = stop if stop is not None else arc.totime
    step = int((stop - start) / count)
    return arc[start:stop:step]
