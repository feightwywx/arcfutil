#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

import os
import argparse


def arcade_clean(path: str):
    if not os.path.exists(path):
        print('Not a valid path: ' + path)
        return
    file_size = 0
    hit_path = []
    for root, dirs, files in os.walk(path):
        current_path_splited = os.path.split(root)
        if current_path_splited[1] in ['Autosave', 'Backup'] and current_path_splited[0].endswith('Arcade'):
            print(root)
            for file in files:
                filepath = os.path.join(root, file)
                file_size += os.path.getsize(filepath)
                hit_path.append(filepath)
    if file_size != 0:
        print('{:.2f} MB of Arcade autosave and backup files detected. Remove? (Y/n): '.format(file_size / 1024 / 1024), end='')
        if input() == 'Y':
            print('Removing Arcade autosave and backup files...')
            for file in hit_path:
                os.remove(file)
    else:
        print('Congratulations! There is nothing to clean.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        help="your chart path (which may contain Arcade folder). If not declared, use current work dir",
        default=os.getcwd()
        )
    args = parser.parse_args()
    arcade_clean(args.path)

if __name__ == '__main__':
    main()
