from gotta import gottaHand
import sys, os

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
	    dir = sys.argv[1]

	    with open(os.path.join(dir,'config'), 'r') as f:
	        novelUrlList = f.readlines()

	    for n in novelUrlList:
	        getNovel(n, dir)


main()