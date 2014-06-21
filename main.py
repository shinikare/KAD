# -*- encoding: utf8 -*-

from libs.onet import getOnetSource, rankOnetPage, getAnahorsFromApi, getPageDate
from multiprocessing import Queue, Process, Value
from re import search
from codecs import open
from os import makedirs
import time

def chunkList(l, n):
    list = []
    for i in xrange(0, len(l), n):
        list.append(l[i:i+n])
    return list


def RankPage(links, queue):
    for link in links:
        data = getOnetSource(link)
        patterns = ['ABW', 'NBP', 'Wprost', 'prokuratura',
                        'śledztwo', 'Renata', 'Mazur','taśmy', 'afera']
        rank, amount = rankOnetPage(data, patterns)
        date = None
        if rank > 0.4:
            date = getPageDate(data)
            d = search(r'([0-9-]+){3,}\s([0-9:]+){3,}', date)
            if d:
                queue.put([str(rank), str(d.group(0)), str(link)])
        print rank, date, link


if __name__ == '__main__':
    links = getAnahorsFromApi('news')
    if links:
        subprocess = []
        chunks = chunkList(links, len(links)/5)

        queue = Queue()
        for chunk in chunks:
            p = Process(target=RankPage, args=(chunk, queue))
            p.start()
            subprocess.append(p)

        found = []
        for p in subprocess:
            p.join()

        while not(queue.empty()):
            l = queue.get()
            found.append(';'.join(l))

        dir = time.strftime("%x").replace('/','-')
        file = dir + '/' + time.strftime("%X").replace(':','_')+'.csv'
        try:
            makedirs(dir)
        except Exception:
            pass

        with open(file, 'w+') as f:
            for n in found:
                f.write(n+"\n")
        print 'Updated'
