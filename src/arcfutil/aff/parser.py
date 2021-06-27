#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import re
from ..exception import *
from . import note
from . import sorter


# 正则表达式
patt_offset = r'AudioOffset:(-*\d+)'
patt_tap = r'\((\d+),([1-4])\);'
patt_hold = r'hold\((\d+),(\d+),([1-4])\);'
patt_arc = r'arc\((\d+),(\d+),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([a-z]{1,4}),(-*\d+[.\d+]*),(-*\d+[.\d+]*),([0-2]),' \
             r'([a-z]+),([a-z]+)\).*;'
patt_arctap = r'arctap\(([0-9]+)\)'
patt_flick = r'flick\((\d+),(-*\d+[.\d+]*),(-*\d+[.\d+]*),(-*\d+[.\d+]*),(-*\d+[.\d+]*)\);'
patt_timing = r'timing\((\d+),(-*\d+[.\d+]*),(\d+[.\d+]*)\);'
patt_camera = r'camera\((\d+),(-*\d+[.\d+]*),(-*\d+[.\d+]*),(-*\d+[.\d+]*),(-*\d+[.\d+]*),(-*\d+[.\d+]*),' \
              r'(-*\d+[.\d+]*),([a-z]+),(\d+)\);'
patt_scene = r'scenecontrol\((\d+),([a-z]+)(,(\d+[.\d+]*),(\d+))?\);'


def __dumpline(noteobj: note.Note):
    return str(noteobj)


def dump(notelist: note.NoteGroup):
    notelist = sorter.sort(notelist)
    affstr = ''
    isfirsthyphen = False
    for eachline in notelist:
        if eachline is not None:
            affstr += (str(eachline) + '\n')
        if type(eachline).__name__ == 'AudioOffset' and not isfirsthyphen:
            affstr += '-\n'
            isfirsthyphen = True
    return affstr


def dumps(notelist: note.NoteGroup, destpath: str):
    notelist = sorter.sort(notelist)
    isfirsthyphen = False
    with open(destpath, 'w') as faff:
        for eachline in notelist:
            if eachline is not None:
                faff.write(str(eachline) + '\n')
            if type(eachline).__name__ == 'AudioOffset' and not isfirsthyphen:
                faff.write('-\n')
                isfirsthyphen = True
    return True


def __serialgroup(notelist):
    tmpgroup = []
    currlen = len(notelist)
    for i in range(currlen - 1):
        if i < len(notelist) and notelist[i] == '_groupbegin_':
            notelist.pop(i)  # 扔掉初始标记
            # 哦我的上帝，这循环比隔壁苏珊阿姨的苹果派还要烂，让我直想穿皮靴狠狠踹你的屁股
            while True:
                try:
                    if notelist[i] == '_groupend_':
                        notelist.pop(i)  # 扔掉结束标记，
                        break  # 然后跳出死循环
                except IndexError:  # 没有找到timinggroup结束标记
                    pass
                tmpgroup.append(notelist[i])
                notelist.pop(i)
            notelist.insert(i, note.TimingGroup(tmpgroup))
            tmpgroup = []

    return notelist


def __notestriter(notestr: str, termsign: str):
    noteslicestr = ''
    for each in notestr:
        if each != termsign[0]:
            noteslicestr += each
            if len(notestr) > 0:
                notestr = notestr[1:]
            else:
                break
        else:
            break
    return noteslicestr


def __loadline(notestr: str):
    tempnotestr = notestr.strip()
    noteobj = None
    # 依次切割出note类型，参数，      子表达式（如果有）
    #         keyword  paralist   sub_expression
    keyword = __notestriter(tempnotestr, '(')
    tempnotestr = tempnotestr[len(keyword) + 1:]
    parastr = __notestriter(tempnotestr, ')')
    paralist = parastr.split(',')
    tempnotestr = tempnotestr[len(parastr) + 1:]
    sub_expression = __notestriter(tempnotestr, ';')
    tempnotestr = tempnotestr[len(sub_expression) + 1:]
    print(keyword, paralist, sub_expression, tempnotestr)

    if keyword == '' and paralist is not None:
        return note.Tap(
            time=int(paralist[0]),
            lane=int(paralist[1])
        )
    elif keyword == 'hold':
        return note.Hold(
            time=int(paralist[0]),
            totime=int(paralist[1]),
            lane=int(paralist[2])
        )
    elif keyword == 'arc':
        if paralist[9] == 'true':  # 是否为黑线
            isskyline = True
        else:
            isskyline = False
            if paralist[9] != 'false':
                raise AffNoteValueError
        if sub_expression is not None:
            skynotetimelist = __loadline(sub_expression.lstrip('[').rstrip(']'))
        else:
            skynotetimelist = []
        return note.Arc(
            time=int(paralist[0]),
            totime=int(paralist[1]),
            fromx=float(paralist[2]),
            tox=float(paralist[3]),
            slideeasing=paralist[4],
            fromy=float(paralist[5]),
            toy=float(paralist[6]),
            color=int(paralist[7]),
            fx=paralist[8],
            isskyline=isskyline,
            skynote=skynotetimelist
        )
    elif keyword == 'arctap':
        return paralist
    elif keyword == 'timing':
        return note.Timing(
            int(paralist[0]),
            float(paralist[1]),
            float(paralist[2])
        )
    elif keyword == 'camera':
        return note.Camera(
            time=int(paralist[0]),
            transverse=float(paralist[1]),
            bottomzoom=float(paralist[2]),
            linezoom=float(paralist[3]),
            steadyangle=float(paralist[4]),
            topzoom=float(paralist[5]),
            angle=float(paralist[6]),
            easing=paralist[7],
            lastingtime=int(paralist[8])
        )
    elif keyword == 'scenecontrol':
        scenetype = paralist[1]
        if scenetype in ['trackshow', 'trackhide']:
            return note.SceneControl(
                time=int(paralist[0]),
                scenetype=scenetype
            )
        elif scenetype in ['redline', 'arcahvdistort', 'arcahvdebris', 'hidegroup']:
            return note.SceneControl(
                time=int(paralist[0]),
                scenetype=scenetype,
                x=float(paralist[2]),
                y=int(paralist[3])
            )
        else:
            raise AffSceneTypeError
    elif keyword == 'flick':
        return note.Flick(
            time=int(paralist[0]),
            x=float(paralist[1]),
            y=float(paralist[2]),
            dx=float(paralist[3]),
            dy=float(paralist[4])
        )
    elif keyword == 'timinggroup':
        temptg = note.TimingGroup(opt=','.join(paralist))
        return temptg

    return noteobj


def load(affstr: str):
    notestrlist = affstr.splitlines()
    notelist = note.AffList()
    tempstruct = None
    for eachline in notestrlist:
        stripedlinestr = eachline.strip()
        if stripedlinestr not in ['', '-']:
            if stripedlinestr.startswith('AudioOffset:'):
                notelist.offset = int(stripedlinestr[stripedlinestr.index(':') + 1:])
            if stripedlinestr == '};':
                notelist.append(tempstruct)
                tempstruct = None
                continue

            loadednote = __loadline(stripedlinestr)
            if isinstance(loadednote, note.TimingGroup):
                if tempstruct is None:
                    tempstruct = loadednote
                else:
                    raise AffReadError('Timinggroup nesting is not allowed')
            else:
                if tempstruct is not None:
                    tempstruct.append(loadednote)
                else:
                    notelist.append(loadednote)
        else:
            continue
    return notelist


def loads(path: str):
    with open(path, mode='r') as faff:
        filestring = faff.read()
    return load(filestring)
