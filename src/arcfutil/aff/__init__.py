#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .note import *
from . import parser
from . import sorter


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
