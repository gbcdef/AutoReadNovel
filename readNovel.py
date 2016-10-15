from gotta import gottaHand
import sys, os


def getNovel(url, path):
    h = gottaHand(url, path)
    h.checkNew()


def test():
    getNovel('http://m.biquge.la/booklist/176.html', os.getcwd())


def main():
    if len(sys.argv) < 2:
        path = os.getcwd()
    else:
        path = sys.argv[1]

    with open(os.path.join(path, 'config'), 'r') as f:
        novelUrlList = f.readlines()

    for n in novelUrlList:
        getNovel(n,path)

main()