# -*- encoding: utf-8 -*-
import json
from libs.onet import getAnahorsFromApi, getPageWords
from multiprocessing import Process
import threading, sys, codecs, time, os

def chunkList(l, n):
    list = []
    for i in xrange(0, len(l), n):
        list.append(l[i:i+n])
    return list

def getWords(links, i ):
    wl = []
    for link in links:
        words = getPageWords(link)
        if words:
            print 'Parsing link',link,'ok', len(words)
            wl+=words
        else:
            print 'Parsing link',link,'fail - empty set of words'
    #queue.put([1,2,3], False)
    with codecs.open('out/process-'+str(i)+'.json', 'w+') as f:
        json.dump(wl, f)
    print 'Found ', len(wl)
    return(0)

if __name__ == '__main__':
    links = getAnahorsFromApi('news')
    if links:
        amount = len(links)/5
        chunks = chunkList(links, amount)
        try:
            os.makedirs('out')
        except Exception:
            pass

        print 'Starting ', len(chunks)
        subprocess = [] # process list to wait
        i=0
        for chunk in chunks:
            p = Process(target=getWords, args=(chunk, i))
            p.start()
            subprocess.append(p)
            i+=1

        time.sleep(5)
        for p in subprocess:
            p.join()                    

        mainList = []
        for i in range(len(chunks)-1):
            with codecs.open('out/process-'+str(i)+'.json', 'r') as f:
                mainList += json.load(f)

        print 'Excluding repeated words'
        mainSet = set(mainList)

        # generate csv
        outSet = []
        print 'Found ', len(mainSet), ' in ', amount*5
        with codecs.open('out.csv', 'w+', encoding='utf8') as f:
            for word in mainSet:
                if len(word) > 4:
                    outSet.append(word)
                    f.write(word+"\n")

        print 'Accepted ', len(outSet)
