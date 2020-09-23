#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import sys

import songlist
import sortassets


def man():
    print('''
    arcfutil -- a module for Arcaea files by .direwolf
    Github: https://github.com/feightwywx/arcfutil
    
    If you want to process .aff files, just add this before your own code:
    from arcfutil import aff
    
    If you want to process songlist/Arcaea song data, just run like these:
    arcfutil songassets
    arcfutil songlist
    
    For more information, check arcfutil document: https://github.com/feightwywx/arcfutil/wiki
    ''')


if __name__ == '__main__':
    realargv = sys.argv[1:]
    if realargv:
        module = realargv[0]
        if module == 'songlist':
            songlist.main(realargv)
        elif module == 'sortassets':
            sortassets.main(realargv)
        else:
            man()
    else:
        man()
