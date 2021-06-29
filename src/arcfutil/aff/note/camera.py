#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note
from . import validstrings
from ...exception import *


class Camera(Note):
    def __init__(self, time: int, transverse: float, bottomzoom: float, linezoom: float, steadyangle: float,
                 topzoom: float, angle: float, easing: str, lastingtime: int):
        super().__init__(time)
        self.transverse: float = transverse
        self.bottomzoom: float = bottomzoom
        self.linezoom: float = linezoom
        self.steadyangle: float = steadyangle
        self.topzoom: float = topzoom
        self.angle: float = angle
        self.easing: str = easing
        self.lastingtime = lastingtime

    def __str__(self):
        return 'camera({time},{trans:.2f},{bzoom:.2f},{lzoom:.2f},{stangle:.2f},{tzoom:.2f},{angle:.2f},{easing},' \
               '{lasting});'.format(
                time=int(self.time), trans=self.transverse, bzoom=self.bottomzoom, lzoom=self.linezoom,
                stangle=self.steadyangle, tzoom=self.topzoom, angle=self.angle, easing=self.easing,
                lasting=int(self.lastingtime))

    def __setattr__(self, key, value):
        super(Camera, self).__setattr__(key, value)
        if key == 'easing':
            if value not in validstrings.cameraeasinglist:
                raise AffNoteValueError('invalid value {} for attribute "easing" (only accept {})'.format(
                    value, str(validstrings.cameraeasinglist)
                ))
