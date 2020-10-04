#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from . import note
from . import parser
from . import sorter

# note
SlideEasing = note.SlideEasing
FX = note.FX
ArcColor = note.ArcColor
AudioOffset = note.AudioOffset
CameraEasing = note.CameraEasing
SceneType = note.SceneType
Tap = note.Tap
Hold = note.Hold
Arc = note.Arc
Timing = note.Timing
Camera = note.Camera
TimingGroup = note.TimingGroup


def audiooffset(offset: int):
    return note.AudioOffset(offset)


def tap(time: int, lane: int):
    return note.Tap(time, lane)


def hold(time: int, totime: int, lane: int):
    return note.Hold(time, totime, lane)


def arc(time: int, totime: int, fromx: float, tox: float, slideeasing, fromy: float, toy: float,
        color, isskyline, skynote: list = None, fx: FX = FX.none):
    return note.Arc(time, totime, fromx, fromy, slideeasing, tox, toy, color, isskyline, skynote, fx)


def timing(time: int, bpm: float, bar: float = 4):
    return note.Timing(time, bpm, bar)


def camera(time: int, transverse: float, bottomzoom: float, linezoom: float, steadyangle: float, topzoom: float,
           angle: float, easing, lastingtime: int):
    return note.Camera(time, transverse, bottomzoom, linezoom, steadyangle, topzoom, angle, easing, lastingtime)


def scenecontrol(time: int, scenetype, x: float = None, y: int = None):
    return note.SceneControl(time, scenetype, x, y)


def timinggroup(*notes):
    return TimingGroup(notes)


# parser
def dump(notelist: list) -> str:
    """
    Encode note objects to Arcaea format string.
    ProTip: If you want to encode a single note object, just refer itself.

    :param notelist: A list of note objects.
    :return: An Arcaea format string.
    """
    return parser.dump(notelist)


def dumps(notelist: list, destpath: str):
    """
    Encode note objects to Arcaea fromat string, and write it to a file (usually a .aff file).
    NOTICE! If destpath point at a file which exists previously, EVERYTHING in it will be LOST!

    :param notelist: A list of note objects.
    :param destpath: Destination path of Arcaea format file.
    :return: True when there's no exceptions.
    """
    return parser.dumps(notelist, destpath)


def load(affstr: str) -> list:
    """
    Decode Arcaea format stringto note objects.

    :param affstr:
    :return:
    """
    return parser.load(affstr)


def loads(path: str) -> list:
    """
    Decode Arcaea format file to note objects.

    :param path: Path of .aff file.
    :return: A list of note objects.
    """
    return parser.loads(path)


# sorter
def sort(unsorted: list):
    return sorter.sort(unsorted)
