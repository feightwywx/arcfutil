#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from enum import Enum
from copy import deepcopy


class SlideEasing(Enum):
    b = 0
    s = 1
    si = 2
    so = 3
    sisi = 4
    siso = 5
    sosi = 6
    soso = 7


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
        self._alterself = None  # Temp

    def type(self):
        return type(self).__name__

    def copyto(self, dest: int):
        pass
        # 接下来的行为根据子类而定


class Tap(Note):
    def __init__(self, time: int, lane: int):
        super(Tap, self).__init__(time)
        self.lane: int = lane

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself

    def mirror(self):
        self.lane = 5 - self.lane  # Simple magic number


class Hold(Tap):
    def __init__(self, time: int, lane: int, totime: int):
        super(Hold, self).__init__(time, lane)
        self.totime: int = totime
        self._alterself = deepcopy(self)

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
                 tox: float,
                 toy: float,
                 slideeasing: SlideEasing = SlideEasing.b,
                 color: ArcColor = ArcColor.blue,
                 isskyline: bool = False,
                 skynote: list = None,
                 fx: FX = FX.none
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
    def __init__(self, time: int, bpm: float, bar: float = 4):
        super(Timing, self).__init__(time)
        self.bpm: float = bpm
        self.bar: float = bar

    def copyto(self, dest: int):
        self._alterself = deepcopy(self)
        self._alterself.time = dest
        return self._alterself


class Camera(Note):  # TODO: Camera语句
    pass


class SceneControl(Note):  # TODO: SceneControl语句
    pass
