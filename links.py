from taichi.base.htmlutils import *
from webscraping.pdict import PersistentDict
import simplejson, urllib

key = "pings"
cache = PersistentDict("urls.db")
#cache['2'] = html

#helper func
def allLinks(parseAllResult):
    links = []
    for lin in parseAllResult:
        links.append( getAllLinks(str(lin))[0])
    return links


def bingLinks(keyword):
    html = getHtml("http://www.bing.com/search?q="+ keyword + "&go=&form=QBLH&filt=all&qs=n&sk=&sc=8-4")
    link =  parseAll(html, 'div' , {'class':'sb_tlst'})
    return allLinks(link)



def yahooLinks(keyword):
    APP_ID = 'appid=%20RFn8O53V34FfngzZkPWYGuSn0JN8fFDN25_.cKT86Kh3eFZYX_gPc693ao_3yRL4xNE-%20&format=json' # Change this to your API key
    SEARCH_BASE = 'http://search.yahooapis.com/WebSearchService/V1/webSearch'

    def search(query, results=50, start=1, **kwargs):
        kwargs.update({
                'appid': APP_ID,
                'query': query,
                'results': results,
                'start': start,
                'output': 'json'
                })
        url = SEARCH_BASE + '?' + urllib.urlencode(kwargs)
        result = simplejson.load(urllib.urlopen(url))
        return result['ResultSet']
 
    info = search(keyword)
    results = info['Result']
    links = []
    for result in results:
        links.append(result['Url'])
    return links




    
def googleBlogLinks(keyword):
    url = 'http://blogsearch.google.com/blogsearch?q=' + keyword
    html = getHtml(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a', id=re.compile("^p-"))
    results = []
    for link in links:
        results.append(link['href'])
    return results



print googleBlogLinks(key)
