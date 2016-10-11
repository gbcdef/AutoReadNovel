from gotta import gottaHand
import sys

def getNovel(url, dir):
    h = gottaHand(url, dir)
    h.checkNew()



def test():
    getNovel('http://m.biquge.la/booklist/176.html')


def main():
	if len(sys.argv) < 2:
		print 'specify working directory'
		return
	else:
	    with open('config', 'r') as f:
	        novelUrlList = f.readlines()

	    dir = sys.argv[1]
	    for n in novelUrlList:
	        getNovel(n, dir)


try:
    main()
except:
    pass

# test()