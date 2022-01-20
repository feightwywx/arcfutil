#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.
import copy
import json
import shutil
import sys
import getopt
import os
from collections import OrderedDict
import time
import logging

# TODO 优化/重构
# 兄弟们，什么他妈的叫他妈的屎山啊？

sl_langkeys = (
    'en',
    'ja',
    'ko',
    'zh-Hans',
    'zh-Hant'
)

sl_daynightkeys = (
    'day',
    'night'
)

sl_singlekeys = (
    'id',
    'title_localized',
    'jacket_localized',
    'artist',
    'bpm',
    'bpm_base',
    'set',
    'purchase',
    'audioPreview',
    'side',
    'bg',
    'bg_daynight',
    'remote_dl',
    'source_localized',
    'source_copyright',
    'world_unlock',
    'no_pp',
    'byd_local_unlock',
    'songlist_hidden',
    'date',
    'version'
)

sl_singlekeys_indiff = (
    'ratingClass',
    'chartDesigner',
    'jacketDesigner',
    'jacketOverride',
    'jacket_night',
    'rating',
    'hidden_until_unlocked',
    'ratingPlus'
)

songsfolderskiplst = (
    'pack',
    'random',
    'tutorial',
    'packlist',
    'songlist',
    'unlocks'
)

intvaluelst = (
    'bpm_base',
    'audioPreview',
    'audioPreviewEnd',
    'side',
    'date',
    'rating'
)

boolvaluelst = (
    'remote_dl',
    'world_unlock',
    'no_pp',
    'ratingPlus',
    'jacketOverride',
    'hidden_until_unlocked',
    'songlist_hidden',
    'ratingPlus'
)

songfolderskiplst = (
    'base.jpg',
    'base_256.jpg'
)

LOG_FORMAT = '[%(asctime)s][%(levelname)s]%(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'


def parse_songlist(slpath: str) -> dict:
    """
    :param slpath: path of "songlist" file
    """
    sl = {}
    try:
        with open(slpath, 'r', encoding='utf-8') as f:
            sl = json.loads(f.read())
    except FileNotFoundError:
        logging.warning('Corresponding songlist not found: {0}'.format(slpath))
        exit(1)
    finally:
        if sl != {}:
            return sl
        else:
            raise FileNotFoundError


def parse_songconfig(scpath: str) -> dict:
    sc = {}
    try:
        with open(scpath, 'r', encoding='utf-8') as f:
            for line in f:
                linesplit = line.split('=')
                if len(linesplit) == 2:
                    sc[linesplit[0]] = linesplit[1][:-1]  # 去除行尾的\n
    except FileNotFoundError:
        logging.warning('Corresponding songconfig.txt not found: {0}'.format(scpath))
    finally:
        return sc


def songlist2songconfig(eachsong: dict) -> str:
    songconfig = ''
    for skey in sl_singlekeys:
        try:
            if skey == 'source_copyright':  # Compatible with Brcbeb Soulmate
                songconfig += 'copyright={0}\n'.format(eachsong['source_copyright'])
                continue

            if skey == 'no_pp':
                songconfig += 'nopp={0}\n'.format(eachsong['no_pp'])
                continue

            if skey == 'bpm':
                songconfig += 'bpm_disp={0}\n'.format(eachsong['bpm'])
                continue

            if skey == 'title_localized':
                titlekey = eachsong['title_localized']
                for eachlang in sl_langkeys:
                    if eachlang == 'en':  # English title as default
                        songconfig += 'title={0}\n'.format(titlekey[eachlang])
                    try:
                        songconfig += 'title_{0}={1}\n'.format(eachlang, titlekey[eachlang])
                    except KeyError:
                        pass
                continue

            if skey == 'jacket_localized':
                jacketkey = eachsong['jacket_localized']
                for eachlang in sl_langkeys:
                    try:
                        songconfig += 'jacket_localized_{0}={1}\n'.format(eachlang, jacketkey[eachlang])
                    except KeyError:
                        pass
                continue

            if skey == 'bg_daynight':
                bgdaynightkey = eachsong['bg_daynight']
                songconfig += 'bg_day={0}\n'.format(bgdaynightkey['day'])
                songconfig += 'bg_night={0}\n'.format(bgdaynightkey['night'])
                continue

            if skey == 'audioPreview':
                songconfig += 'pv={0}-{1}\n'.format(eachsong['audioPreview'], eachsong['audioPreviewEnd'])
                continue

            if skey == 'source_localized':
                srclocalkey = eachsong['source_localized']
                for eachlang in sl_langkeys:
                    if eachlang == 'en':
                        songconfig += 'source={0}\n'.format(srclocalkey[eachlang])
                    try:
                        songconfig += 'source_{0}={1}\n'.format(eachlang, srclocalkey[eachlang])
                    except KeyError:
                        pass
                continue

            songconfig += '{0}={1}\n'.format(skey, str(eachsong[skey]))
        except KeyError:
            pass

    for skey_indiff in sl_singlekeys_indiff:
        diff = eachsong['difficulties']
        if skey_indiff == 'ratingClass':
            continue

        if skey_indiff == 'rating':
            ratings = []
            max_ratingclass = 0
            for eachrating in diff:
                singlerate = str(eachrating['rating'])
                # 已废弃：如果有ratingPlus，在数值后添加+
                # try:
                #     if eachrating['ratingPlus']:
                #         singlerate += '+'
                # except KeyError:
                #     pass
                ratings.append(singlerate)
                max_ratingclass = eachrating['ratingClass']
            songconfig_diff = ''
            for i in range(max_ratingclass + 1):
                try:
                    songconfig_diff += ratings[i]
                    if i != max_ratingclass:  # last diff int don't have '-' after it
                        songconfig_diff += '-'
                except IndexError:
                    pass
            songconfig += 'diff={0}\n'.format(songconfig_diff)
            continue

        if skey_indiff == 'ratingPlus':
            pluses = []
            max_ratingclass = 0
            for eachrating in diff:
                if 'ratingPlus' in eachrating:
                    singleplus = bool(eachrating['ratingPlus'])
                else:
                    singleplus = False
                pluses.append(singleplus)
                max_ratingclass = eachrating['ratingClass']
            songconfig_diff = ''
            for i in range(max_ratingclass + 1):
                try:
                    if pluses[i]:
                        songconfig_diff += '1'
                    else:
                        songconfig_diff += '0'
                    if i != max_ratingclass:  # last diff int don't have '-' after it
                        songconfig_diff += '-'
                except IndexError:
                    pass
            songconfig += 'diff_plus={0}\n'.format(songconfig_diff)
            continue

        for eachdiff in diff:
            ratingclass = eachdiff['ratingClass']
            try:
                if skey_indiff == 'chartDesigner':  # Compatible with Brcbeb Soulmate
                    songconfig += 'designer_{0}={1}\n'.format(ratingclass, str(eachdiff[skey_indiff]))
                    continue
            except KeyError:
                pass

            try:
                if skey_indiff == 'jacketDesigner':
                    songconfig += 'jacketdesigner_{0}={1}\n'.format(ratingclass, str(eachdiff[skey_indiff]))
                    continue

                songconfig += '{0}_{1}={2}\n'.format(skey_indiff, ratingclass, str(eachdiff[skey_indiff]))
            except KeyError:
                pass

    return songconfig


def songconfig2songlist(eachsong: dict) -> OrderedDict:
    timestamp = int(time.time())
    songlist = OrderedDict()
    for skey in sl_singlekeys:
        try:
            if skey == 'source_copyright':  # Compatible with Brcbeb Soulmate
                songlist['source_copyright'] = eachsong['copyright']
                continue

            if skey == 'no_pp':
                songlist['no_pp'] = bool(eachsong['nopp'])
                continue

            if skey == 'bpm':
                songlist['bpm'] = eachsong['bpm_disp']
                continue

            if skey == 'title_localized':
                titlekey = {}
                try:
                    titlekey['en'] = eachsong['title']
                except KeyError:
                    pass

                for eachlang in sl_langkeys:
                    try:
                        titlekey[eachlang] = eachsong['title_{0}'.format(eachlang)]
                    except KeyError:
                        pass
                songlist['title_localized'] = titlekey
                continue

            if skey == 'jacket_localized':
                jacketkey = {}
                for eachlang in sl_langkeys:
                    try:
                        jacketkey[eachlang] = bool(eachsong['jacket_localized_{0}'.format(eachlang)])
                    except KeyError:
                        pass
                if jacketkey != {}:
                    songlist['jacket_localized'] = jacketkey
                continue

            if skey == 'bg_daynight':
                bgdaynightkey = {}
                for eachdaynight in sl_daynightkeys:
                    try:
                        bgdaynightkey[eachdaynight] = eachsong['bg_{0}'.format(eachdaynight)]
                    except KeyError:
                        pass
                    if bgdaynightkey != {}:
                        songlist['bg_daynight'] = bgdaynightkey
                continue

            if skey == 'audioPreview':
                try:
                    pvtimeslst = eachsong['pv'].split('-')
                    songlist['audioPreview'] = int(pvtimeslst[0])
                    songlist['audioPreviewEnd'] = int(pvtimeslst[1])
                except KeyError or IndexError:
                    songlist['audioPreview'] = 0
                    songlist['audioPreviewEnd'] = 0
                continue

            if skey == 'source_localized':
                srclocalkey = {}
                try:
                    srclocalkey['en'] = eachsong['source']
                except KeyError:
                    pass

                try:
                    for eachlang in sl_langkeys:
                        srclocalkey[eachlang] = eachsong['source_{0}'.format(eachlang)]
                except KeyError:
                    pass
                if srclocalkey != {}:
                    songlist['source_localized'] = srclocalkey
                continue

            if skey in intvaluelst:
                songlist[skey] = int(eachsong[skey])
            elif skey in boolvaluelst:
                songlist[skey] = bool(eachsong[skey])
            else:
                songlist[skey] = eachsong[skey]
        except KeyError:
            if skey == 'date':
                songlist[skey] = timestamp
            if skey == 'purchase':
                songlist[skey] = ''
            if skey == 'bg':
                songlist[skey] = ''
            if skey == 'side':
                songlist[skey] = 0
            if skey == 'version':
                songlist[skey] = '3.0'
            pass

    songlist_diff = []
    difficultylst = eachsong['diff'].split('-')
    try:
        pluslst = eachsong['diff_plus'].split('-')
    except KeyError:
        pluslst = None
    difficultylstlen = len(difficultylst)
    for eachratingclass in range(difficultylstlen):
        songlist_ratingclass = OrderedDict()
        currentdiff = difficultylst[eachratingclass]
        currentplus = None
        if pluslst:
            currentplus = int(pluslst[eachratingclass])
        for skey_diff in sl_singlekeys_indiff:
            try:
                if skey_diff == 'ratingClass':
                    songlist_ratingclass['ratingClass'] = eachratingclass
                    continue

                if skey_diff == 'rating':
                    if '+' in currentdiff:
                        songlist_ratingclass['rating'] = int(currentdiff[:-1])
                        songlist_ratingclass['ratingPlus'] = True
                    else:
                        songlist_ratingclass['rating'] = int(currentdiff)
                    continue

                if skey_diff == 'ratingPlus':
                    if currentplus:
                        songlist_ratingclass['ratingPlus'] = True

                if skey_diff == 'chartDesigner':
                    try:
                        songlist_ratingclass['chartDesigner'] = eachsong['designer_{0}'.format(eachratingclass)]
                    except KeyError:
                        songlist_ratingclass[skey_diff] = ''
                    try:
                        if not songlist_ratingclass['chartDesigner']:
                            songlist_ratingclass['chartDesigner'] = eachsong['designer']
                    except KeyError:
                        songlist_ratingclass[skey_diff] = ''
                    continue

                if skey_diff == 'jacketDesigner':
                    try:
                        songlist_ratingclass['jacketDesigner'] = eachsong['jacketdesigner_{0}'.format(eachratingclass)]
                    except KeyError:
                        songlist_ratingclass[skey_diff] = ''
                    try:
                        if not songlist_ratingclass['jacketDesigner']:
                            songlist_ratingclass['jacketDesigner'] = eachsong['jacketdesigner']
                    except KeyError:
                        songlist_ratingclass[skey_diff] = ''
                    continue

                if skey_diff in intvaluelst:
                    songlist_ratingclass[skey_diff] = eachsong['{0}_{1}'.format(skey_diff, int(eachratingclass))]
                elif skey_diff in boolvaluelst:
                    songlist_ratingclass[skey_diff] = eachsong['{0}_{1}'.format(skey_diff, bool(eachratingclass))]
                else:
                    songlist_ratingclass[skey_diff] = eachsong['{0}_{1}'.format(skey_diff, eachratingclass)]
            except KeyError:
                pass

        songlist_diff.append(songlist_ratingclass)

    songlist['difficulties'] = songlist_diff

    logging.debug(songlist)
    return songlist


def gen_songlist(path: str, withtempest: bool = False):
    songspath = os.path.join(path, 'songs')
    songlistpath = os.path.join(songspath, 'songlist')
    songslst = os.listdir(songspath)
    songlistsongs: list = []
    for eachsongfolder in songslst:  # eachsongfolder: str
        if eachsongfolder in songsfolderskiplst:
            continue
        eachsongpath = os.path.join(songspath, eachsongfolder, 'songconfig.txt')
        songconfig = parse_songconfig(eachsongpath)
        if songconfig != {}:
            songlistsongs.append(songconfig2songlist(songconfig))
    if withtempest:
        songlistsongs.append(
            {
                "id": "tempestissimo",
                "title_localized": {
                    "en": "Tempestissimo"
                },
                "artist": "t+pazolite",
                "bpm": "231",
                "bpm_base": 231,
                "set": "vs",
                "purchase": "vs",
                "audioPreview": 60000,
                "audioPreviewEnd": 70000,
                "side": 1,
                "bg": "tempestissimo",
                "remote_dl": True,
                "world_unlock": False,
                "byd_local_unlock": True,
                "date": 1590537605,
                "version": "3.0",
                "difficulties": [
                ]
            }
        )
    songlist = {'songs': songlistsongs}
    sl = json.dumps(songlist, ensure_ascii=False, indent=2)
    with open(songlistpath, 'w', encoding='utf-8') as slfile:
        slfile.write(sl)
    print('Song count in generated songlist: {0}'.format(len(songlist['songs'])))


def gen_songconfig(path: str):
    songspath = os.path.join(path, 'songs')
    slpath = os.path.join(path, 'songs', 'songlist')
    sl = parse_songlist(slpath)
    songs = sl['songs']
    count = 0
    for eachsong in songs:  # Generate songconfig.txt for one song
        # eachsong is dict
        if eachsong['id'] == 'tempestissimo':
            continue
        songconfig = songlist2songconfig(eachsong)
        songpath = os.path.join(songspath, eachsong['id'], 'songconfig.txt')
        altsongpath = os.path.join(songspath, eachsong['id'] + '.txt')
        try:
            with open(songpath, "w", encoding="utf-8") as scfile:
                scfile.write(songconfig)
        except FileNotFoundError:
            print('[WARN] Folder of song', eachsong['id'],
                  'does not exist. File will be wrote to /songs/{id}.txt.'.format(id=eachsong['id']))
            with open(altsongpath, "w", encoding="utf-8") as scfile:
                scfile.write(songconfig)
        count += 1
    print('Generated', count, 'songconfig(s) successfully.')


def gen_packlist(path: str, withtempest: bool = False):
    packlist_template = OrderedDict(
        [
            ('id', '__PLACEHOLDER__'),
            ('plus_character', -1),
            ('custom_banner', True),
            ('name_localized', {
                'en': '__PLACEHOLDER__'
            }),
            ('description_localized', {
                'en': '',
                'ja': ''
            })
        ]
    )
    songspath = os.path.join(path, 'songs')
    packlistpath = os.path.join(songspath, 'packlist')
    songlistpath = os.path.join(songspath, 'songlist')
    songlist = parse_songlist(songlistpath)
    packidlist = []
    packslist = []
    for each in songlist['songs']:  # each is dict
        try:
            packid = each['set']
            if withtempest and packid == 'vs':
                continue
            if packid not in packidlist:
                packidlist.append(packid)
        except KeyError as ex:
            logging.error(ex)
    for each in packidlist:  # each is str
        temppackdict = packlist_template
        temppackdict['id'] = each
        temppackdict['name_localized']['en'] = each
        packslist.append(copy.deepcopy(temppackdict))
    packlist = json.dumps({'packs': packslist}, ensure_ascii=False, indent=2)
    with open(packlistpath, 'w', encoding='utf-8') as plf:
        plf.write(packlist)
        print('Pack count in generated packlist: {0}'.format(len(packslist)))


def bg_copy(path: str):
    bgpath = os.path.join(path, 'img', 'bg')
    songspath = os.path.join(path, 'songs')
    copiedbg = []
    for song in os.listdir(songspath):
        if song in songsfolderskiplst:
            continue
        songpath = os.path.join(songspath, song)
        if os.path.isfile(songpath):
            continue
        for songfile in os.listdir(songpath):
            if songfile.endswith('.jpg') and songfile not in songfolderskiplst:
                shutil.copy(os.path.join(songpath, songfile), os.path.join(bgpath, songfile))
                copiedbg.append(songfile)
    if copiedbg:
        print('Copied background:')
        for each in copiedbg:
            print(each)
    else:
        print('[WARN] No custom background copied.')


def man():
    print(
        r'''
        arcfutil
        songlist generator

        Usage:
        arcfutil songlist [-hrpbt] <inputpath>
        inputpath: The folder which contains Arcaea assets(e.g. /songs, /img, etc.).
        -h help: Show this help message.
        -r reverse: Generate "songconfig.txt" from "songlist" file for every song.
        -p packlist: Generate "packlist"
        -b bg: copy background files to ./img/bg/ path.
        -t tempest: Generate "songlist" with song "tempestissimo".
        ''')


def main(argv=None):
    if argv is None:
        argv = sys.argv
    logging.basicConfig(filename='soulmate.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

    # flags
    withtempest = False
    withpacklist = False
    withbgcopy = False
    realargv = argv[1:]
    if not len(realargv):  # Arguments not given
        man()
        sys.exit(0)
    try:
        opts, args = getopt.getopt(realargv, 'hrpbt', ['help', 'reverse', 'packlist', 'bg', 'tempestw'])
    except getopt.GetoptError:
        sys.exit(1)

    if len(args) == 0:
        assetspath = os.getcwd()
    else:
        assetspath = args[0]

    if opts:
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                man()
                sys.exit(0)
            elif opt == '-r' or opt == '--reverse':
                logging.info('--- songconfig.txt generation begin ---')
                gen_songconfig(assetspath)
                sys.exit(0)

            if opt == '-t' or opt == '--tempest':
                withtempest = True
            if opt == '-p' or opt == '--packlist':
                withpacklist = True
            if opt == '-b' or opt == '--bg':
                withbgcopy = True
    logging.info('--- songlist generation begin ---')
    gen_songlist(assetspath, withtempest)
    if withpacklist:
        logging.info('--- packlist generation begin ---')
        gen_packlist(assetspath, withtempest)
    if withbgcopy:
        logging.info('--- bg copy begin ---')
        bg_copy(assetspath)


if __name__ == '__main__':
    main()
