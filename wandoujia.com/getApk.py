#coding:utf-8

import os, sys, time, random, json
import re, requests, urllib2
import pprint
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup

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
        r = requests.get(url, headers=headers, timeout=1)
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




def get_apk_real_downloadurl(apk_name_en="com.tencent.mm"):
    apkurl_prefix = "http://apps.wandoujia.com/apps/"
    s = requests.session()
    headers = {
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
      "Accept-Language" : "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
      "Accept-Encoding" : "gzip, deflate,sdch",
      "Host" :  "apk.wandoujia.com",
      "User-Agent" :  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36",
      "Connection" : "keep-alive",
      "Cache-Control" : "no-cache",
    }
    s.headers.update(headers)
    resp = s.get(apkurl_prefix+str(apk_name_en), timeout = 1000, allow_redirects=False)
    content = resp.content
    #print content
    template = '<a href="(.*?)">here</a>'
    real_url = re.compile(template)
    real_url = re.search(real_url,content).group(1)
    ##http://f5.market.mi-img.com/download/AppStore/044e54cd2ffb22f2f87baf3be3bd41255a543b33f/com.qiyi.video.apk
    return real_url


if __name__ == "__main__":
	weburl="http://apps.wandoujia.com/apps/com.tencent.mm"
	html_doc = getURLContent(weburl)
	#print html_doc
	soup = BeautifulSoup(html_doc, from_encoding="utf-8") 
	downloadcount = soup.findAll(attrs={"class":"num-list"})[0].findAll("span", {"class":"item"})[0].i.contents[0]
	print type(downloadcount), downloadcount

	apk_icon = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"icon"})[0].img.get('src')
	apk_name_cn = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"icon"})[0].img.get('alt')
	print apk_name_cn
	apk_download_href = soup.findAll(attrs={"class":"main-info"})[0].findAll(attrs={"class":"btn-download btn-green install-btn"})[-1].get('href')

	apk_download_url = apk_download_href.split("&pn=")[0]
	write2file("com.tencent.mm.apk", apk_download_url)
	# for item in apk_download_href.split('amp'):
	# 	print item
	#print soup.find_all('num-list')

	#http://180.97.171.41/m.wdjcdn.com/apk.wdjcdn.com/c/f7/6834fd9186188819aebebec09d517f7c.apk#name=微信&icon=http://img.wdjimg.com/mms/icon/v1/7/ed/15891412e00a12fdec0bbe290b42ced7_68_68.png&content-type=application





