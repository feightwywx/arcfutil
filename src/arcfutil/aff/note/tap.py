#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note


class Tap(Note):
    def __init__(self, time: int, lane: int):
        super(Tap, self).__init__(time)
        self.lane: int = lane

    def __str__(self):
        return '({time},{lane});'.format(time=int(self.time), lane=int(self.lane))

    def mirror(self):
        self.lane = 5 - self.lane  # Simple magic number
        return self
