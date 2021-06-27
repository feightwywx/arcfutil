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
        self.extend(notes)
        self.type = type(self).__name__

    def __str__(self):
        return ''.join(str(x) + '\n' for x in self if x is not None)

    def moveto(self, dest: int):
        for each in self:
            if each is not None:
                each.moveto(dest)
        return self

    def type(self):
        return type(self).__name__
