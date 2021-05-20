#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.
from copy import copy
from operator import attrgetter
from .note import *


def sort(unsorted: NoteGroup):
    sortable_timing = []
    sortable_tap = []
    sortable_hold = []
    sortable_arc = []
    sortable_camera = []
    sortable_scene = []
    sortable_group = []
    sortedlist = copy(unsorted)
    sortedlist.clear()

    for eachnote in unsorted:
        if eachnote is not None:
            if eachnote.type == 'Timing':
                sortable_timing.append(eachnote)
            elif eachnote.type == 'Tap':
                sortable_tap.append(eachnote)
            elif eachnote.type == 'Hold':
                sortable_hold.append(eachnote)
            elif eachnote.type == 'Arc':
                eachnote.skynote = sorted(eachnote.skynote)
                sortable_arc.append(eachnote)
            elif eachnote.type == 'Camera':
                sortable_camera.append(eachnote)
            elif eachnote.type == 'SceneControl':
                sortable_scene.append(eachnote)
            elif eachnote.type == 'TimingGroup':
                sortable_group.append(sort(eachnote))
    sortedlist.extend(sorted(sortable_camera, key=attrgetter('time')))
    sortedlist.extend(sorted(sortable_timing, key=attrgetter('time')))
    sortedlist.extend(sorted(sortable_scene, key=attrgetter('time')))
    sortedlist.extend(sorted(sortable_tap, key=attrgetter('time', 'lane')))
    sortedlist.extend(sorted(sortable_hold, key=attrgetter('time', 'lane', 'totime')))
    sortedlist.extend(sorted(sortable_arc, key=attrgetter('time', 'fromx', 'fromy', 'totime', 'tox', 'toy')))
    sortedlist.sort(key=attrgetter('time'))
    sortedlist.extend(sortable_group)
    return sortedlist
