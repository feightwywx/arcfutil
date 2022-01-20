#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

def man():
    print('''
    arcfutil -- a module for Arcaea files by .direwolf
    Github: https://github.com/feightwywx/arcfutil

    If you want to process .aff files, just add this before your own code:
    from arcfutil import aff

    If you want to process songlist/Arcaea song data, just run these to get help:
    songassets -h
    songlist -h

    For more information, check arcfutil document: https://github.com/feightwywx/arcfutil/wiki
    ''')


def main():
    man()


if __name__ == '__main__':
    main()
