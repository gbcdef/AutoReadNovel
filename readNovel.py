from gotta import gottaHand
import threading


def getNovel(url):
    try:
        h = gottaHand(url)
        h.startDaemon()
    except:
        print 'wrong in getNovel'


def test():
    getNovel('http://m.biquge.la/booklist/176.html')


def main():
    with open('config', 'r') as f:
        novelUrlList = f.readlines()
        print novelUrlList
    for novelUrl in novelUrlList:
        print novelUrl
        t = threading.Thread(target=getNovel, args=(novelUrl,))
        t.start()

main()
# try:
#     main()
# except:
#     pass
