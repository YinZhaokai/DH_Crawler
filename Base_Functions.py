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
#==================================================set cookie==========================================================
cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
hander = urllib.request.HTTPCookieProcessor(cookie) #HTTPCookieProcessor object to set cookie hander
opener = urllib.request.build_opener(hander) ##set opener by cookie hander
urllib.request.install_opener(opener)



def savetoSQL(title,institutions,locations,keywords,topics,fulltext,year):
    conn = pymssql.connect(host='SHINELON-PC\SA',user='sa',password='sa',database='DigitalHumanities')

    cur = conn.cursor()

    cur.execute( "SELECT * FROM [DigitalHumanities].[dbo].[Digital_Humanities_Conference] WHERE [TITLE] = ' %s ' AND [YEAR] = %d"%(title,year))

    reslist = cur.fetchall()

    if len(reslist) >= 1:
        print("Data Already in")
    else:
        print("No Data")    
        cur.execute("INSERT INTO [DigitalHumanities].[dbo].[Digital_Humanities_Conference] VALUES ('%s','%s','%s','%s','%s','%s','%d')"%(title,institutions,locations,keywords,topics,fulltext,year))
        conn.commit()
        print("Finish Saving")
        print(" ")

    cur.close()
    conn.close()

def readXML(paper_xml):
    #获取文章标题
    title = paper_xml.find('title').getText().strip().replace("'","''")
    print(title)
    authors = paper_xml.find_all('author')
    #names = []
    institutions = ""
    locations = ""
    #获取每篇文章作者姓名、机构和机构所在区域
    for author in authors:
        #name = author.find('surname').getText().strip() + " " + author.find('forename').getText().strip()
        #print(name)
        #names.append(name)
        temp = author.find('affiliation').getText().strip().split(',')
        if len(temp)==2:
            institution = temp[0].replace("'","''") + ',' +'\t'
            location = temp[1].replace("'","''") + ',' + '\t'
        else:
            institution = temp[0].replace("'","''") + ',' +'\t'
            location = '\t'
        #institution = author.find('affiliation').getText().strip()
        institutions += institution
        locations += location
        #location = author.find('affiliation').getText().strip().split(',')[1]
        #locations.append(location)

    keywords = ""
    topics = ""          
    #获取每篇文章keywords
    xml_keywords = paper_xml.find('keywords',{'n':'keywords'}).find_all('term')
    for xml_keyword in xml_keywords:
        keyword = xml_keyword.getText().strip().replace("'","''") + ','
        keywords += keyword
    print(keywords)
    #获取每篇文章topics
    xml_topics = paper_xml.find('keywords',{'n':'topics'}).find_all('term')
    for xml_topic in xml_topics:
        topic = xml_topic.getText().strip().replace("'","''") + ','
        topics += topic
    print(topics)
    #获取每篇文章正文。必须以''替换'，否则会在导入数据库时出错
    fulltext = paper_xml.find('text').find('body').getText().strip().replace("'","''")
    return title,institutions,locations,keywords,topics,fulltext
            