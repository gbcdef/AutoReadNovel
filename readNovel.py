from multiprocessing import Process
from gotta import gottaHand
# import threading
import time


def getNovel(url):
    try:
        h = gottaHand(url)
        h.startDaemon(600)
    except:
        print 'wrong in getNovel'


def test():
    getNovel('http://m.biquge.la/booklist/176.html')


def main():
    with open('config', 'r') as f:
        novelUrlList = f.readlines()
        print novelUrlList

    l = len(novelUrlList)
    for novelUrl in novelUrlList :
        p = Process(target=getNovel, args=(novelUrl,))
        p.start()
        # t = threading.Thread(target=getNovel, args=(novelUrl,))
        # t.start()
        time.sleep(5)

try:
    main()
except:
    pass
