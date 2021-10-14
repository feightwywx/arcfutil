#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from .tap import Tap
from .common_note import time_align
from ...exception import *


class Hold(Tap):
    def __init__(self, time: int, totime: int, lane: int):
        super(Hold, self).__init__(time, lane)
        self.totime = totime

    def __getitem__(self, item):
        if isinstance(item, slice):
            slicepara = self._getslicetimepara(item)
            notelist = [Hold(time, totime, self.lane) for time, totime in slicepara[0]]
            return notelist if slicepara[1] else notelist[0]
        else:
            raise AffNoteIndexError('Hold indices must be slices')

    def __len__(self):
        return self.totime - self.time

    def __str__(self):
        return 'hold({time},{totime},{lane});'.format(
            time=int(self.time), totime=int(self.totime), lane=int(self.lane))

    def __iter__(self):  # 防止意外迭代之后进入死循环
        pass

    def _getslicetimepara(self, item: slice) -> tuple:
        isreturnlist = bool(item.step is not None)
        start = item.start if item.start is not None else self.time
        stop = item.stop if item.stop is not None else self.totime
        step = item.step if item.step is not None else (stop - start)
        if stop < start:
            raise AffNoteIndexError('start time is before stop time')
        elif step < 0:
            raise AffNoteIndexError('step smaller than zero')

        paralist = []
        while start <= stop:
            totime = start + step
            if totime < stop:
                paralist.append((start, totime))
            elif totime >= stop:
                if item.stop is None:
                    paralist.append((start, stop))
                else:
                    paralist.append((start, item.stop))
            start += step
            if start == stop:
                break
        return paralist, isreturnlist

    def moveto(self, dest: int):
        time = self.time
        super().moveto(dest)
        self.totime += self.time - time
        return self

    def copyto(self, dest: int):
        alterself = self.copy()
        return alterself.moveto(dest)

    def offsetto(self, value: int):
        super(Hold, self).offsetto(value)
        self.totime += value
        return self
        
    def align(self, bpm: float, error: int = 3, lcd = 96):
        super(Hold, self).align(bpm, error, lcd)
        self.totime = time_align(self.totime, bpm, error, lcd)
        return self
