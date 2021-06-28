#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from copy import deepcopy


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

    def type(self):
        return type(self).__name__


class NoteGroup(list):
    def __init__(self, *notes):
        list.__init__(self)
        super(NoteGroup, self).__init__()
        for each in notes:
            if isinstance(each, (list, tuple)) and not isinstance(each, NoteGroup):
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

    def type(self):
        return type(self).__name__
