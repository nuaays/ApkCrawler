#coding:utf-8

import os, sys, time, random, json
import re, requests, urllib2
import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import cPickle

# http://apps.wandoujia.com/,  2626288个软件
# 下载总排行 http://apps.wandoujia.com/top/total?zh=0
# 全部软件 http://apps.wandoujia.com/tag/%E5%85%A8%E9%83%A8%E8%BD%AF%E4%BB%B6
# 全部游戏 http://apps.wandoujia.com/tag/%E5%85%A8%E9%83%A8%E6%B8%B8%E6%88%8F?pos=w/crumb/tag

# 视频 http://apps.wandoujia.com/tag/%E8%A7%86%E9%A2%91?page=1
# 视频·春晚 http://apps.wandoujia.com/tag/%E8%A7%86%E9%A2%91%C2%B7%E6%98%A5%E6%99%9A?page=1
# 音乐 http://apps.wandoujia.com/tag/%E9%9F%B3%E4%B9%90?page=1
# 图像 http://apps.wandoujia.com/tag/%E5%9B%BE%E5%83%8F?page=1
# 购物 http://apps.wandoujia.com/tag/%E8%B4%AD%E7%89%A9?page=1
# 购物·年货 http://apps.wandoujia.com/tag/%E8%B4%AD%E7%89%A9%C2%B7%E5%B9%B4%E8%B4%A7?page=1
# 美化手机 http://apps.wandoujia.com/tag/%E7%BE%8E%E5%8C%96%E6%89%8B%E6%9C%BA?page=1
# 聊天社交 http://apps.wandoujia.com/tag/%E8%81%8A%E5%A4%A9%E7%A4%BE%E4%BA%A4?page=1
# 交通导航 http://apps.wandoujia.com/tag/%E4%BA%A4%E9%80%9A%E5%AF%BC%E8%88%AA?page=1
# 运动健康 http://apps.wandoujia.com/tag/%E8%BF%90%E5%8A%A8%E5%81%A5%E5%BA%B7?page=1
# 金融理财 http://apps.wandoujia.com/tag/%E9%87%91%E8%9E%8D%E7%90%86%E8%B4%A2?page=1
# 理财·红包 http://apps.wandoujia.com/tag/%E7%90%86%E8%B4%A2%C2%B7%E7%BA%A2%E5%8C%85?page=1
# 新闻阅读 http://apps.wandoujia.com/tag/%E6%96%B0%E9%97%BB%E9%98%85%E8%AF%BB?page=1
# 系统工具 http://apps.wandoujia.com/tag/%E7%B3%BB%E7%BB%9F%E5%B7%A5%E5%85%B7?page=1
# 效率办公 http://apps.wandoujia.com/tag/%E6%95%88%E7%8E%87%E5%8A%9E%E5%85%AC?page=1
# 电话通讯 http://apps.wandoujia.com/tag/%E7%94%B5%E8%AF%9D%E9%80%9A%E8%AE%AF?page=1
# 旅游出行 http://apps.wandoujia.com/tag/%E6%97%85%E6%B8%B8%E5%87%BA%E8%A1%8C?page=1
# 旅行·购票 http://apps.wandoujia.com/tag/%E6%97%85%E8%A1%8C%C2%B7%E8%B4%AD%E7%A5%A8?page=1
# 生活服务 http://apps.wandoujia.com/tag/%E7%94%9F%E6%B4%BB%E6%9C%8D%E5%8A%A1?page=1
# 教育培训 http://apps.wandoujia.com/tag/%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD?page=1
# 丽人母婴 http://apps.wandoujia.com/tag/%E4%B8%BD%E4%BA%BA%E6%AF%8D%E5%A9%B4?page=1
# 生活实用工具 http://apps.wandoujia.com/tag/%E7%94%9F%E6%B4%BB%E5%AE%9E%E7%94%A8%E5%B7%A5%E5%85%B7?page=1


#http://apps.wandoujia.com/redirect?signature=72aaeb5&url=http%3A%2F%2Fapk.wandoujia.com%2Fc%2Ff7%2F6834fd9186188819aebebec09d517f7c.apk&pn=com.tencent.mm&md5=6834fd9186188819aebebec09d517f7c&apkid=17178194&vc=700&size=35705360&pos=t%2Fdetail#name=微信&icon=http://img.wdjimg.com/mms/icon/v1/7/ed/15891412e00a12fdec0bbe290b42ced7_68_68.png&content-type=application

def save2pkl(dataobject, pklfile):
	with open(pklfile,"wb") as fh:
		cPickle.dump(dataobject, fh)


USER_AGENTS = (
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.1",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
    'Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10'
)

def getURLContent(url='http://apps.wandoujia.com/apps/com.tencent.mm'):
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://apps.wandoujia.com'        
               }

    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0" #USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]

    try:
        r = requests.get(url, headers=headers, timeout=1000)
        r.raise_for_status()
    except requests.RequestException as e:
        print e
        return None
    else:
        print r.encoding
        return r.content

def getURL(url='http://apps.wandoujia.com/apps/com.tencent.mm'):
    print "[Download]%s" % url
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://apps.wandoujia.com'        
               }
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0"

    try:
        r = requests.get(url, headers=headers, timeout=1000)
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


def get_apk_real_downloadurl(apkurl):
    #http://apps.wandoujia.com/redirect?signature=72aaeb5&url=http%3A%2F%2Fapk.wandoujia.com%2Fc%2Ff7%2F6834fd9186188819aebebec09d517f7c.apk&pn=com.tencent.mm&md5=6834fd9186188819aebebec09d517f7c&apkid=17178194&vc=700&size=35705360&pos=t%2Fdetail#name=微信&icon=http://img.wdjimg.com/mms/icon/v1/7/ed/15891412e00a12fdec0bbe290b42ced7_68_68.png&content-type=application
    #http://apps.wandoujia.com/redirect?signature=72aaeb5&url=http%3A%2F%2Fapk.wandoujia.com%2Fc%2Ff7%2F6834fd9186188819aebebec09d517f7c.apk
    #6834fd9186188819aebebec09d517f7c.apk
    #http://apk.wandoujia.com/c/f7/6834fd9186188819aebebec09d517f7c.apk
    apk_redirect_url = "http://apk.wandoujia.com/c/f7/" + apkurl.split("&pn=")[0].split("%2F")[-1]
    apk_real_downloadurl = ""

    s = requests.session()
    headers = {
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language" : "en-US,en;q=0.5",
      "Accept-Encoding" : "gzip, deflate",
      "Host" :  "apk.wandoujia.com",
      "User-Agent" :  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
      "Connection" : "keep-alive",
      #"Cache-Control" : "no-cache",
      #'Cookie': '_ga=GA1.2.547995142.1452520047; Hm_lvt_c680f6745efe87a8fabe78e376c4b5f9=1452520047; lv=1453034963871; __utma=49511670.547995142.1452520047.1452521677.1453034965.2; __utmz=49511670.1452521677.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=49511670; PRUM_EPISODES=s=1453045185861&r=http%3A//apps.wandoujia.com/top/total'
    }
    s.headers.update(headers)
    resp = s.get(apk_redirect_url, timeout = 100, allow_redirects=False)
    #print "XXX:", resp.status_code #302
    #print "XXX:", resp.headers.get("Location")
    #http://180.97.171.41/m.wdjcdn.com/apk.wdjcdn.com/c/f7/6834fd9186188819aebebec09d517f7c.
    return resp.headers.get("Location")


def getOneApkinfo(apk_name="com.tencent.mm"):
	apk_weburl="http://apps.wandoujia.com/apps/" + apk_name
	#apk_weburl="http://apps.wandoujia.com/apps/com.tencent.mm"
	apk_all_versions = apk_weburl + "/versions"
	#
	html_doc = getURLContent(apk_weburl)
	soup = BeautifulSoup(html_doc, from_encoding="utf-8") 
	#
	apk_downloadcount = soup.findAll(attrs={"class":"num-list"})[0].findAll("span", {"class":"item"})[0].i.contents[0]
	apk_icon = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"icon"})[0].img.get('src')
	apk_name_cn = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"icon"})[0].img.get('alt')
	apk_name_en = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"app-txt app"})[0].get("data-pn")
	download_href = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"btn-download btn-green install-btn"})[-1].get('href')
	apk_download_url = get_apk_real_downloadurl(download_href)
	apk_size = soup.findAll('dl',{'class':'app-attrs'})[0].dd.contents[0]
	apk_catagory = soup.findAll('a',{'class':'detail-tag'})[-1].contents[0]
	
	#write2file("com.tencent.mm.apk", apk_download_url)
	apkinfostring = "%s|%s|%s|%s|%s|%s|%s|%s" % (apk_name_en, apk_name_cn, apk_size, apk_downloadcount, apk_download_url, apk_icon, apk_all_versions, apk_catagory)
	append2file("apkinfo", apkinfostring)
	print apkinfostring
	return apkinfostring



def getSubpageMaxnum(webpage="http://apps.wandoujia.com/tag/%E6%97%85%E8%A1%8C%C2%B7%E8%B4%AD%E7%A5%A8"):
	print "[catagory]", webpage
	return BeautifulSoup(getURLContent(webpage), from_encoding="utf-8").findAll('a',{'class':'page-item'})[-2].contents[0]

def fetchApksNameFromOneWebpage(webpage="http://apps.wandoujia.com/tag/%E6%97%85%E8%A1%8C%C2%B7%E8%B4%AD%E7%A5%A8"):
	apksname = []
	html_doc = getURLContent(webpage)
	soup = BeautifulSoup(html_doc, from_encoding="utf-8")
	for i in soup.findAll('div',{'class':'app full '}):
		print i.get("data-pn")
		apksname.append(i.get("data-pn"))
	#print soup.findAll('div',{'class':'page-wp roboto'})[0].findAll('a',{'class':'page-item'})
	#print soup.findAll('a',{'class':'page-item'})[-2].contents[0]

	return apksname



if __name__ == "__main__":
	apknamelist = fetchApksNameFromOneWebpage("http://apps.wandoujia.com/tag/%E5%85%A8%E9%83%A8%E8%BD%AF%E4%BB%B6")
	print len(apknamelist)

	catagory = {#'视频':'http://apps.wandoujia.com/tag/%E8%A7%86%E9%A2%91',
				'视频·春晚':'http://apps.wandoujia.com/tag/%E8%A7%86%E9%A2%91%C2%B7%E6%98%A5%E6%99%9A',
				'音乐':'http://apps.wandoujia.com/tag/%E9%9F%B3%E4%B9%90',
				'图像':'http://apps.wandoujia.com/tag/%E5%9B%BE%E5%83%8F',
				#'购物':'http://apps.wandoujia.com/tag/%E8%B4%AD%E7%89%A9',
				'购物·年货':'http://apps.wandoujia.com/tag/%E8%B4%AD%E7%89%A9%C2%B7%E5%B9%B4%E8%B4%A7',
				'美化手机':'http://apps.wandoujia.com/tag/%E7%BE%8E%E5%8C%96%E6%89%8B%E6%9C%BA',
				'聊天社交':'http://apps.wandoujia.com/tag/%E8%81%8A%E5%A4%A9%E7%A4%BE%E4%BA%A4',
				'交通导航':'http://apps.wandoujia.com/tag/%E4%BA%A4%E9%80%9A%E5%AF%BC%E8%88%AA',
				'运动健康':'http://apps.wandoujia.com/tag/%E8%BF%90%E5%8A%A8%E5%81%A5%E5%BA%B7',
				#'金融理财':'http://apps.wandoujia.com/tag/%E9%87%91%E8%9E%8D%E7%90%86%E8%B4%A2',
				'理财·红包':'http://apps.wandoujia.com/tag/%E7%90%86%E8%B4%A2%C2%B7%E7%BA%A2%E5%8C%85',
				'新闻阅读':'http://apps.wandoujia.com/tag/%E6%96%B0%E9%97%BB%E9%98%85%E8%AF%BB',
				'系统工具':'http://apps.wandoujia.com/tag/%E7%B3%BB%E7%BB%9F%E5%B7%A5%E5%85%B7',
				'效率办公':'http://apps.wandoujia.com/tag/%E6%95%88%E7%8E%87%E5%8A%9E%E5%85%AC',
				'电话通讯':'http://apps.wandoujia.com/tag/%E7%94%B5%E8%AF%9D%E9%80%9A%E8%AE%AF',
				#'旅游出行':'http://apps.wandoujia.com/tag/%E6%97%85%E6%B8%B8%E5%87%BA%E8%A1%8C',
				'旅行·购票':'http://apps.wandoujia.com/tag/%E6%97%85%E8%A1%8C%C2%B7%E8%B4%AD%E7%A5%A8',
				'生活服务':'http://apps.wandoujia.com/tag/%E7%94%9F%E6%B4%BB%E6%9C%8D%E5%8A%A1',
				'教育培训':'http://apps.wandoujia.com/tag/%E6%95%99%E8%82%B2%E5%9F%B9%E8%AE%AD',
				'丽人母婴':'http://apps.wandoujia.com/tag/%E4%B8%BD%E4%BA%BA%E6%AF%8D%E5%A9%B4',
				'生活实用工具':'http://apps.wandoujia.com/tag/%E7%94%9F%E6%B4%BB%E5%AE%9E%E7%94%A8%E5%B7%A5%E5%85%B7'
				}
	#
	allapkinformation = []
	for key, value in catagory.items():
		#print key, value
		startnum=1
		endnum = getSubpageMaxnum(value)
		#print key, startnum, endnum
		webpageurls = [ value+"?navType=app&pos=w/tag/appnav&page=%d" % num for num in xrange(1, int(endnum))]
		apksname = []
		for url in webpageurls:
			print key, url
			apksname.extend(fetchApksNameFromOneWebpage(url))
		
		for apkname in apksname:
			allapkinformation.append(getOneApkinfo(apkname))
		save2pkl(allapkinformation, "allapkinfo.pkl")




	#
	#print BeautifulSoup(getURLContent("http://apps.wandoujia.com/apps/com.twitter.android?pos=w%2Fapps%2Ftags%2F%E5%85%A8%E9%83%A8%E8%BD%AF%E4%BB%B6%2FsuperiorFirst"), from_encoding="utf-8").findAll('a',{'class':'detail-tag'})[-1].contents[0]









