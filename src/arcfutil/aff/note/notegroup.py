#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from math import modf
from .common_note import Note
from .common_note import NoteGroup
from .timing import Timing
from ..sorter import sort


class AffList(NoteGroup):
    def __init__(self, *notes, offset: int = 0, desnity: float = 1):
        super(AffList, self).__init__(*notes)
        self.offset: int = offset
        self.desnity: float = desnity

    def __str__(self):
        if self.desnity == 1:
            tsdfstring = None
        else:
            tsdfstring = 'TimingPointDensityFactor:'
            mod_des = modf(self.desnity)
            if mod_des[0] == 0:
                tsdfstring = 'TimingPointDensityFactor:{:d}\n'.format(int(self.desnity))
            else:
                tsdfstring = 'TimingPointDensityFactor:{:.3f}\n'.format(float(self.desnity))
        return ''.join([
            'AudioOffset:{:d}\n'.format(int(self.offset)),
            tsdfstring if tsdfstring is not None else '',
            '-\n'
        ]) + super().__str__()

    def offsetto(self, value: int):
        basebpm = 0
        for each in self:
            if isinstance(each, Timing) and each.time == 0:
                basebpm = each.bpm
        for each in self:
            if each is not None:
                each.offsetto(value)
        self.insert(0, Timing(0, basebpm, 4))
        return sort(self)


class TimingGroup(NoteGroup):
    def __init__(self, *notes, opt=None):
        super(TimingGroup, self).__init__(*notes)
        self.option = opt

    def __str__(self):
        group = 'timinggroup({0}){{'.format(str(self.option) if self.option is not None else '')
        for each in self:
            group += '\n  {0}'.format(each)
        group += '\n};'
        return group

    def append(self, __object) -> None:
        if isinstance(__object, Note):  # 禁止TimingGroup内嵌套其它NoteGroup
            super(NoteGroup, self).append(__object)
        else:
            raise TypeError('can only append Note (or its instance, not "{}") to {}'.format(
                type(__object).__name__,
                type(self).__name__
            ))

    def offsetto(self, value: int):
        basebpm = 0
        for each in self:
            if isinstance(each, Timing) and each.time == 0:
                basebpm = each.bpm
        for each in self:
            if each is not None:
                each.offsetto(value)
        self.insert(0, Timing(0, basebpm, 4))
        return sort(self)
