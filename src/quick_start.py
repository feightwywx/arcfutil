#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# (c)2021 .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

from arcfutil import aff

a_normal_list = [
    aff.Timing(0, 222.22),
    aff.Tap(0, 1),
    aff.Hold(0, 100, 2),
    aff.Arc(0, 200, 0, 1, 's', 1, 0, 0, True, [0, 100, 200]),
    aff.TimingGroup(
        aff.Timing(0, 222.22),
        opt='noinput'
    )
]

afflist = aff.AffList(
    a_normal_list,
    offset=248,
    desinty=2
)

tg = aff.TimingGroup(
        aff.Timing(0, 222.22),
        opt='noinput'
    )

afflist.offsetto(200)
aff.extends(tg, '0.aff')
