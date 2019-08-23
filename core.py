'this is the core of walld, all functions should store here'
import json
import random
import os
import subprocess
import requests
import config

class Walld():
    '''this class represents almost all walld functions except trays one'''
    def __init__(self, api):
        self.filer = Filer(config.MAIN_FOLDER)
        self.api = api
        self.save_path = config.MAIN_FOLDER+'/saved/' + str(random.random())
        self.cp =
        self.desktop_environment = os.popen("env | grep DESKTOP_SESSION= \
        | awk -F= '{print $2}'").read()
        if not os.path.exists(config.MAIN_FOLDER):
            print("This installation is incorrect! can`t see "\
            + config.MAIN_FOLDER + " folder!")
            exit(1)
        print('class walld started!')

    def get_settings(self):
        '''gets list of settings'''
        return self.filer.settings

    def get_categories(self):
        '''gets a list of all categories by api method'''
        list_categories = []
        params = {"param":"categories"}
        json_answer = json.loads(requests.get(self.api, params=params).text)
        for i in json_answer:
            list_categories.append(i['category'] + '::cat_')
        return list_categories

    def save_image(self, name=False):
        '''copy image to specific(if passed) folder or to standart
        self.save_path path'''
        if name:
            subprocess.call(['/usr/bin/cp ', config.MAIN_FOLDER+'/temp.jpg ', name], shell=False)
            print('saved at ' + name)
        else:
            subprocess.call(['/usr/bin/cp ', config.MAIN_FOLDER+'/temp.jpg ', self.save_path], shell=False)
            print('saved at ' + self.save_path)

    def spin_dice(self):
        '''making a list of urls by accessing a db, than sets wall'''
        self.set_wall(download(self.get_urls()['url'],\
         config.MAIN_FOLDER+'/temp.jpg'))

    def set_wall(self, file_name):
        '''this is critical module, depending on de it sets walls'''
        if self.desktop_environment == 'xfce\n':
            mon_list = os.popen('/usr/bin/xfconf-query -c \
            xfce4-desktop -l | grep "workspace0/last-image"').read().split()
            for i in mon_list:
                os.system('/usr/bin/xfconf-query \
                --channel xfce4-desktop --property '+ i +' --set ' + file_name)
        elif self.desktop_environment == 'mate\n': #experimental
            os.system('/usr/bin/gsettings set org.mate.background\
            picture-filename'+ file_name)
        elif self.desktop_environment == 'gnome\n': #experimental
            os.system('/usr/bin/gsettings set \
            org.gnome.desktop.background picture-uri file://'+ file_name)

    def change_option(self, name, add=False):
        '''need to rewrite it'''
        self.filer.change_option(name, add)

    def get_urls(self):
        '''requests new link for wallpaper'''
        params = []
        for i in self.filer.settings['categories']:
            params.append(("category", i[:-6]))
        json_answer = json.loads(requests.get(self.api\
         + '/walls', params=params).text)
        if json_answer['success']:
            result = json_answer['content']
        else:
            print('something wrong and its on client side')
        return result

class Filer():
    '''Abstraction for files and settings'''
    def __init__(self, main_folder):
        self.main_folder = main_folder
        self.settings_file = self.main_folder + '/prefs.json'
        if not os.path.exists(self.main_folder):
            print('creating!' + self.main_folder)
            os.mkdir(self.main_folder)
        print('checking options!')
        try:
            with open(self.settings_file, 'r') as file:
                self.settings = json.load(file)
        except FileNotFoundError:
            print('file not found! creating new one')
            self.settings = {'categories':[], 'resolutions':[]}
            self.dump()

    def change_option(self, name, add=False):
        '''works with options file'''
        if add:
            print('adding', name)
            if 'cat_' in name:
                self.settings['categories'].append(name)
            elif 'res_' in name:
                self.settings['resolutions'].append(name)
            self.dump()
        else:
            print('removing', name)
            if 'cat_' in name:
                self.settings['categories'].remove(name)
            elif 'res_' in name:
                self.settings['resolutions'].remove(name)
            self.dump()

    def dump(self):
        '''this function dumps settings to file'''
        with open(self.settings_file, 'w') as temp:
            json.dump(self.settings, temp)

def download(url, file_name):
    '''downloads a file, first comes url, second comes full path of file'''
    with open(file_name, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
    return file_name
