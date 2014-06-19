from bs4 import BeautifulSoup
from sourselect import select
import urllib2
import re

def getOnetSource(url='http://onet.pl/'):
    """
        Download page
        @parm url
        @return bs4 object
    """
    try:
        data =  urllib2.urlopen(urllib2.Request(url, headers={
            'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
        })).read()
        return BeautifulSoup(data)
    except Exception, e:
        print e
        return None

def getAnahorsFromApi(newsfeed):
    """
        Parse source and return links
        in list
        @param newsfeed   Category name eg. wiadomosci
        @param cls  Class to find
        @return {list}
    """

    source = getOnetSource('http://www.onet.pl/_cdf/api?____presetName='+newsfeed)
    if source:
        links = []
        for anahor in   select(source, 'ul a'):
            links.append(anahor.get('href'))
        return links
    else:
        return None

def getPageWords(data):
    """
        Parse page and return words from content
        @param url Link to page
        @return {list}
    """
    data = getOnetSource(url)
    if data:
        text = ''
        for p in select(data, '#detail p.hyphenate'):
            text += re.sub(r'\n|\r|\t|\s{2,}|[,.!]', '', p.getText())+' '

        words = text.split(' ')

        """
        # parset title
        titleBox = select(data, '#mainTitle h1')
        if titleBox:
            title = re.sub(r'\n|\r|\t|\s{2,}|[,.!]', '', titleBox[0].getText()) # escape text
            words = words.union(set(title.split(' ')))
        """
        return words
    return None

def getPageDate(data):
    """
        Return page data
    """
    return None

def getOnetPage(url):
    """
        Parsing data from onet page, return tuple with
        date and word list
        @return {tuple}
    """
    data = getOnetSource(url)
    words = getPageWords(data)
    date = getPageDate(data)

    return words, date