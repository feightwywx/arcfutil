#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import re
from .Aff import AffNote


# 正则表达式  TODO camera和scene
__patt_offset = r'AudioOffset:(-*\d+)'
__patt_tap = r'\((\d+),([1-4])\);'
__patt_hold = r'hold\((\d+),(\d+),([1-4])\);'
__patt_arc = r'arc\((\d+),(\d+),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([a-z]{1,4}),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([0-2]),([a-z]+),([a-z]+)\).*;'
__patt_arctap = r'arctap\(([0-9]+)\)'
__patt_timing = r'timing\((\d+),(-*\d+[.\d+]*),(\d+[.\d+]*)\);'
__patt_camera = r''
__patt_scene = r''


def dumpline(note: AffNote.Note):
    return str(note)


def dump(notelist: list):
    affstr = ''
    for eachline in notelist:
        if eachline:
            affstr += (str(eachline) + '\n')
        else:
            affstr += '-\n'
    return affstr


def dumps(notelist: list, destpath: str):
    with open(destpath, 'w') as faff:
        for eachline in notelist:
            if eachline:
                faff.write(str(eachline) + '\n')
            else:
                faff.write('-\n')
    return destpath


def loadline(note: str):
    noteobj = None
    if re.match(__patt_offset, note):
        offset = re.findall(__patt_offset, note)[0]
        noteobj = AffNote.AudioOffset(int(offset))
    elif re.match(__patt_tap, note):
        notepara = re.findall(__patt_tap, note)[0]
        noteobj = AffNote.Tap(time=int(notepara[0]), lane=int(notepara[1]))
    elif re.match(__patt_hold, note):
        notepara = re.findall(__patt_hold, note)[0]
        noteobj = AffNote.Hold(time=int(notepara[0]), totime=int(notepara[1]), lane=int(notepara[2]))
    elif re.match(__patt_arc, note):
        notepara = re.findall(__patt_arc, note)[0]
        noteeasing, notecolor, notefx = None, None, None
        arctap = re.findall(__patt_arctap, note)

        # 转换为枚举类型
        for each in AffNote.SlideEasing:
            if each.value == notepara[4]:
                noteeasing = each
        for each in AffNote.ArcColor:
            if each.value == notepara[7]:
                notecolor = each
        for each in AffNote.FX:
            if each.value == notepara[8]:
                notefx = each

        noteobj = AffNote.Arc(time=int(notepara[0]), totime=int(notepara[1]), fromx=float(notepara[2]),
                              fromy=float(notepara[3]), tox=float(notepara[5]), toy=float(notepara[6]),
                              isskyline=bool(notepara[9]))

        # 如果不为None就设置属性
        if noteeasing:
            noteobj.slideeasing = noteeasing
        if notecolor:
            noteobj.color = notecolor
        if notefx:
            noteobj.fx = notefx
        if arctap:
            noteobj.skynote = arctap
    elif re.match(__patt_timing, note):
        notepara = re.findall(__patt_timing, note)[0]
        noteobj = AffNote.Timing(time=int(notepara[0]), bpm=float(notepara[1]), bar=float(notepara[2]))
        return noteobj

    return noteobj


def load(aff: str):
    affnotelist = str.splitlines()
    notelist = []
    for eachline in affnotelist:
        notelist.append(loadline(eachline))
    return notelist


def loads(path: str):
    notelist = []
    with open(path, mode='r') as faff:
        for eachline in faff:
            notelist.append(loadline(eachline))
    return notelist
