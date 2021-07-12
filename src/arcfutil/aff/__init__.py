#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .note import *
from . import parser
from . import sorter
from . import generator


# parser
def dump(notelist: NoteGroup) -> str:
    """
    Encode note objects to Arcaea format string.
    ProTip: If you want to encode a single note object, just refer itself.

    :param notelist: A list of note objects.
    :return: An Arcaea format string.
    """
    return parser.dump(notelist)


def dumps(notelist: NoteGroup, destpath: str) -> int:
    """
    Encode note objects to Arcaea fromat string, and write it to a file (usually a .aff file).
    NOTICE! If destpath point at a file which exists previously, EVERYTHING in it will be LOST!

    :param notelist: A list of note objects.
    :param destpath: Destination path of Arcaea format file.
    :return: Length of written string.
    """
    return parser.dumps(notelist, destpath)


def extends(notelist: NoteGroup, destpath: str) -> int:
    return parser.extends(notelist, destpath)


def load(affstr: str) -> NoteGroup:
    """
    Decode Arcaea format stringto note objects.

    :param affstr:
    :return: 
    """
    return parser.load(affstr)


def loads(path: str) -> NoteGroup:
    """
    Decode Arcaea format file to note objects.

    :param path: Path of .aff file.
    :return: A list of note objects.
    """
    return parser.loads(path)


def loadline(affstr: str) -> Note or NoteGroup:
    return parser.loadline(affstr)


# sorter
def sort(unsorted: NoteGroup) -> NoteGroup:
    return sorter.sort(unsorted)
