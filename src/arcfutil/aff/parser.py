#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from ..exception import *
from . import note
from . import sorter


def __dumpline(noteobj: note.Note):
    return str(noteobj)


def dump(notelist: note.NoteGroup):
    notelist = sorter.sort(notelist)
    return str(notelist)


def dumps(notelist: note.NoteGroup, destpath: str):
    strnotelist = dump(notelist)
    with open(destpath, 'w') as faff:
        return faff.write(strnotelist)


def extends(notelist: note.NoteGroup, destpath: str):
    notelist = sorter.sort(notelist)
    with open(destpath, 'a') as faff:
        count = 0
        if isinstance(notelist, note.TimingGroup):
            faff.write(str(notelist))
            faff.write('\n')
            count += len(str(notelist)) + 1
        else:
            for each in notelist:
                faff.write(str(each))
                faff.write('\n')
                count += len(str(each)) + 1
        return count


def __notestriter(notestr: str, termsign: str):
    return notestr[:notestr.find(termsign)]


def loadline(notestr: str):
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
        if sub_expression:  # arctap读取
            splited = sub_expression.split(',')
            skynotetimelist = [arctap[arctap.index('(') + 1:arctap.rindex(')')] for arctap in splited]
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
            fx=None if paralist[8] == 'none' else paralist[8],
            isskyline=isskyline,
            skynote=skynotetimelist
        )
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
                continue
            elif stripedlinestr.startswith('TimingPointDensityFactor'):
                notelist.desnity = float(stripedlinestr[stripedlinestr.index(':') + 1:])
                continue
            elif stripedlinestr == '};':
                notelist.append(tempstruct)
                tempstruct = None
                continue
            else:
                loadednote = loadline(stripedlinestr)
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
