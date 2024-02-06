#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from typing import Callable, Iterable, List, Literal, Union
from arcfutil.aff.note.notegroup import TimingGroup
from ..note import Arc
from ..note import NoteGroup
from ..note import SceneControl
from ..note import Timing
from ..note import Tap
from ..note import Hold
from random import randint
from ...exception import AffNoteTypeError, AffNoteValueError
from ..easing import get_ease, linear
from copy import deepcopy


def arc_crease_line(
        base: Arc,
        x_range: float,
        y_range: float,
        count: int,
        mode='m',
        easing='s'
) -> NoteGroup:
    """
    :param easing:
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
            each.slideeasing = easing
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
            arclist[i].slideeasing = easing
            arclist[i - 1].slideeasing = easing
    else:
        raise ValueError('Invalid mode:' + mode)
    return arclist


def arc_rain(original_t: int, dest_t: int, step: float, length: Union[float, None] = None, mode: Literal['s', 'e', 'eb']='s',
             x_limit: Union[List[float], None] = None, y_limit: Union[List[float], None] = None):
    # 考虑生成边界的左下角是坐标原点，之后再偏移
    # 怎么会有人用这种办法生成范围内随机数，可拓展性也太差了吧...被几年前的自己气死.jpg
    x_offset = 0
    # 如果给定了x_limit，则说明不需要预置的x偏移量
    if x_limit is None:
        if mode == 'e' or mode == 'eb':
            x_offset = 100
        else:
            x_offset = 50

    # 这位更是
    def max_x(y: int) -> int:
        if mode == 'e':
            # 右上顶点(1.25+1,1.61)
            return int(-(75/161) * y + 300)
        elif mode == 'eb':
            # 右上顶点(1.63+1,1.61)
            return int(-(27/161) * y + 300)
        else:
            return int(-0.5 * y + 200)

    def min_x(y: int) -> int:
        if mode == 'e':
            # 左上顶点(-0.25+1,1.61)
            return int(75/161 * y)
        elif mode == 'eb':
            # 左上顶点(-0.63+1,1.61)
            return int(27/161 * y)
        else:
            return int(0.5 * y)

    destgroup = NoteGroup()
    if length is None:
        length = step
    current_time = original_t
    while current_time < dest_t:
        rand_y = randint(0, 100 if mode == 's' else 161) if y_limit is None else randint(int(y_limit[0] * 100), int(y_limit[1] * 100))
        rand_x = randint(min_x(rand_y), max_x(rand_y)) if x_limit is None else randint(int(x_limit[0] * 100), int(x_limit[1] * 100))
        if dest_t - current_time <= length:  # 如果时间不足就截断
            actual_dest_t = dest_t
        else:
            actual_dest_t = int(current_time + length)
        destgroup.append(Arc(
            current_time,
            actual_dest_t,
            (rand_x - x_offset) / 100,
            (rand_x - x_offset) / 100,
            's',
            rand_y / 100,
            rand_y / 100,
            0,
            True
        ))
        current_time += step
    return destgroup


def arc_slice_by_count(arc: Arc, count: int, start: int = None, stop: int = None):
    start = start if start is not None else arc.time
    stop = stop if stop is not None else arc.totime
    if stop < start:
        raise AffNoteValueError(
            'stop time before start time'
        )
    step = (stop - start) / count
    if step < 1:
        step = 1
        count = arc.totime - arc.time
    destgroup = NoteGroup()
    for i in range(count):
        destgroup.append(Arc(
            start + i * step,
            start + (i + 1) * step,
            arc[start + i * step][0],
            arc[start + (i + 1) * step][0],
            's',
            arc[start + i * step][1],
            arc[start + (i + 1) * step][1],
            arc.color,
            arc.isskyline,
            fx=arc.fx
        ))
    return destgroup


def arc_slice_by_timing(arc: Arc, timings: Iterable):
    timepoints = {arc.time, arc.totime}
    for each in timings:
        if isinstance(each, Timing) and arc.time <= each.time <= arc.totime:
            timepoints.add(each.time)
    timepoints = sorted(timepoints)

    destgroup = NoteGroup()
    for i in range(len(timepoints) - 1):
        from_time = timepoints[i]
        to_time = timepoints[i + 1]
        from_slice = arc[from_time]
        to_slice = arc[to_time]
        temp_arc = Arc(
            from_time,
            to_time,
            from_slice[0],
            to_slice[0],
            's',
            from_slice[1],
            to_slice[1],
            arc.color,
            arc.isskyline
        )
        if arc.isskyline and arc.skynote:
            valid_skynotes = []
            for each in arc.skynote:
                if from_time <= each < to_time:
                    valid_skynotes.append(each)
                elif each == to_time and i == (len(timepoints) - 2):  # 黑线末尾的天键
                    valid_skynotes.append(each)
            temp_arc.skynote = valid_skynotes
        destgroup.append(temp_arc)
    return destgroup


def arc_animation_assist(
    arc: Union[Arc, Tap, Hold],
    start_t: int,
    stop_t: int,
    delta_x: float,
    delta_y: float,
    basebpm: float,
    easing_x: Callable = linear,
    easing_y: Callable = linear,
    infbpm: float = 999999,
    framerate: float = 60,
    fake_note_t: int = 100000,
    offset_t: int = 0,
    delta_offset_t = 0,
    easing_offset_t: Callable = linear
) -> NoteGroup:
    delta_t = 1000 / framerate
    count = int((stop_t - start_t) / delta_t)

    destgroup = NoteGroup()
    for i in range(count + 1):
        frame = TimingGroup(Timing(0, basebpm), opt='noinput')
        frame.append(SceneControl(0,'hidegroup', y=1))

        # 这一帧的起始时间
        t1 = start_t + i * delta_t
        frame.append(SceneControl(t1,'hidegroup', y=0))
        frame.append(Timing(t1, infbpm))
        frame.append(Timing(t1 + 1, 0))

        # 这一帧结束
        frame.append(Timing(t1 + 1.5 * delta_t - 1, -infbpm))  # 每帧显示1.5帧时间，防止闪烁
        frame.append(Timing(t1 + 1.5 * delta_t, 0))
        frame.append(SceneControl(t1 + 2 * delta_t, 'hidegroup', y=1))  # 隐藏时间略晚于倒退时间

        # 真正显示的假note
        actual_offset_t = fake_note_t - (
            offset_t - delta_offset_t * easing_offset_t(i / count))
        frame.append(Timing(actual_offset_t, infbpm))
        frame.append(Timing(actual_offset_t + 1, basebpm))
        temp_arc = deepcopy(arc)
        if (isinstance(arc, Arc)):
            temp_arc = temp_arc.offsetto(fake_note_t + 1)
            temp_arc.fromx += delta_x * easing_x(i / count)
            temp_arc.tox += delta_x * easing_x(i / count)
            temp_arc.fromy += delta_y * easing_y(i / count)
            temp_arc.toy += delta_y * easing_y(i / count)
            
        elif (isinstance(arc, Tap) or isinstance(arc, Hold)):
            temp_arc = temp_arc.offsetto(fake_note_t + 1)
            temp_arc.lane += delta_x * easing_x(i / count)
        
        frame.append(temp_arc)

        destgroup.append(frame)

    return destgroup


def arc_envelope(a1: Arc, a2: Arc, count: int, mode: Literal['c', 'p'] = 'c') -> NoteGroup:
    class Point:
        def __init__(self, time, position) -> None:
            self.time: int = time
            self.x: float = position[0]
            self.y: float = position[1]

    arcs: List[Arc] = [a1, a2]
    easing, color, isskyline = a1.slideeasing, a1.color, a1.isskyline
    points: List[Point] = []

    if mode == 'c':
        for i in range(count + 1):
            index = i % 2
            arc = arcs[index]
            step = (arc.totime - arc.time) / (count)
            current_time = arc.time + step * i
            points.append(Point(current_time, arc[current_time]))

        zipped = []
        for i in range(len(points) - 1):
            zipped.append((points[i], points[i+1]))

        return NoteGroup(map(lambda p: Arc(
            p[0].time, p[1].time, p[0].x, p[1].x, easing, p[0].y, p[1].y, color, isskyline
        ), zipped)
        )
    elif mode == 'p':
        zipped = zip(
            arc_slice_by_count(arcs[0], count), arc_slice_by_count(arcs[1], count)
        )
        return NoteGroup(map(lambda p: Arc(
            p[0].time, p[0].totime, p[0].fromx, p[1].tox, easing, p[0].fromy, p[1].toy, color, isskyline
        ), zipped))
    else:
        raise AffNoteValueError(f"Excepting 'c' or 'p' for 'mode', not {mode}")


def arc_straighten(arcs: NoteGroup, x: bool = False, y: bool = False, connector: bool = False) -> NoteGroup:
    result = NoteGroup([])
    if not (x or y or connector):
        print('Warning: No option used, will return origin NoteGroup')
        return arcs

    for i in range(len(arcs)):
        arc = arcs[i]
        if not isinstance(arc, Arc):
            raise AffNoteTypeError(f"Excepting 'Arc', not {type(arc).__name__}")

        if x:
            arc.tox = arc.fromx
        if y:
            arc.toy = arc.fromy
        result.append(arc)

        if connector and (i != len(arcs) - 1):
            next_arc = arcs[i+1]
            if isinstance(next_arc, Arc) and (next_arc.fromx != arc.tox or next_arc.fromy != arc.toy):
                result.append(Arc(arc.totime, arc.totime, arc.tox, next_arc.fromx, 's', arc.toy, next_arc.fromy, arc.color, arc.isskyline))

    return result


def arc_interlace(arcs: NoteGroup):
    result = NoteGroup([])
    for i in range(0, len(arcs) - 1, 2):
        if isinstance(arcs[i], Arc) and isinstance(arcs[i + 1], Arc):
            arcs[i + 1].isskyline = not arcs[i + 1].isskyline
        else: 
            raise AffNoteTypeError(f"Excepting 'Arc', not {type(arcs[i]).__name__}")
    return arcs
