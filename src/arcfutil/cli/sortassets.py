#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Adding support for 4.aff and video by tenshi0xx <https://github.com/tenshi0xx>
# Licensed under the MIT License.

import os
import sys
import shutil
import getopt


def dl(path, destpath=None):
    filelst = os.listdir(path)
    if destpath:
        dest = destpath
    else:
        dest = os.path.join(os.getcwd(), 'arcfutil_output')
    songcount = 0
    for each in filelst:  # each is file name
        oggpath = os.path.join(path, each)
        if not os.path.isfile(oggpath):
            continue
        namecut = each.split('_')
        if len(namecut) == 1:
            songpath = os.path.join(dest, each)
            try:
                os.makedirs(songpath)
            except FileExistsError:
                pass
            try:
                shutil.copyfile(oggpath, os.path.join(songpath, 'base.ogg'))
            except FileNotFoundError:
                print(songpath, 'may be a file. Delete it and try again.')
                continue
            for i in range(5):  # Support for 4.aff
                try:
                    affname = '{0}_{1}'.format(each, i)
                    shutil.copyfile(os.path.join(path, affname), os.path.join(songpath, '{0}.aff'.format(i)))
                except FileNotFoundError:
                    if i < 3:
                        print('{1}.aff for song {0} does not exist.'.format(each, i))
            # Copy and rename additional video files
            video_files = {
                'video_1080.mp4': f'{each}_video_1080.mp4',
                'video_720.mp4': f'{each}_video_720.mp4',
                'video_audio.ogg': f'{each}_video_audio.ogg',
                'video.mp4': f'{each}_video.mp4'
            }
            for new_name, old_name in video_files.items():
                try:
                    shutil.copyfile(os.path.join(path, old_name), os.path.join(songpath, new_name))
                except FileNotFoundError:
                    # print(f'{old_name} for song {each} does not exist.')
                    pass
            songcount += 1
    print('Processed', str(songcount), 'song(s) in dl folder.')
    print('Output path:', str(dest))


def main(argv=None):
    # TODO -o 参数指定输出目录
    # TODO -s 参数指定songs目录
    if not argv:
        argv = sys.argv
    realargv = argv[1:]
    if not len(realargv):  # Arguments not given
        man()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(realargv, 'd:h', ['dl=', 'help'])
    except getopt.GetoptError:
        man()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ['-d', '--dl']:
            if arg:
                dlpath = arg
            else:
                dlpath = os.getcwd()
            dl(dlpath)
        if opt in ['-h', '--help']:
            man()


def man():
    print(
        r'''
        arcfutil
        assets sorter

        Usage:
        arcfutil assets [-d <inputpath>] [-h]
        -d dl: Sort Arcaea dl files, to directory structure that can be read by chart maker.
            <inputpath>: Path of folder 'dl'.
        -h help: Show this help message.
        ''')


if __name__ == '__main__':
    main()
