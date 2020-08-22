#!/bin/python3
"""
Main script that sits in walld_tray
and calls walld for help
PYSIMPLEGUIQT VERSION
OUTDATED!!
"""
import sys
import argparse
from PySimpleGUIQt import SystemTray, PopupGetFile
from walld_tray.core import Walld
from walld_tray.config import API

walld = Walld(API)
parser = argparse.ArgumentParser()
parser.add_argument('-c', action='store_true', help='change wallpaper')
args = parser.parse_args()

if args.c:
    print(args.c)
    walld.spin_dice()
    sys.exit()

#'Resolution', ['16:9::res_', '16:10::res_', '21:9::res_']
menu_def = ['BLANK', ['Change wallpaper', '---', '&Save',
                      'Save as...', 'Category',
                      walld.get_categories(), 'E&xit', '!master']]

TRAY = SystemTray(menu=menu_def, data_base64=config.ICON)

def make_flip(item): # сразу лезть в файл настроек и там все менять?
    '''operates with settings and updates walld_tray with dots'''
    # далее вызывать tray_update()
    if 'sca_' in item:
        place = 5

    elif "res_" in item:
        place = 7

    var = item.split('::')[2]+'::cat_'
    second = menu_def[1][place].index(var) + 1
    last = (menu_def[1][place][second].index(item))

    if '*' in item:
        if 'sca_' in item:
            menu_def[1][place][second][last] = item[1:] 
            #this is for sub cat if * in it
        elif "res_" in item:
            menu_def[1][place][menu_def[1][place].index(item)] = item[1:]
        #menu_def[1][place][menu_def[1][place].index(item)] = item[1:]
        #dont touch it dumbass
        walld.change_option(item)

    else:
        if 'sca_' in item:
            menu_def[1][place][second][last] = '*' + item
        elif "res_" in item:
            menu_def[1][place][menu_def[1][place].index(item)] = '*' + item
        walld.change_option(item, add=True)
    TRAY.Update(menu=menu_def)


def restore_settings():
    '''restores settings on startup'''
    for i in walld.get_settings()['categories']:
        for value in walld.get_settings()['categories'][i]:
            nibba = value +'::sca_::' +i
            try:
                second = menu_def[1][5].index(i+'::cat_') +1
            except ValueError:
                break
            last = (menu_def[1][5][second].index(nibba))
            menu_def[1][5][second][last] = "*" + nibba
    for i in walld.get_settings()['resolutions']:
        menu_def[1][7][menu_def[1][7].index(i)] = "*" + i
    TRAY.Update(menu=menu_def)

def tray_start():
    '''main funcrion, starts walld_tray'''
    restore_settings()
    while True:  # The event loop
        menu_item = TRAY.Read()
        print(menu_item)
        if menu_item == 'Exit':
            break

        elif menu_item == 'Save as...':
            apath = PopupGetFile('hi',
                                 save_as=True,
                                 file_types=(('PNG files', '*.png'),
                                             ('JPEG files', '*.jpg')))
            walld.save_image(apath)

        elif menu_item in ('__ACTIVATED__', 'Change wallpaper'):
            walld.spin_dice()

        elif ('cat_' in menu_item or 'res_' in menu_item or 'sca_' in menu_item):
            print('aha')
            make_flip(menu_item)

        elif menu_item == 'Save':
            walld.save_image()

tray_start()
