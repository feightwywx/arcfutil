#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import os
import sys
import shutil

if len(sys.argv) != 1:
    os.chdir(sys.argv[1])  # read work path from argv
path = os.getcwd()
print('当前工作目录：' + path)

filelst = os.listdir(path)
filecount = len(filelst)
songcount = 0
for each in filelst:  # each is file name
    if not os.path.isfile(each):
        continue
    namecut = each.split('_')
    if len(namecut) == 1:
        songpath = os.path.join(path, '__outputfiles', each)
        try:
            os.makedirs(songpath)
        except FileExistsError:
            print('曲目 {0} 已存在。'.format(each))
        shutil.copyfile(each, os.path.join(songpath, 'base.ogg'))
        for i in range(4):
            try:
                shutil.copyfile('{0}_{1}'.format(each, i), os.path.join(songpath, '{0}.aff'.format(i)))
            except FileNotFoundError:
                if i != 3:
                    print('曲目 {0} 对应的谱面 {1}.aff 不存在。'.format(each, i))
        songcount += 1
print('处理完成。曲目数：' + str(songcount) + '。')
