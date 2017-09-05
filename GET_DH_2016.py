#!/usr/bin/python3
#coding=utf-8


#==================================================import============================================================
import urllib.parse
import urllib.request
import urllib.error
import http.cookiejar
import codecs
import re
from bs4 import BeautifulSoup
import os
import json
import requests
import time
import winsound
import random
import pymssql
from retrying import retry
from Base_Functions import readXML
from Base_Functions import savetoSQL
#==================================================set cookie==========================================================
cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
hander = urllib.request.HTTPCookieProcessor(cookie) #HTTPCookieProcessor object to set cookie hander
opener = urllib.request.build_opener(hander) ##set opener by cookie hander
urllib.request.install_opener(opener)


#==================================================get data=============================================================
@retry
def getData(url, code) :
    try:
	    #访问该url的请求
	    request = urllib.request.Request(url)
	
	    #发送请求包
	    response = opener.open(request)
	    #读取HTML及其它网页格式
	    text = response.read().decode(code)
	    return text
    except:
        raise Exception('Broken URL')
    




def Loop():
    
    url_base = "http://dh2016.adho.org/abstracts/browse/title/"
    for i in range(1,10):
        url = url_base + str(i) + "/"
        sleeptime = random.uniform(3,5)
        time.sleep(round(sleeptime,2))
        data = getData(url, code = 'utf-8')

        print("This is page %d" %i)

        soup = BeautifulSoup(data,'html.parser')
        #获取文章列表
        paper_lists = soup.find('ul')
        soup.clear()

        papers = paper_lists.find_all('li')

        for paper in papers:
            #获取每篇文章url
            paper_url = "http://dh2016.adho.org" + paper.find('a')['href']
            sleeptime = random.uniform(1,3)
            time.sleep(round(sleeptime,2))
            paper_data = getData(paper_url, code = 'utf-8')
            paper_soup = BeautifulSoup(paper_data,'html.parser')
            #获取每篇文章xml的url
            paper_xml_url = "http://dh2016.adho.org" + paper_soup.find('div',{'class':'col-xs-12'}).find('a',{'class':'btn'})['href']
            paper_soup.clear()
            paper_xml_page = getData(paper_xml_url, code = 'utf-8')
            #打开每篇文章的xml
            paper_xml = BeautifulSoup(paper_xml_page,'xml')
            
            title,institutions,locations,keywords,topics,fulltext = readXML(paper_xml)



            #savetoSQL(title,institutions,locations,keywords,topics,fulltext,2016)


            


            

def main():
    Loop()

if __name__=="__main__":
    main()
