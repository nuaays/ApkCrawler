#coding:utf-8

import os, sys, time, random, json
import re, requests, urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup  

# http://app.mi.com/topList?page=1
# http://app.mi.com/topList?page=42

USER_AGENTS = (
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.1",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'
)

def getURLContent(url='http://app.mi.com/topList?page=1'):
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://app.mi.com/topList',
               'Cookie':'JSESSIONID=aaaWYqTT3MMdVfeRHjMev; __utma=127562001.883425548.1452953270.1452953270.1452953270.1; __utmc=127562001; __utmz=127562001.1452953270.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'     
               }

    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0" #USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]

    try:
        r = requests.get(url, headers=headers, timeout=1)
        r.raise_for_status()
    except requests.RequestException as e:
        print e
        return None
    else:
        print r.encoding
        return r.content

def getURL(url):
    print "[Download]%s" % url
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://app.mi.com/topList'        
               }
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0"

    try:
        r = requests.get(url, headers=headers, timeout=1)
        r.raise_for_status()
    except requests.RequestException as e:
        print e
        return None
    else:
    	print r.encoding
        return r

def write2file(filename, requestshandle):
    if not requestshandle:
        print "[ERROR] No available requests", requestshandle
    else:
        with open(filename, "wb+") as fp:
            fp.write(requestshandle.content)

def append2file(filename, string):
	with open(filename, "a+") as fp:
            fp.write(string)
            fp.write("\n")


def fetchApkinfoFromWebpage(weburl="http://app.mi.com/topList?page=1"):
    apklist = []
    html_doc = getURLContent(weburl)
    soup = BeautifulSoup(html_doc, from_encoding="utf-8") 
    for item in soup.findAll(attrs={"class":"applist"})[0]:
        #print item
        item_soup = BeautifulSoup(str(item))
        #http://file.market.xiaomi.com/thumbnail/PNG/l62/AppStore/0a4e5f4d25ff24f2237ba83be3dd43205cbf1b5b4
        #http://file.market.xiaomi.com/thumbnail/PNG/l114/AppStore/0a4e5f4d25ff24f2237ba83be3dd43205cbf1b5b4
        apk_icon = apk_name = item_soup.find_all('img')[0].get('data-src')
        apk_name_cn = item_soup.find_all('h5')[0].get_text() #item_soup.find_all('a')[-2].get_text() #item_soup.find_all('h5')[0].get_text() ##apk_name = item_soup.find_all('img')[0].get('alt').encode('utf-8')
        apk_webpage = "http://app.mi.com" + item_soup.find_all('a')[0].get('href')
        apk_id = apk_webpage.split("/")[-1]
        apk_url = get_apk_real_downloadurl(apk_id)
        #apk_name_en = BeautifulSoup(getURLContent(apk_webpage)).findAll(attrs={"class":"special-li"})[0].get_text()
        apk_name_en = apk_url.split("/")[-1].replace(".apk","")
        print apk_id, apk_name_en, apk_name_cn, apk_url, apk_webpage, apk_icon
        apkstring = "%s|%s|%s|%s|%s|%s" % (apk_id, apk_name_en, apk_name_cn, apk_url, apk_webpage, apk_icon)
        append2file("apkinfo.txt", apkstring)
        apklist.append(apkstring)
    #print len(apklist)
    return apklist



def get_apk_real_downloadurl(apkid):
    apkurl_prefix = "http://app.mi.com/download/"
    s = requests.session()
    headers = {
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language" : "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
      "Accept-Encoding" : "gzip, deflate,sdch",
      "Host" :  "app.mi.com",
      "User-Agent" :  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
      "Connection" : "keep-alive",
      "Cache-Control" : "no-cache",
    }
    s.headers.update(headers)
    resp = s.get(apkurl_prefix+str(apkid), timeout = 1000, allow_redirects=False)
    content = resp.content
    #print content
    template = '<a href="(.*?)">here</a>'
    real_url = re.compile(template)
    real_url = re.search(real_url,content).group(1)
    ##http://f5.market.mi-img.com/download/AppStore/044e54cd2ffb22f2f87baf3be3bd41255a543b33f/com.qiyi.video.apk
    return real_url


def downloadApk(apkid, apkfilename):
    s = requests.session()
    headers = {
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language" : "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
      "Accept-Encoding" : "gzip, deflate,sdch",
      "Host" :  "app.mi.com",
      "User-Agent" :  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
      "Connection" : "keep-alive",
      "Cache-Control" : "no-cache",
    }
    s.headers.update(headers)
    s.headers['Host'] = 'app.mi.com'
    resp = s.get('http://app.mi.com/download/'+str(apkid), timeout = 100, allow_redirects=False)
    content = resp.content
    #print "Content:", content
    template = '<a href="(.*?)">here</a>'
    real_url = re.compile(template)
    real_url = re.search(real_url,content).group(1)
    #print real_url
    apkrealname = real_url[real_url.rfind('/')+1:]
    apkrealname = urllib2.unquote(apkrealname)
    s.headers['Host'] = 'f3.market.xiaomi.com'
    resp = s.get(real_url,timeout = 100)
    content = resp.content
    with open(apkfilename,'wb+') as f:
      f.write(content)
    #
    pass



if __name__ == "__main__":
  allapklist = []
  gameswebpage = "http://app.mi.com/gTopList"
  appswebpages = ["http://app.mi.com/topList?page=%d" % i for i in xrange(1,43)]
  appswebpages.insert(0, gameswebpage)

  for weburl in appswebpages:
      apklist = fetchApkinfoFromWebpage(weburl)
      allapklist.extend(apklist)
  print len(allapklist)


  #downloadApk(125, "com.qiyi.video.apk")
  #print get_apk_real_downloadurl("http://app.mi.com/download/125")
  #write2file("com.qiyi.video.apk", getURL("http://app.mi.com/download/125"))
  
  #print BeautifulSoup(getURLContent("http://app.mi.com/detail/125"), from_encoding="utf-8").findAll(attrs={"class":"special-li"})[0].get_text()



