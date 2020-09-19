#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from enum import Enum
from copy import deepcopy


class SlideEasing(Enum):
    b = 'b'
    s = 's'
    si = 'si'
    so = 'so'
    sisi = 'sisi'
    siso = 'siso'
    sosi = 'sosi'
    soso = 'soso'


class FX(Enum):
    none = 'none'
    full = 'full'
    incremental = 'incremental'


class ArcColor(Enum):
    blue = 0
    red = 1
    green = 2


class Note:
    def __init__(self, time: int):
        self.time: int = time
        self.type = type(self).__name__
        self._alterself = None  # Temp

    def type(self):
        return type(self).__name__


class AudioOffset(Note):  # 虽然不太合理，但还是继承了Note对象））
    def __init__(self, offset: int):
        super(AudioOffset, self).__init__(0)
        self.offset = offset

    def __repr__(self):
        return 'AudioOffset:{offset}'.format(offset=self.offset)


class Tap(Note):
    def __init__(self, time: int, lane: int):
        super(Tap, self).__init__(time)
        self.lane: int = lane

    def __repr__(self):
        return '({time},{lane});'.format(time=self.time, lane=self.lane)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself

    def mirror(self):
        self.lane = 5 - self.lane  # Simple magic number


class Hold(Tap):
    def __init__(self, time: int, totime: int, lane: int):
        super(Hold, self).__init__(time, lane)
        self.totime: int = totime
        self._alterself = deepcopy(self)

    def __repr__(self):
        return 'hold({time},{totime},{lane});'.format(time=self.time, totime=self.totime, lane=self.lane)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time += dest
        self._alterself.totime += dest - self.time
        return self._alterself


class Arc(Note):
    def __init__(self,
                 time: int,
                 totime: int,
                 fromx: float,
                 fromy: float,
                 slideeasing,
                 tox: float,
                 toy: float,
                 color,
                 isskyline: bool,
                 skynote: list,
                 fx
                 ):
        super(Arc, self).__init__(time)
        self.totime: int = totime
        self.fromx: float = fromx
        self.fromy: float = fromy
        self.tox: float = tox
        self.toy: float = toy
        self.slideeasing: SlideEasing = slideeasing
        self.color: ArcColor = color
        self.isskyline: bool = isskyline
        self.skynote: list = skynote
        self.fx: FX = fx

    def __repr__(self):
        arcstr = 'arc({time},{totime},{fromx:.2f},{fromy:.2f},{slideeasing},{tox:.2f},{toy:.2f},{color},{fx},' \
                 '{isskyline})'.format(
                    time=self.time,
                    totime=self.totime,
                    fromx=self.fromx,
                    fromy=self.fromy,
                    slideeasing=self.slideeasing.value,
                    tox=self.tox,
                    toy=self.toy,
                    color=self.color.value,
                    fx=self.fx.name,
                    isskyline='true' if self.isskyline else 'false'
                 )
        skynotestr = ''
        if self.skynote:
            for i in range(len(self.skynote)):
                eachtime = self.skynote[i]
                skynotestr += 'arctap({time})'.format(time=eachtime)
                if i != len(self.skynote) - 1:
                    skynotestr += ','
        return arcstr + ('[{0}]'.format(skynotestr) if skynotestr else '') + ';'

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        easings = {name for name, member in SlideEasing.__members__.items()}
        colors = {name for name, member in ArcColor.__members__.items()}.union(
                 {member.value for name, member in ArcColor.__members__.items()})
        fxs = {name for name, member in FX.__members__.items()}

        if type(value).__name__ != 'SlideEasing' and key == 'slideeasing':
            if value in easings:
                for each in SlideEasing:
                    if each.value == value:
                        self.__dict__[key] = each
            else:
                print('Value', value, 'is invalid. Setting Slideeasing.b.')  # TODO 抛出异常
                self.__dict__[key] = SlideEasing.b

        if type(value).__name__ != 'ArcColor' and key == 'color':
            if value in colors:
                for each in ArcColor:
                    if each.value == value:
                        self.__dict__[key] = each
                    elif each.name == value:
                        self.__dict__[key] = each
            else:
                print('Value', value, 'is invalid. Setting ArcColor.blue.')  # TODO 抛出异常
                self.__dict__[key] = ArcColor.blue

        if type(value).__name__ != 'FX' and key == 'fx':
            print(value, fxs)
            if value in fxs:
                for each in FX:
                    if each.value == value:
                        self.__dict__[key] = each
                    elif each.name == value:
                        self.__dict__[key] = each
            else:
                print('Value', value, 'is invalid. Setting FX.none.')  # TODO 抛出异常
                self.__dict__[key] = FX.none

        if key == 'skynote' and value:
            self.__dict__[key] = sorted(value)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        self._alterself.totime += dest - self.time
        return self._alterself

    def mirror(self):
        # more magic number))
        self.fromx = 1 - self.fromx
        self.tox = 1 - self.fromx


class Timing(Note):
    def __init__(self, time: int, bpm: float, bar: float):
        super(Timing, self).__init__(time)
        self.bpm: float = bpm
        self.bar: float = bar

    def __repr__(self):
        return 'timing({time},{bpm:.2f},{bar:.2f});'.format(time=self.time, bpm=self.bpm, bar=self.bar)

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself


class Camera(Note):  # TODO: Camera语句
    pass


class SceneControl(Note):  # TODO: SceneControl语句
    pass


class TimingGroup(list):
    def __init__(self, tup):
        super().__init__(tup)
        self.type = type(self).__name__

    def __getattr__(self, item):
        # 把timinggroup中第二个元素的time属性，当作整个timinggroup的属性
        # 如果timinggroup只有一个元素或者为空就返回0
        if item == 'time':
            if len(self) > 1:
                return self[1].time
            else:
                return 0

    def __repr__(self):
        group = 'timinggroup(){'
        for each in self:
            group += '\n{0}'.format(each)
        group += '\n};'
        return group

    def type(self):
        return type(self).__name__
