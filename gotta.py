import requests
import time
import re
from bs4 import BeautifulSoup
import os
from urlparse import urlparse


class gottaHand():

    def __init__(self, novel_url):
        self.novel_url = novel_url
        self.up = urlparse(novel_url)
        # if failed generate soup, wait 30s and retry
        succeedFlag = self.regenSoup()
        while succeedFlag is False:
            time.sleep(30)
            succeedFlag = self.regenSoup()

        self.novel_name = self.soup.find('title').get_text().encode('utf-8')
        # use testInit to do the test thing
        # self.testInit()
        self.chapDict = {}
        for x in self.chapList:
            self.chapDict[x.get_text()] = self.up.scheme + r'://' + \
                self.up.netloc + x.a['href']

        cwd = os.getcwd()
        self.novel_dir = os.path.join(cwd, 'novels')
        if not os.path.exists(self.novel_dir):
            os.makedirs(self.novel_dir)

        self.indexPath = os.path.join(os.getcwd(), 'index.html')
        if not os.path.exists(self.indexPath):
            with open(self.indexPath, 'w') as f:
                f.write('<!DOCTYPE html>')
                f.write('<meta charset="UTF-8">')


    def startDaemon(self, interval=180):
        print 'Start watching', self.novel_name
        times = 0
        while True:
            times += 1
            print 'Checking', str(times), 'times:', self.novel_name
            if self.checkNew():
                print 'Finished checking, found new chapters.'
            else:
                if interval < 60:
                    print 'No new chapters, next check: ', interval, 'seconds later'
                else:
                    print 'No new chapters, next check: ', interval/60, 'minutes later'

            time.sleep(interval)

    def checkNew(self):
        self.regenSoup()
        hasNew = False
        for x in self.chapList:
            title = x.get_text()
            if title not in self.chapDict:
                print 'Has new chapter', title.encode('utf-8')
                tempUrl = self.up.scheme + r'://' + self.up.netloc + x.a['href']
                self.getChapContent(tempUrl)
                # rest for 2 seconds in case get same unix timestamp
                time.sleep(2)
                self.chapDict[title] = tempUrl
                hasNew = True

        return hasNew

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
        with open(self.indexPath, 'r+w') as f:
            f.read()
            f.write('\n')
            f.write('<a href=\'novels\\' + shortPath + '\'><div>' +
                    self.novel_name + ': ' + title + '</div></a>')
        # return filepath

    def regenSoup(self):
        try:
            self.response = requests.get(self.novel_url)
            if self.response.status_code == 200:
                self.soup = BeautifulSoup(self.response.content, 'html.parser')
                self.chapList = self.soup.findAll('div', {'class': 'bgg'})
                return True
            else:
                return False
        except:
            print time.time(), 'Failed connecting to', self.novel_url

    def testInit(self):
        [self.chapList.pop() for x in range(3)]
