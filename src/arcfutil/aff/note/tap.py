#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note
from ...exception import *


class Tap(Note):
    def __init__(self, time: int, lane: int):
        super(Tap, self).__init__(time)
        self.lane: int = lane

    def __str__(self):
        return '({time},{lane});'.format(time=int(self.time), lane=int(self.lane))

    def __setattr__(self, key, value):
        super(Tap, self).__setattr__(key, value)
        if key == 'lane':
            if not 0 < value < 5:
                raise AffNoteValueError('invalid value {} for attribute "lane" (only accept 1~4)'.format(value))

    def mirror(self):
        self.lane = 5 - self.lane  # Simple magic number
        return self
