#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from musicdl import musicdl
from hanziconv import HanziConv
import glob

SONG_LIST = 'musicdl-list.txt'
SONG_DIR = 'C:\\Users\\Administrator\\Music'
SONG_EXT = 'mp3'

class MusicDl:
    def __init__(self):
        self.target_srcs = [
                    'baiduFlac', 'kugou', 'qq', 'qianqian', 
                    'migu', 'xiami', 'joox', 'yiting',
                ]
        self.config = {'logfilepath': 'musicdl.log', 'savedir': 'downloaded', 'search_size_per_source': 5, 'proxies': {}}
        self.client = musicdl.musicdl(config=self.config)

    def search(self, keyword):
        search_results = self.client.search(keyword, self.target_srcs);
        return search_results
        
    def down(self, song_name, song_artist):
        for src, results in search_results.items():
            print(src)
            for result in results:
                #print(result)
                print('songname=' + HanziConv.toSimplified(result['songname']))
                print('singers=' + HanziConv.toSimplified(result['singers']))
                if song_name.lower() == result['songname'].lower():
                    if song_artist.lower() in result['singers'].lower():
                        if SONG_EXT == result['ext'].lower():
                            #self.client.download([search_results[src][results.index(result)]])
                            self.client.download([result])
                            return
                            
if __name__ == '__main__':
    mdl = MusicDl()
    
    with open(SONG_LIST, encoding="utf8") as f_song_list:
        SONG_LIST = f_song_list.read().splitlines()
    for song in SONG_LIST:
        song_nfo = song.split(',')
        song_name = song_nfo[0]
        song_artist = song_nfo[1]
        print(song_name)
        song_filename = SONG_DIR + '\\*' + song_name + '.*'
               
        if glob.glob(song_filename):
            print('song already exist')
        else:
            search_results = mdl.search(song_name)
            mdl.down(song_name, song_artist)
