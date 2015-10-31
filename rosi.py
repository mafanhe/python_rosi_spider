__author__ = 'mafanhe'
# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import os

class Spider:
    def __init__(self):
        self.siteURL = 'http://www.mmkds.com/rosi-'
        self.user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
        #初始化headers
        self.headers = {'User-Agent' : self.user_agent}

    def getPage(self, pageIndex):
        url = self.siteURL+str(pageIndex)
        print url
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print url+u"连接失败，错误原因",e.reason
                return None
    def getAllImg(self, pageIndex ):
        page = self.getPage(pageIndex)
        # print page
        if(page is not None):
            pattern = re.compile("<dt class='gallery-icon'.*?<a href='(.*?)'", re.S)
            items = re.findall(pattern, page)
            self.saveImgs(items,pageIndex)
    def saveImgs(self,images,pageIndex):
        number = 1
        print u"发现",len(images),u"张图片"
        self.mkdir(str(pageIndex))
        print u"请耐心等待，正在保存图片....."
        for imageURL in images:
            # print imageURL
            splitPath = imageURL.split('.')
            fTail = splitPath.pop()
            if len(fTail)>3:
                fTail = "jpg"
            fileName = str(pageIndex)+'/'+str(number)+"."+fTail
            self.saveImg(imageURL,fileName)
            number += 1
    def saveImg(self,imageURL,fileName):
        u = urllib.urlopen(imageURL)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        print u"正在保存图片",fileName
        f.close()
    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print u"创建名为",path, u'的文件夹'
            os.makedirs(path)
            return True
        else:
            print u"名为",path,u'的文件夹已经创建成功'
            return False
spider = Spider()
pageNum = raw_input("请输入rosi图片番号：\n")
spider.getAllImg(pageNum)
print "END"
