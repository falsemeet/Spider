#/sur/bin/env python
#-*-coding:utf-8-*-
#@auther=="guijianchou"
#HomePage: https://github.com/guijianchou/spider

import urllib2
import re
import threading
import copy
from Queue import Queue as TaskQ
import os
import time

st = 1 
ed = 100
album_host = "weidongrui.lofter.com"
get_gif = True
img_thread_cnt = 1
path = 'img'

finder = re.compile(r'<img src="(http://(imglf\d?\.(?:nosdn\.127|ph\.126)\.net)(?:/img)?/[=a-zA-Z\d/\-]+\.jpg)[\?"]')
def get_content(uri, headers=dict()):
    req = urllib2.Request(uri)
    for i in headers:
        req.add_header(i, headers[i])
    return urllib2.urlopen(req).read()
def pting():
    while True:
        if ppq.empty() == False:
            print ppq.get()
def ppt(s):
    ppq.put(s)
q = TaskQ()
ppq = TaskQ()
cnt = 0
tls = list()
ppp = threading.Thread(target = pting)
ppp.start()
if get_gif == True:
    finder = re.compile(r'<img src="(http://(imglf\d?\.(?:nosdn\.127|ph\.126)\.net)(?:/img)?/[=a-zA-Z\d/\-]+\.(?:gif|jpg))[\?"]')
hed = {
    "host": "imglf0.nosdn.127.net",
    "connection": "keep-alive",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2849.0 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.8"
}
hed2 = {
    "Host": album_host,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2849.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8",
    "Cookie": r"usertrack=ZUcIilfNSMYX92jEFuGoAg==; JSESSIONID-WLF-XXD=349b8f0fb287cd8cca5cb015b83b71020d6128f878c6f7441d707d9cab09b78209dfbf161d8d75c5f0c1a8a8c3c49a83b895d575a1a00a5a2cabfcffcea559652c045043d0683e0ace5384b797335054c261362132241cddd12ef6923c901e91f0e6b6023e71fa1c5918e1f026641d280fa26be3158ebdbb378e1f1d45aded874ad1913c; _ntes_nnid=9293516f048ca0b60f87383f93fcc85a,1473071297877; reglogin_hasopened=1; regtoken=2000; reglogin_isLoginFlag=; reglogin_isLoginFlag=; __utma=61349937.2091497105.1473071305.1473071305.1473071305.1; __utmb=61349937.24.8.1473072871458; __utmc=61349937; __utmz=61349937.1473071305.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
}
def organise(i, slp):
    l = 0
    while (l < 1):
        p = get_content('http://%s/?page=%d'%(album_host, i), hed2)
        lst = finder.findall(p)
        l = len(lst) + 1
    pcnt = 0
    for j in lst:
        tmph = copy.copy(hed)
        tmph['host'] = j[1]
        q.put((j[0], tmph))
        pcnt = pcnt + 1
    ppt(str(pcnt) + ' Done ' + str(i))
    global cnt
    cnt = cnt + 1
for i in xrange(st, ed + 1, 1):
    tls.append(threading.Thread(target = organise, args = (i, (ed - st + 1) / 10)))
    tls[-1].start()
while cnt < ed - st + 1:
    pass

def fetch():
    while q.empty() == False:
        try:
            tmp = q.get()
            fname = path + '\\' + tmp[0].split('/')[-1].split('/')[-1]
            p = get_content(tmp[0], tmp[1])
            f = open(fname, 'wb')
            f.write(p)
            f.close()
            ppt(str(q.qsize()) + ' Fetch ' + fname)
        except BaseException:
            if os.path.isfile(fname):
                try:
                    f.close()
                except BaseException:
                    pass
                os.remove(fname)
            if q.empty() == True:
                ppt('Thread terminated')
            ppt('oops ' + tmp[0])
tlst = list()
for i in xrange(img_thread_cnt):
    tlst.append(threading.Thread(target = fetch))
    tlst[-1].start()
