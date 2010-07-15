from taichi.base.htmlutils import *
from webscraping.pdict import PersistentDict
import simplejson, urllib

key = "love"
cache = PersistentDict("urls.db")
#cache['2'] = html

#helper function to get all the html links from BS results
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


def googleLinks(keyword, country = "us"):


    GOOGLE_URLS = ['http://www.google.ad', 'http://www.google.ae', 'http://www.google.com.af', 'http://www.google.com.ag', 'http://www.google.com.ai', 'http://www.google.am', 'http://www.google.it.ao', 'http://www.google.com.ar', 'http://www.google.as', 'http://www.google.at', 'http://www.google.com.au', 'http://www.google.az', 'http://www.google.ba', 'http://www.google.com.bd', 'http://www.google.be', 'http://www.google.bf', 'http://www.google.bg', 'http://www.google.com.bh', 'http://www.google.bi', 'http://www.google.bj', 'http://www.google.com.bn', 'http://www.google.com.bo', 'http://www.google.com.br', 'http://www.google.bs', 'http://www.google.co.bw', 'http://www.google.com.by', 'http://www.google.com.bz', 'http://www.google.ca', 'http://www.google.cd', 'http://www.google.cf', 'http://www.google.cg', 'http://www.google.ch', 'http://www.google.ci', 'http://www.google.co.ck', 'http://www.google.cl', 'http://www.google.cm', 'http://www.google.cn', 'http://www.google.com.co', 'http://www.google.co.cr', 'http://www.google.com.cu', 'http://www.google.cz', 'http://www.google.de', 'http://www.google.dj', 'http://www.google.dk', 'http://www.google.dm', 'http://www.google.com.do', 'http://www.google.dz', 'http://www.google.com.ec', 'http://www.google.ee', 'http://www.google.com.eg', 'http://www.google.es', 'http://www.google.com.et', 'http://www.google.fi', 'http://www.google.com.fj', 'http://www.google.fm', 'http://www.google.fr', 'http://www.google.ga', 'http://www.google.ge', 'http://www.google.gg', 'http://www.google.com.gh', 'http://www.google.com.gi', 'http://www.google.gl', 'http://www.google.gm', 'http://www.google.gp', 'http://www.google.gr', 'http://www.google.com.gt', 'http://www.google.gy', 'http://www.google.com.hk', 'http://www.google.hn', 'http://www.google.hr', 'http://www.google.ht', 'http://www.google.hu', 'http://www.google.co.id', 'http://www.google.ie', 'http://www.google.co.il', 'http://www.google.im', 'http://www.google.co.in', 'http://www.google.is', 'http://www.google.it', 'http://www.google.je', 'http://www.google.com.jm', 'http://www.google.jo', 'http://www.google.co.jp', 'http://www.google.co.ke', 'http://www.google.com.kh', 'http://www.google.ki', 'http://www.google.kg', 'http://www.google.co.kr', 'http://www.google.com.kw', 'http://www.google.kz', 'http://www.google.la', 'http://www.google.com.lb', 'http://www.google.li', 'http://www.google.lk', 'http://www.google.co.ls', 'http://www.google.lt', 'http://www.google.lu', 'http://www.google.lv', 'http://www.google.com.ly', 'http://www.google.co.ma', 'http://www.google.md', 'http://www.google.me', 'http://www.google.mg', 'http://www.google.mk', 'http://www.google.ml', 'http://www.google.mn', 'http://www.google.ms', 'http://www.google.com.mt', 'http://www.google.mu', 'http://www.google.mv', 'http://www.google.mw', 'http://www.google.com.mx', 'http://www.google.com.my', 'http://www.google.co.mz', 'http://www.google.com.na', 'http://www.google.com.nf', 'http://www.google.com.ng', 'http://www.google.com.ni', 'http://www.google.ne', 'http://www.google.nl', 'http://www.google.no', 'http://www.google.com.np', 'http://www.google.nr', 'http://www.google.nu', 'http://www.google.co.nz', 'http://www.google.com.om', 'http://www.google.com.pa', 'http://www.google.com.pe', 'http://www.google.com.ph', 'http://www.google.com.pk', 'http://www.google.pl', 'http://www.google.pn', 'http://www.google.com.pr', 'http://www.google.ps', 'http://www.google.pt', 'http://www.google.com.py', 'http://www.google.com.qa', 'http://www.google.ro', 'http://www.google.ru', 'http://www.google.rw', 'http://www.google.com.sa', 'http://www.google.com.sb', 'http://www.google.sc', 'http://www.google.se', 'http://www.google.com.sg', 'http://www.google.sh', 'http://www.google.si', 'http://www.google.sk', 'http://www.google.com.sl', 'http://www.google.sn', 'http://www.google.sm', 'http://www.google.st', 'http://www.google.com.sv', 'http://www.google.td', 'http://www.google.tg', 'http://www.google.co.th', 'http://www.google.com.tj', 'http://www.google.tk', 'http://www.google.tl', 'http://www.google.tm', 'http://www.google.to', 'http://www.google.com.tr', 'http://www.google.tt', 'http://www.google.com.tw', 'http://www.google.co.tz', 'http://www.google.com.ua', 'http://www.google.co.ug', 'http://www.google.co.uk', 'http://www.google.com.uy', 'http://www.google.co.uz', 'http://www.google.com.vc', 'http://www.google.co.ve', 'http://www.google.vg', 'http://www.google.co.vi', 'http://www.google.com.vn', 'http://www.google.vu', 'http://www.google.ws', 'http://www.google.rs', 'http://www.google.co.za', 'http://www.google.co.zm', 'http://www.google.co.zw']

    base_url = randElement(GOOGLE_URLS)
    html = getHtml(base_url + "/search?hl=en&q=" + keyword +"&num=100")
    text = parseAll(html, 'h3', {'class' : 'r'})
    links = [link for link in allLinks(text) if isProperLink(link)]
    print links


    
def googleBlogLinks(keyword):
    url = 'http://blogsearch.google.com/blogsearch?q=' + keyword
    html = getHtml(url)
    soup = BeautifulSoup(html)
    links = soup.findAll('a', id=re.compile("^p-"))
    results = []
    for link in links:
        results.append(link['href'])
    return results





