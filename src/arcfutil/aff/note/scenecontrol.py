#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note
from ...exception import *


class SceneControl(Note):
    def __init__(self, time: int, scenetype: str, x: float = None, y: int = None):
        super(SceneControl, self).__init__(time)
        self.scenetype: str = scenetype
        self.x: float = x
        self.y = y

    def __str__(self):
        if self.scenetype in ['trackshow', 'trackhide']:
            return 'scenecontrol({0},{1});'.format(self.time, self.scenetype)
        elif self.scenetype in ['redline', 'arcahvdistort', 'arcahvdebris', 'hidegroup']:
            return 'scenecontrol({0},{1},{2:.2f},{3});'.format(
                int(self.time), self.scenetype, self.x, int(self.y))
        else:
            raise AffSceneTypeError('{0} is not a valid scene type'.format(self.scenetype))
