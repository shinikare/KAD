import json
import urllib2
from bs4 import BeautifulSoup as Soup
#from soupselect import select

# import threads

print "Rozpoczynam prace..."

# pobranie tresci strony www
#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent','Mozilla/5.0')]
#sock = opener.open("http://wiadomosci.onet.pl/")
#htmlSource = sock.read()
#sock.close()

htmlSource = urllib2.urlopen(urllib2.Request('http://wiadomosci.onet.pl/', headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})).read()

#import urllib
#req = urllib.request.Request(url="http://localhost/",data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
#handler = urllib.request.urlopen(req)

#print htmlSource

print "-----------------"

# wyciagamy dane ze strony
zupa = Soup(htmlSource)
#elementy = zupa.findAll('<div class="itemLead hyphenate">')
#elementy = zupa.findAll('div', atrybuty={'class':'itemLead hyphenate'})
#elementy = zupa.select('div class="itemLead hyphenate')
elementy = zupa.findAll("div", {"class" : "itemLead hyphenate"})

print elementy
