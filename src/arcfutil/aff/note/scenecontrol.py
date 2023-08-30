#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .common_note import Note
from . import validstrings
from ...exception import *

# TODO 自定义scenecontrol支持
class SceneControl(Note):
    def __init__(self, time: int, scenetype: str, x: float = 0, y: int = 0):
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

    def __setattr__(self, key, value):
        super(SceneControl, self).__setattr__(key, value)
        if key == 'scenetype':
            if value not in validstrings.scenetypelist:
                raise AffNoteValueError('invalid value {} for attribute "scenetype" (only accept {})'.format(
                    value, str(validstrings.scenetypelist)
                ))
