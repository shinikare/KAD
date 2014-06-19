# -*- encoding: utf-8 -*-

from libs.onet import getAnahorsFromApi, getPageWords
from multiprocessing import Queue
import threading, sys, codecs

def chunkList(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def getWords(links, queue,i ):
    for link in links:
        words = getPageWords(link)
        if words:
            print 'Parsing link',link,'ok', len(words)
            queue.put(words)
        else:
            print 'Parsing link',link,'fail - empty set of words'


if __name__ == '__main__':
    links = getAnahorsFromApi('news')
    if links:
        amount = len(links)/5
        chunks = chunkList(links, amount)
        queue = Queue()

        processes = [] # process list to wait
        i=0
        for chunk in chunks:
            p = threading.Thread(target=getWords, args=(chunk, queue, i))
            p.daemon = True
            p.start()
            processes.append(p)

        while processes:
            processes.pop().join()


        mainSet = set ()
        for i in range(1,amount-1):
            mainSet = mainSet.union(queue.get())

        # generate csv
        outSet = set ()
        print 'Found ', len(mainSet), ' in ', amount*5
        with codecs.open('out.csv', 'w+', encoding='utf8') as f:
            for word in mainSet:
                if len(word) > 4:
                    outSet.add(word)
                    f.write(word+"\n")

        print 'Accepted ', len(outSet)
        sys.exit(0)