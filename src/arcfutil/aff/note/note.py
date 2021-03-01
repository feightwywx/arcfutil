#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from copy import deepcopy
from .easing import slicer
from ...exception import *

slideeasinglist = [
    'b',
    's',
    'si',
    'so',
    'sisi',
    'soso',
    'sosi',
    'soso'
]

fxlist = [
    'full',
    'incremental'
]

cameraeasinglist = [
    'qi',
    'qo',
    'l',
    'reset',
    's'
]

scenetypelist = [
    'trackshow',
    'trackhide',
    'redline',
    'arcahvdistort',
    'arcahvdebris'
]


class Note:
    def __init__(self, time: int):
        self.time = time
        self.type = type(self).__name__
        self._alterself = None  # Temp

    def moveto(self, dest: int):
        self.time = dest

    def offsetto(self, value: int):
        self.time += value

    def type(self):
        return type(self).__name__


class AudioOffset(Note):  # 虽然不太合理，但还是继承了Note对象 TODO: 之后将AudioOffset作为NoteList的属性
    def __init__(self, offset: int):
        super(AudioOffset, self).__init__(0)
        self.offset = offset

    def __str__(self):
        return 'AudioOffset:{offset}'.format(offset=int(self.offset))

    def moveto(self, dest: int):
        pass

    def offsetto(self, value: int):
        pass


class Tap(Note):
    def __init__(self, time: int, lane: int):
        super(Tap, self).__init__(time)
        self.lane: int = lane

    def __str__(self):
        return '({time},{lane});'.format(time=int(self.time), lane=int(self.lane))

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself

    def mirror(self):
        self.lane = 5 - self.lane  # Simple magic number


class Hold(Tap):
    def __init__(self, time: int, totime: int, lane: int):
        super(Hold, self).__init__(time, lane)
        self.totime = totime
        self._alterself = deepcopy(self)

    def __getitem__(self, item):
        if isinstance(item, slice):
            start = item.start if item.start else self.time
            stop = item.stop if item.stop else self.totime
            step = item.step if item.step else (stop - start)
            if stop < start:
                raise AffNoteIndexError('start time is before stop time')
            elif step < 0:
                raise AffNoteIndexError('step smaller than zero')

            notelist = []
            while start < stop:
                notelist.append(Hold(start, start + step, self.lane))
                start += step
            return notelist[0] if len(notelist) == 1 else notelist
        else:
            raise AffNoteIndexError('Hold indices must be slices')

    def __str__(self):
        return 'hold({time},{totime},{lane});'.format(
            time=int(self.time), totime=int(self.totime), lane=int(self.lane))

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time += dest
        self._alterself.totime += dest - self.time
        return self._alterself

    def moveto(self, dest: int):
        time = self.time
        super().moveto(dest)
        self.totime += self.time - time

    def offsetto(self, value: int):
        super(Hold, self).offsetto(value)
        self.totime += value


class Arc(Note):
    def __init__(self, time: int, totime: int, fromx: float, tox: float, slideeasing: str, fromy: float, toy: float,
                 color: int, isskyline: bool, skynote: list = None, fx=None):
        super(Arc, self).__init__(time)
        self.totime = totime
        self.fromx: float = fromx
        self.fromy: float = fromy
        self.tox: float = tox
        self.toy: float = toy
        self.slideeasing: str = slideeasing
        self.color: int = color
        self.isskyline: bool = isskyline
        self.skynote: list = skynote
        self.fx: str = fx

    def __getitem__(self, item):
        x_type = 's'
        y_type = 's'
        se = self.slideeasing

        if len(se) < 3 and se not in ['bb', 'bs', 'sb']:
            x_type = se
            if se == 'b':
                y_type = 'b'
        else:
            if se.startswith('b'):
                x_type = 'b'
            elif se.startswith('si'):
                x_type = 'si'
            elif se.startswith('so'):
                x_type = 'so'

            if se.endswith('b'):
                y_type = 'b'
            elif se.endswith('si'):
                y_type = 'si'
            elif se.endswith('so'):
                y_type = 'so'
        if isinstance(item, slice):
            start = item.start if item.start else self.time
            stop = item.stop if item.stop else self.totime
            step = item.step if item.step else (stop - start)
            if stop < start:
                raise AffNoteIndexError('start time is before stop time')
            elif step < 0:
                raise AffNoteIndexError('step smaller than zero')

            notelist = []
            while start < stop:
                slice_x = slicer(start + step, self.time, self.totime, self.fromx, self.tox, x_type)
                slice_y = slicer(start + step, self.time, self.totime, self.fromy, self.toy, y_type)
                notelist.append(Arc(start, start + step, self.fromx, slice_x, 's', self.fromy, slice_y, self.color,
                                    self.isskyline))
                start += step
            return notelist[0] if len(notelist) == 1 else notelist

        else:
            slice_x = slicer(item, self.time, self.totime, self.fromx, self.tox, x_type)
            slice_y = slicer(item, self.time, self.totime, self.fromy, self.toy, y_type)
            arc = deepcopy(self)
            self.fromx = slice_x
            self.fromy = slice_y
            self.tox = slice_x
            self.toy = slice_y
            return arc

    def __len__(self):
        return self.totime - self.time

    def __str__(self):
        arcstr = 'arc({time},{totime},{fromx:.2f},{tox:.2f},{slideeasing},{fromy:.2f},{toy:.2f},{color},{fx},' \
                 '{isskyline})'.format(
                  time=int(self.time), totime=int(self.totime), fromx=self.fromx, fromy=self.fromy,
                  slideeasing=self.slideeasing, tox=self.tox, toy=self.toy, color=int(self.color),
                  fx=self.fx if self.fx else 'none', isskyline='true' if self.isskyline else 'false'
                  )
        skynotestr = ''
        if self.skynote:
            for i in range(len(self.skynote)):
                eachtime = self.skynote[i]
                skynotestr += 'arctap({time})'.format(time=int(eachtime))
                if i != len(self.skynote) - 1:
                    skynotestr += ','
        return arcstr + ('[{0}]'.format(skynotestr) if skynotestr else '') + ';'

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == 'skynote' and value:
            if value:
                for each in enumerate(value):
                    value[each[0]] = int(each[1])
            self.__dict__[key] = sorted(value)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        self._alterself.totime += dest - self.time
        return self._alterself

    def moveto(self, dest: int):
        originaltime = self.time
        self.time = dest
        lasting = self.time - originaltime
        self.totime += lasting
        if self.skynote:
            for each in enumerate(self.skynote):
                self.skynote[each[0]] += lasting

    def mirror(self):
        # more magic number))
        self.fromx = 1 - self.fromx
        self.tox = 1 - self.fromx

    def offsetto(self, value: int):
        super(Arc, self).offsetto(value)
        self.totime += value
        if self.skynote:
            for each in enumerate(self.skynote):
                self.skynote[each[0]] += value


class Timing(Note):
    def __init__(self, time: int, bpm: float, bar: float = 4):
        super(Timing, self).__init__(time)
        self.bpm: float = bpm
        self.bar: float = bar

    def __str__(self):
        return 'timing({time},{bpm:.2f},{bar:.2f});'.format(time=int(self.time), bpm=self.bpm, bar=self.bar)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself


class Flick(Note):
    def __init__(self, time: int, x: float, y: float, dx: float, dy: float):
        super().__init__(time)
        self.x: float = x
        self.y: float = y
        self.dx: float = dx
        self.dy: float = dy

    def __str__(self):
        return 'flick({time},{x:.2f},{y:.2f},{dx:.2f},{dy:.2f});'.format(
            time=self.time, x=self.x, y=self.y, dx=self.dx, dy=self.dy
        )

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself


class Camera(Note):
    def __init__(self, time: int, transverse: float, bottomzoom: float, linezoom: float, steadyangle: float,
                 topzoom: float, angle: float, easing: str, lastingtime: int):
        super().__init__(time)
        self.transverse: float = transverse
        self.bottomzoom: float = bottomzoom
        self.linezoom: float = linezoom
        self.steadyangle: float = steadyangle
        self.topzoom: float = topzoom
        self.angle: float = angle
        self.easing: str = easing
        self.lastingtime = lastingtime

    def __str__(self):
        return 'camera({time},{trans:.2f},{bzoom:.2f},{lzoom:.2f},{stangle:.2f},{tzoom:.2f},{angle:.2f},{easing},' \
               '{lasting});'.format(
                time=int(self.time), trans=self.transverse, bzoom=self.bottomzoom, lzoom=self.linezoom,
                stangle=self.steadyangle, tzoom=self.topzoom, angle=self.angle, easing=self.easing,
                lasting=int(self.lastingtime))

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself


class SceneControl(Note):
    def __init__(self, time: int, scenetype: str, x: float = None, y: int = None):
        super(SceneControl, self).__init__(time)
        self.scenetype: str = scenetype
        self.x: float = x
        self.y = y

    def __str__(self):
        if self.scenetype in ['trackshow', 'trackhide']:
            return 'scenecontrol({0},{1});'.format(self.time, self.scenetype)
        elif self.scenetype in ['redline', 'arcahvdistort', 'arcahvdebris']:
            return 'scenecontrol({0},{1},{2:.2f},{3});'.format(
                int(self.time), self.scenetype, self.x, int(self.y))
        else:
            return None


class TimingGroup(list):
    def __init__(self, tup):
        super().__init__(tup)

    def __getattr__(self, item):
        # 把timinggroup中time最小且非零元素的time属性，当作整个timinggroup的属性
        # 如果timinggroup为空就返回0
        mintime = 0
        for each in self:
            if each and each.time != 0:
                if mintime == 0:
                    mintime = each.time
                elif mintime > each.time:
                    mintime = each.time
        return mintime

    def __str__(self):
        group = 'timinggroup(){'
        for each in self:
            group += '\n{0}'.format(each)
        group += '\n};'
        return group

    def moveto(self, dest: int):
        for each in self:
            if each:
                each.moveto(dest)

    def offsetto(self, value: int):
        basebpm = 0
        for each in self:
            if type(each).__name__ == 'Timing' and each.time == 0:
                basebpm = each.bpm

        for each in self:
            if each:
                each.offsetto(value)
        self.append(Timing(0, basebpm, 4))

    def type(self):
        return type(self).__name__
