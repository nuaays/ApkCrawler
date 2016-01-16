#coding:utf-8

import os, sys, time, random, json
import requests, urllib2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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

def getURL(url='http://zhushou.360.cn/list/index/cid/1/'):
    print "[Download]%s" % url
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://zhushou.360.cn/detail/index/soft_id/77208'        
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

def download(appwebpageurl):
	for l in getURLContent(appwebpageurl).split("pkgName\":")[1:]:
		#print l
		array=l.split(",")
		apkname_en=array[0].strip('"')
		apkname_CN=""
		apkdownload=""		
		apksingleweb="http://android.myapp.com/myapp/detail.htm?apkName=%s" % apkname_en
		apksingleweb_content = getURLContent(apksingleweb).split("\n")
		for i in apksingleweb_content:
			if "det-ins-btn" in i and "onclick" in i and "asistanturlid" in i:
				#print i.split()
				apkdownload=i.split()[4].split('"')[1]
				print apkdownload


		for i in array:
			if "appName" in i:
				key, value = i.strip('"').split(":")
				#print key.strip('"'), value.strip('"')
				apkname_CN = value.strip('"')
			if "apkUrl" in i:
				#print i
				apkurl=i.split(":\"")[-1].strip('"')
				#print apkurl
				#apkdownload = apkurl.replace("&asr=8eff","")
				#print apkdownload
		apkname_filename=apkdownload.split("=")[-1]
		
		#write2file(apkname_filename, getURL(apkdownload))
		#print apkname_CN.decode("utf-8").encode("gb2312").decode("utf-8")

		try:
			#print apkname_en ,unicode(apkname_CN, "UTF-8"), apkdownload
			write2file(unicode(apkname_CN,"UTF-8")+".apk", getURL(apkdownload))
		except Exception, e:
			#print apkname_en ,unicode(apkname_CN, "UTF-8"), apkdownload
			print e
		#file(apkname_en, 'wb').write(urllib2.urlopen(apkdownload).read())
	#
	#write2file('AcFun', getURL('http://dd.myapp.com/16891/2234C387A04515252915D42D016BDF58.apk?fsname=tv.acfundanmaku.video_4.1.0_180.apk'))


def getApksFromOneWebPage(pageurl="http://zhushou.360.cn/list/index/cid/1", catagorynum=1):
	app_infodict={}

	content = getURLContent(pageurl)
	try:
		appsinfoline = [line for line in content.split("\n") if "sid=" in line][0].strip()
	except Exception, e:
		print e
		print pageurl
		print content
		return app_infodict

	#
	appsinfo = appsinfoline.split("<li>")
	for appinfo in appsinfo:
		appinfoarray = appinfo.split("href=\"")[-1].split("&")
		app_catagory=catagorynum
		app_softid = ""
		app_name = ""
		app_icon = ""
		app_apk_url = ""
		app_url = "http://zhushou.360.cn/detail/index/soft_id/"
		app_size = ""
		app_downloadcount = ""


		try:
			for item in appinfoarray:
				item = item.replace("'","")
				if "name" in item:
					app_name = item.split("=")[-1]
				if "icon" in item:
					app_icon = item.split("=")[-1]
				if "softid" in item:
					app_softid = item.split("=")[-1]
					app_url = "http://zhushou.360.cn/detail/index/soft_id/"+app_softid
				if "url" in item:
					app_apk_url = item.split("\"")[0].split("=")[-1]
			if app_name == "":
				continue
			else:
				appwebpagecontent = getURLContent(app_url).split("\n")
				info = []
				for line in appwebpagecontent:
					if "span class=\"s-3\"" in line:
						info.append(line.split(">")[1].split("<")[0].split("：")[-1])

				app_downloadcount, app_size = info[0:2]


			print app_softid, app_name, app_icon, app_apk_url
			append2file("apk_info_summary.txt", "%d|%s|%s|%s|%s|%s|%s" % (app_catagory, app_softid, app_name, app_icon, app_apk_url, app_size, app_downloadcount))
			#
			#
			app_infodict[app_softid] = {"name":app_name, "softid":app_softid, "catagory":app_catagory, "url":app_url, "icon":app_icon, "apk":app_apk_url, "apksize":app_size, "downloadcount":app_downloadcount}

			#download icon
			write2file("icon/"+app_softid+".png", getURL(app_icon))
		except Exception, e:
			print e

	#
	return app_infodict



 def fetchApkinfoFromWebpage():
 	pass


if __name__ == "__main__":
	zhoushou360 ={"全部":1, "系统安全":11,"通讯社交":12,"影音视听":14,"新闻阅读":15,"生活休闲":16,"主题壁纸":18,"办公商务":17,"摄影摄像":102228,"购物优惠":102230,"地图旅游":102231,"教育学习":102232,"金融理财":102139,"健康医疗":102233}
	#zhoushou360 ={"购物优惠":102230,"地图旅游":102231,"教育学习":102232,"金融理财":102139,"健康医疗":102233}
	#"摄影摄像":102228,


	app_info_dict_summary = {}

	#
	html_doc = getURLContent("http://app.mi.com/topList?page=1")
	from bs4 import BeautifulSoup  
	soup = BeautifulSoup(html_doc, from_encoding="utf-8") 
	#soup = BeautifulSoup(html_markup,"lxml",from_encoding="utf-8")  
	#print soup.prettify()
	print soup.title
	# print soup.title.name
	# print soup.title.string.encode("utf-8")
	# print soup.p
	# print soup.a
	# print soup.div

	apklist = []

	for item in soup.findAll(attrs={"class":"applist"})[0]:
		#print item
		item_soup = BeautifulSoup(str(item))
		apk_icon = apk_name = item_soup.find_all('img')[0].get('data-src')
		apk_name = item_soup.find_all('h5')[0].get_text() #item_soup.find_all('a')[-2].get_text() #item_soup.find_all('h5')[0].get_text() ##apk_name = item_soup.find_all('img')[0].get('alt').encode('utf-8')
		apk_webpage = "http://app.mi.com" + item_soup.find_all('a')[-1].get('href')
		print apk_name, apk_webpage, apk_icon
		apklist.append(apk_webpage)
		#http://f5.market.mi-img.com/download/AppStore/044e54cd2ffb22f2f87baf3be3bd41255a543b33f/com.qiyi.video.apk

	print len(apklist)

 
