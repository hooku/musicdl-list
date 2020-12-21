#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from musicdl import musicdl
from hanziconv import HanziConv
import glob
import ntpath
import os

SONG_LIST = 'musicdl-list.txt'
SONG_DIR = 'C:\\Users\\Public\\Music'
SONG_EXT = ('mp3', 'm4a', 'flac')

class MusicDl:
    def __init__(self):
        self.target_srcs = [
                    'baiduFlac', 'kugou', 'qianqian', 
                    'migu', 'xiami', 'joox', 'yiting',
                ]
        self.config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 5, 'proxies': {}}
        self.client = musicdl.musicdl(config=self.config)

    def search(self, keyword):
        search_results = self.client.search(keyword, self.target_srcs);
        return search_results
        
    def down(self, song_name, song_artist):
        for ext in SONG_EXT:
            for src, results in search_results.items():
                for result in results:
                    #print(result)
                    print(src + ' - ' + result['songname'] + ' - ' + result['singers'] + ' - ' + result['ext'])
                    if song_name.lower() in HanziConv.toSimplified(result['songname'].lower()):
                        if song_artist.lower() in HanziConv.toSimplified(result['singers'].lower()):
                            if ext in result['ext'].lower():
                                self.client.download([result])
                                #print('matches')
                                return True
        #print('no match')
        return False
        
class MusicFilren:
    def has_song(self, song_name):
        song_files = glob.glob(SONG_DIR + '\\*')
        for song_file in song_files:
            song_file_sc = HanziConv.toSimplified(song_file)
            if song_name in song_file_sc:
                return song_file

    def rename(self, song_name):
        song_file = self.has_song(song_name)
        if song_file:
            song_filename_prefix = ntpath.basename(song_file).split('_')[0]
            song_filename_suffix = ntpath.basename(song_file).split('.')[1]
            song_filename_new = SONG_DIR + '\\' + song_filename_prefix + '_' + song_name + '.' + song_filename_suffix        
            if song_file != song_filename_new:
                print('rename ' + song_file + ' <==> ' + song_filename_new)
                os.replace(song_file, song_filename_new)
                
if __name__ == '__main__':
    mdl = MusicDl()
    mfr = MusicFilren()
    
    with open(SONG_LIST, encoding="utf8") as f_song_list:
        song_list = f_song_list.read().splitlines()
    for song in song_list:
        song_nfo = song.split(',')
        song_name = song_nfo[0]
        song_artist = song_nfo[1]
        print('song: ' + song_name)
        
        mfr.rename(song_name)

        song_filename = SONG_DIR + '\\*' + song_name + '.*'
        if glob.glob(song_filename):
            print('song already exist')
        else:
            search_results = mdl.search(song_name)
            mdl.down(song_name, song_artist)
            mfr.rename(song_name)
            pass
