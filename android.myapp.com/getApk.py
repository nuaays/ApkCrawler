#coding:utf-8

import json


jsonfile = "appList.json"

content = open(jsonfile).read()
print type(content), len(content)
print content

#content.decode("GB2312")
# dcontent = content.decode("gbk").encode("utf-8")
# str1 = json.loads(dcontent, encoding="utf-8")
# print str1

for i in  content.split("pkgName"):
	print i

# dcontent = content.decode("GB2312")
# str1 = json.loads(dcontent, encoding="GB2312")
# print str1



# d1 = json.dumps(content,sort_keys=True)
# print d1

# http://android.myapp.com/myapp/category.htm?orgame=1&categoryId=103
# http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=20&pageContext=100
# http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=20&pageContext=43
# http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=20&pageContext=69
# http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=20&pageContext=93

print "-"*40

for l in open(jsonfile).read().split("pkgName\":")[1:]:
	print l




import os, sys, time, random
import requests, urllib2

USER_AGENTS = (
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_0; en-US) AppleWebKit/534.21 (KHTML, like Gecko) Chrome/11.0.678.0 Safari/534.21",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; en-US; rv:0.9.2) Gecko/20020508 Netscape6/6.1",
    "Mozilla/5.0 (X11;U; Linux i686; en-GB; rv:1.9.1) Gecko/20090624 Ubuntu/9.04 (jaunty) Firefox/3.5",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
    "Opera/9.80 (X11; U; Linux i686; en-US; rv:1.9.2.3) Presto/2.2.15 Version/10.10"
)

def getURLContent(url='http://www.eloancn.com/randCode/randCode.jsp'):
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://android.myapp.com/myapp/detail.htm?apkName=com.tencent.qqlive'        
               }

    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0" #USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]

    try:
        r = requests.get(url, params={'ip': '8.8.8.8'}, headers=headers, timeout=1)
        r.raise_for_status()
    except requests.RequestException as e:
        print e
        return None
    else:
    	print r.encoding
        return r.content

def getURL(url='http://www.eloancn.com/randCode/randCode.jsp'):
    print "[Download]%s" % url
    headers = {
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate', 
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Connection' : 'keep-alive',
               'Referer' : 'http://android.myapp.com/myapp/detail.htm?apkName=com.tencent.qqlive'        
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

if __name__ == "__main__":
	print "XXX"
	#appwebpageurl="http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=103&pageSize=20&pageContext=43"
	for i in [103,101,122,102,112,106,104,110,115,119,111,107,118,108,100,114,117,109,105,113,116]:
		for j in [43,69,93,100]:
			appwebpageurl="http://android.myapp.com/myapp/cate/appList.htm?orgame=1&categoryId=%d&pageSize=20&pageContext=%d" % (i, j)
			print appwebpageurl
			download(appwebpageurl)
