#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import re
from . import note


# 正则表达式  TODO camera和scene
patt_offset = r'AudioOffset:(-*\d+)'
patt_tap = r'\((\d+),([1-4])\);'
patt_hold = r'hold\((\d+),(\d+),([1-4])\);'
patt_arc = r'arc\((\d+),(\d+),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([a-z]{1,4}),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([0-2]),' \
             r'([a-z]+),([a-z]+)\).*;'
patt_arctap = r'arctap\(([0-9]+)\)'
patt_timing = r'timing\((\d+),(-*\d+[.\d+]*),(\d+[.\d+]*)\);'
patt_camera = r''
patt_scene = r''


def dumpline(noteobj: note.Note):
    return str(noteobj)


def dump(notelist: list):
    affstr = ''
    isfirsthyphen = False
    for eachline in notelist:
        if eachline:
            affstr += (str(eachline) + '\n')
        if type(eachline).__name__ == 'AudioOffset' and not isfirsthyphen:
            affstr += '-\n'
            isfirsthyphen = True
    return affstr


def dumps(notelist: list, destpath: str):
    isfirsthyphen = False
    with open(destpath, 'w') as faff:
        for eachline in notelist:
            if eachline:
                faff.write(str(eachline) + '\n')
            if type(eachline).__name__ == 'AudioOffset' and not isfirsthyphen:
                faff.write('-\n')
                isfirsthyphen = True
    return True


def loadline(notestr: str):
    noteobj = None
    if re.match(patt_offset, notestr):
        offset = re.findall(patt_offset, notestr)[0]
        noteobj = note.AudioOffset(int(offset))
    elif re.match(patt_tap, notestr):
        notepara = re.findall(patt_tap, notestr)[0]
        noteobj = note.Tap(time=int(notepara[0]), lane=int(notepara[1]))
    elif re.match(patt_hold, notestr):
        notepara = re.findall(patt_hold, notestr)[0]
        noteobj = note.Hold(time=int(notepara[0]), totime=int(notepara[1]), lane=int(notepara[2]))
    elif re.match(patt_arc, notestr):
        notepara = re.findall(patt_arc, notestr)[0]
        noteeasing, notecolor, notefx = None, None, None
        arctap = re.findall(patt_arctap, notestr)

        # 转换为枚举类型
        for each in note.SlideEasing:
            if each.value == notepara[4]:
                noteeasing = each
        for each in note.ArcColor:
            if each.value == int(notepara[7]):
                notecolor = each
        for each in note.FX:
            if each.value == notepara[8]:
                notefx = each

        noteobj = note.Arc(time=int(notepara[0]), totime=int(notepara[1]), fromx=float(notepara[2]),
                           fromy=float(notepara[3]), tox=float(notepara[5]), toy=float(notepara[6]),
                           isskyline=bool(notepara[9]), color=notecolor, slideeasing=noteeasing, fx=notefx,
                           skynote=arctap)

        # 如果不为None就设置属性
        if noteeasing:
            noteobj.slideeasing = noteeasing
        if notecolor:
            noteobj.color = notecolor
        if notefx:
            noteobj.fx = notefx
        if arctap:
            noteobj.skynote = arctap
    elif re.match(patt_timing, notestr):
        notepara = re.findall(patt_timing, notestr)[0]
        noteobj = note.Timing(time=int(notepara[0]), bpm=float(notepara[1]), bar=float(notepara[2]))
        return noteobj

    return noteobj


def load(affstr: str):
    affnotelist = affstr.splitlines()
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
