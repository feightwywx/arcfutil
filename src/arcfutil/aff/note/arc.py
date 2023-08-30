#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from typing import Union, List, Callable
from ..easing import slicer
from .hold import Hold
from .common_note import NoteGroup
from .common_note import time_align
from . import validstrings
from ...exception import *


class Arc(Hold):
    def __init__(self, time: int, totime: int, fromx: float, tox: float, slideeasing: Union[str, Callable, List[Callable]], fromy: float, toy: float,
                 color: int, isskyline: bool, skynote: list = None, fx=None):
        super(Arc, self).__init__(time, totime, 1)
        self.fromx: float = fromx
        self.fromy: float = fromy
        self.tox: float = tox
        self.toy: float = toy
        self.slideeasing: Union[str, Callable, List[Callable]] = slideeasing
        self.color: int = color
        self.isskyline: bool = isskyline
        self.skynote: list = skynote
        self.fx: str = fx

    def __getitem__(self, item):
        easingtype = self.__geteasingtype()  # (x_type, y_type)
        if isinstance(item, slice):
            slicetimepara = self._getslicetimepara(item)
            slicepositionpara = self.__getslicepositionpara(slicetimepara, easingtype)
            slicepara = []
            notecount = len(slicetimepara[0])
            for i in range(notecount):
                slicepara.append(slicetimepara[0][i] + slicepositionpara[i])

            notelist = [
                Arc(time, totime, fromx, tox, 's', fromy, toy, self.color, self.isskyline)
                for time, totime, fromx, tox, fromy, toy in slicepara
            ]
            notelist = NoteGroup(notelist)
            return notelist if slicetimepara[1] else notelist[0]
        elif isinstance(item, (int, float)):
            slice_x = slicer(item, self.time, self.totime, self.fromx, self.tox, easingtype[0])
            slice_y = slicer(item, self.time, self.totime, self.fromy, self.toy, easingtype[1])
            return slice_x, slice_y

    def __str__(self):
        if isinstance(self.slideeasing, str):
            if self.slideeasing in validstrings.slideeasingexlist:
                raise AffNoteValueError(
                    'value {} for attribute "slideeasing" is not allowed to output (only {} allowed)'.format(
                        self.slideeasing, str(validstrings.slideeasinglist)
                    ))
            arcstr = 'arc({time},{totime},{fromx:.2f},{tox:.2f},{slideeasing},{fromy:.2f},{toy:.2f},{color},{fx},' \
                    '{isskyline})'.format(
                    time=int(self.time), totime=int(self.totime), fromx=self.fromx, fromy=self.fromy,
                    slideeasing=self.slideeasing, tox=self.tox, toy=self.toy, color=int(self.color),
                    fx=self.fx if self.fx else 'none', isskyline='true' if self.isskyline else 'false'
                    )
            skynotestr = ''
            if self.skynote is not None:
                for i in range(len(self.skynote)):
                    eachtime = self.skynote[i]
                    skynotestr += 'arctap({time})'.format(time=int(eachtime))
                    if i != len(self.skynote) - 1:
                        skynotestr += ','
            return arcstr + ('[{0}]'.format(skynotestr) if skynotestr else '') + ';'
        else:
            raise AffNoteValueError(f"type {type(self.slideeasing).__name__} is not allowed to output (only str allowed)")

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == 'skynote' and value is not None:
            for each in enumerate(value):
                value[each[0]] = int(each[1])
            self.__dict__[key] = sorted(value)
        elif key == 'color':
            if not 0 <= value <= 3:
                raise AffNoteValueError('invalid value {} for attribute "color" (only accept 0~3)'.format(value))
        elif key == 'slideeasing':
            if isinstance(value, str):
                exvalid = validstrings.slideeasinglist + validstrings.slideeasingexlist
                if value not in exvalid:
                    raise AffNoteValueError('invalid value {} for attribute "slideeasing" (only accept {})'.format(
                        value, str(validstrings.slideeasinglist)
                    ))
            elif isinstance(value, List):
                if len(value) != 2:
                    raise AffNoteValueError(f"attribute 'easingtype' recieved {len(value)} callable(s) in one list (excepting 2)")
                for each in value:
                    if isinstance(each, str):
                        valid = ['b', 's', 'si', 'so']
                        if each not in valid:
                            raise AffNoteValueError('invalid value {} for attribute "slideeasing" (only accept {})'.format(
                                each, str(valid)
                            ))
                    elif isinstance(each, Callable):
                        pass
                    else:
                        raise AffNoteValueError(f"invalid easing type {type(each)} for slideeasing (excepting str or callable)")
            elif isinstance(value, Callable):
                pass
            else:
                raise AffNoteValueError(f"invalid type '{type(value).__name__}' for attribute slideeasing (excepting str, Callable or List)")
        # elif key == 'fx' and value is not None:
        #     if value not in validstrings.fxlist:
        #         raise AffNoteValueError('invalid value {} for attribute "fx" (only accept {})'.format(
        #             value, str(validstrings.fxlist)
        #         ))

    def __geteasingtype(self):
        se = self.slideeasing
        if isinstance(se, str):
            x_type = 's'
            y_type = 's'

            if len(se) < 3 and se not in ['bb', 'bs', 'sb', 'ss']:
                x_type = se
                if se == 'b':
                    y_type = 'b'
            else:
                if se.startswith('b'):
                    x_type = 'b'
                elif se.startswith('si'):
                    x_type = 'si'
                elif se.startswith('so'):
                    x_type = 'so'

                if se.endswith('b'):
                    y_type = 'b'
                elif se.endswith('si'):
                    y_type = 'si'
                elif se.endswith('so'):
                    y_type = 'so'
        elif isinstance(se, Callable):
            x_type = se
            y_type = se
        elif isinstance(se, List):
            if len(se) == 2:
                x_type = se[0]
                y_type = se[1]
            else:
                raise AffNoteValueError(f"attribute 'easingtype' recieved {len(se)} function(s) in one list (excepting 2)")
        else:
            raise AffNoteValueError(f"attribute 'slideeasing' recieved a {type(self.slideeasing).__name__} (excepting str, Callable or List[Callable])")
        return x_type, y_type

    def __getslicepositionpara(self, slicetimepara, easingtype):
        sliceparalist = []
        for eachtime in slicetimepara[0]:  # 对每组时间求位置
            slicefromtime = eachtime[0]
            slicetotime = eachtime[1]
            slice_fromx = slicer(slicefromtime, self.time, self.totime, self.fromx, self.tox, easingtype[0])
            slice_fromy = slicer(slicefromtime, self.time, self.totime, self.fromy, self.toy, easingtype[1])
            slice_tox = slicer(slicetotime, self.time, self.totime, self.fromx, self.tox, easingtype[0])
            slice_toy = slicer(slicetotime, self.time, self.totime, self.fromy, self.toy, easingtype[1])
            sliceparalist.append((slice_fromx, slice_tox, slice_fromy, slice_toy))
        return sliceparalist

    def moveto(self, dest: int):
        offset = dest - self.time
        super(Arc, self).moveto(dest)
        if self.skynote:
            for each in enumerate(self.skynote):
                self.skynote[each[0]] += offset
        return self

    def mirror(self):
        # more magic number))
        self.fromx = 1 - self.fromx
        self.tox = 1 - self.tox
        return self

    def vmirror(self):
        # more magic number))
        self.fromy = 1 - self.fromy
        self.toy = 1 - self.toy
        return self

    def offsetto(self, value: int):
        super(Arc, self).offsetto(value)
        if self.skynote:
            for each in enumerate(self.skynote):
                self.skynote[each[0]] += value
        return self
        
    def align(self, bpm: float, error: int = 3, lcm = 96):
        super(Arc, self).align(bpm, error, lcm)
        # 防止单天键出 bug
        if self.time == self.totime:
            if self.skynote:
                self.totime += 1
        
        if self.skynote:
            for each in enumerate(self.skynote):
                self.skynote[each[0]] = time_align(self.skynote[each[0]], bpm, error, lcm)
        return self
    
    def transfer(self, x_value: float, y_value: float):
        self.fromx += x_value
        self.tox += x_value
        self.fromy += y_value
        self.toy += y_value
        return self
