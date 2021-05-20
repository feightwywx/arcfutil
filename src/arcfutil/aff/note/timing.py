#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note


class Timing(Note):
    def __init__(self, time: int, bpm: float, bar: float = 4):
        super(Timing, self).__init__(time)
        self.bpm: float = bpm
        self.bar: float = bar

    def __str__(self):
        return 'timing({time},{bpm:.2f},{bar:.2f});'.format(time=int(self.time), bpm=self.bpm, bar=self.bar)
