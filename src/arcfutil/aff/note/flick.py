#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note


class Flick(Note):
    def __init__(self, time: int, x: float, y: float, dx: float, dy: float):
        super().__init__(time)
        self.x: float = x
        self.y: float = y
        self.dx: float = dx
        self.dy: float = dy

    def __str__(self):
        return 'flick({time},{x:.2f},{y:.2f},{dx:.2f},{dy:.2f});'.format(
            time=int(self.time), x=self.x, y=self.y, dx=self.dx, dy=self.dy
        )
