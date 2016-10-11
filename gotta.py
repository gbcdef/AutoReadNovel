import requests
import time
import re
from bs4 import BeautifulSoup
import os
from urlparse import urlparse
import json

class gottaHand():

    def __init__(self, novel_url, cwd):
        self.novel_url = novel_url
        self.up = urlparse(novel_url)
        # if failed generate soup, wait 30s and retry
        succeedFlag = self.regenChapList()
        while succeedFlag is False:
            time.sleep(30)
            succeedFlag = self.regenChapList()

        self.novel_name = self.soup.find('title').get_text().encode('utf-8')
        # use testInit to do the test thing
        # self.testInit()


        # cwd = os.getcwd()
        self.novel_dir = os.path.join(cwd, 'novels')
        if not os.path.exists(self.novel_dir):
            os.makedirs(self.novel_dir)

        # init cfgs dir
        self.cfgs_dir = os.path.join(cwd,'cfgs')
        if not os.path.exists(self.cfgs_dir):
            os.makedirs(self.cfgs_dir)

        # init cfg path
        self.cfgPath = os.path.join(self.cfgs_dir, self.novel_name)
        # self.write_cfg(self.chapDict)
        # init index.html
        self.indexPath = os.path.join(cwd, 'index.html')
        if not os.path.exists(self.indexPath):
            with open(self.indexPath, 'w') as f:
                f.write('<!DOCTYPE html>')
                f.write('<meta charset="UTF-8">')

    def write_cfg(self, arg):
        with open(self.cfgPath, 'w') as f:
            json.dump(self.chapDict, f)

    def read_cfg(self):
        with open(self.cfgPath, 'r') as f:
            j = json.load(f)

        return j

    def checkNew(self):
        succeedFlag = self.regenChapList()
        while succeedFlag is False:
            time.sleep(30)
            succeedFlag = self.regenChapList()

        if os.path.exists(self.cfgPath):
            self.chapDict = self.read_cfg()
        else:
            self.chapDict = {}
            for x in self.chapList:
                self.chapDict[x.get_text()] = self.up.scheme + r'://' + self.up.netloc + x.a['href']

        hasNew = False
        for x in self.chapList:
            title = x.get_text()
            if title not in self.chapDict:
                print 'Has new chapter', title
                tempUrl = self.up.scheme + r'://' + self.up.netloc + x.a['href']
                self.getChapContent(tempUrl)
                # rest for 2 seconds in case get same unix timestamp
                time.sleep(2)
                self.chapDict[title] = tempUrl
                hasNew = True

        self.write_cfg(self.chapDict)
        if hasNew:
            pass
        else:
            print 'No new chapters, finished check at', time.ctime()


    def getChapContent(self, tempUrl):
        r = requests.get(tempUrl)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find(id='nr_title').get_text().encode('utf-8')
        content = soup.find(id='nr1').prettify().encode('utf-8')
        content = re.sub('\n+', '\n', content)
        content = re.sub(' +', ' ', content)
        # create html for this chapter
        filepath = os.path.join(self.novel_dir, str(int(time.time()))) + '.html'
        with open(filepath, 'w') as f:
            f.write('<!DOCTYPE html>')
            f.write('<meta charset="utf-8">')
            f.write('<title>' + title + '</title>')
            f.write('<body><article>')
            f.write('<h1>' + title + '</h1>')
            f.write('<p>' + time.ctime() + '</p>')
            f.write(content)
            f.write('</article></body>')

        shortPath = os.path.basename(filepath)
        with open(self.indexPath, 'a') as f:
            f.write('\n')
            f.write('<a href=\'novels\\' + shortPath + '\'><div>' +
                    self.novel_name + ': ' + title + '</div></a>')
        # return filepath

    def regenChapList(self):
        try:
            self.response = requests.get(self.novel_url)
            if self.response.status_code == 200:
                self.soup = BeautifulSoup(self.response.content, 'html.parser')
                self.chapList = self.soup.findAll('div', {'class': 'bgg'})
                return True
            else:
                return False
        except:
            return False

    def testInit(self):
        [self.chapList.pop() for x in range(3)]
