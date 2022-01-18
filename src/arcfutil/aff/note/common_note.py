#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from copy import deepcopy
from typing import Iterable


def time_align(time: int, bpm: float, error: int = 3, lcd = 96):
    fpb = 60000 * 4 / bpm / lcd
    alignedTime = 0
    atime1 = round(time//fpb*fpb) #向下取grid时间戳
    atime2 = round((time//fpb+1)*fpb) #向上取grid时间戳
    abs1 = abs(time - atime1) #atime1与time的距离
    abs2 = abs(time - atime2)
    ok1 = (abs1 <= error) #abs1是否在容差内
    ok2 = (abs2 <= error)
    if ok1 & ok2:
        #哪个距离小就用哪个
        if abs1 > abs2:
            ok1 = 0
    
    if ok1:
        alignedTime = atime1
    elif ok2:
        alignedTime = atime2
    else:
        #都不能用那就不动它吧
        alignedTime = time
    
    return alignedTime

class Note:
    def __init__(self, time: int):
        self.time = time
        self.type = type(self).__name__

    def moveto(self, dest: int):
        self.time = dest
        return self

    def copy(self):
        return deepcopy(self)

    def copyto(self, dest):
        alterself = self.copy()
        return alterself.moveto(dest)

    def mirror(self):
        pass

    def offsetto(self, value: int):
        self.time += value
        return self
        
    def align(self, bpm: float, error: int = 3, lcd = 96):
        self.time = time_align(self.time, bpm, error, lcd)
        return self
        

class NoteGroup(list):
    def __init__(self, *notes):
        list.__init__(self)
        super(NoteGroup, self).__init__()
        for each in notes:
            if isinstance(each, Iterable) and type(each).__name__ != 'TimingGroup':
                self.extend(each)
            else:
                self.append(each)
        self.type = type(self).__name__

    def __str__(self):
        return ''.join(str(x) + '\n' for x in self if x is not None)

    def append(self, __object) -> None:
        if isinstance(__object, (Note, NoteGroup)):
            super(NoteGroup, self).append(__object)
        else:
            raise TypeError('can only append Note or NoteGroup (or their instances, not "{}") to {}'.format(
                type(__object).__name__,
                type(self).__name__
            ))

    def extend(self, __iterable) -> None:
        if isinstance(__iterable, NoteGroup):
            super(NoteGroup, self).extend(__iterable)
        else:
            for each in __iterable:  # 如果容器不可信，则用含有类型检查的self.append()代替self.extend()
                self.append(each)

    def moveto(self, dest: int):
        for each in self:
            if each is not None:
                each.moveto(dest)
        return self
        
    def mirror(self):
        for each in self:
            if each is not None:
                each.mirror()
        return self

    def align(self, bpm: float, error: int = 3, lcd = 96):
        for each in self:
            if each is not None:
                each.align(bpm, error, lcd)
        return self
