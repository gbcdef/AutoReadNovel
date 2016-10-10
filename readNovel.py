from gotta import gottaHand

def getNovel(url):
    # try:
    h = gottaHand(url)
    h.checkNew()
    # except:
        # print 'wrong in getNovel'


def test():
    getNovel('http://m.biquge.la/booklist/176.html')


def main():
    with open('config', 'r') as f:
        novelUrlList = f.readlines()

    for n in novelUrlList:
        getNovel(n)


# try:
#     main()
# except:
#     pass

test()