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
from selenium import webdriver
#import pymssql
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

	    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36')
	    request.add_header('Host','dh2015.org')
	    request.add_header('Connection','keep-alive')
	    request.add_header('Cache-Control','max-age=0')
	    request.add_header('Upgrade-Insecure-Requests','1')
	    #request.add_header('Cookie','PHPSESSID=l7mdc6vtk2in48fipb2qn15c10')
	    response = opener.open(request)
	    #读取HTML及其它网页格式
	    text = response.read().decode(code)
	    return text
    except:
        raise Exception('Broken URL')
    




def Loop():
    
    print("start")
    list_page_url = "http://dh2015.org/abstracts/data_titles.php?inputReset=no&showAll=yes&inputBox=inputTitleKeyword"
    list_page_data = getData(list_page_url,code = 'utf8')
    list_page_soup = BeautifulSoup(list_page_data,'html.parser')
    driver = webdriver.PhantomJS(executable_path='D:/phantomjs-2.1.1-windows/bin/phantomjs')
    #print(list_page_soup)
    paper_boxes = list_page_soup.find_all('td')
    for paper_box in paper_boxes:
        paper_title = paper_box.getText().strip()
        #paper_title = "AXES: Researching & Accessing Videos Through Multimodal Analyses"
        print(paper_title)
        url_base = "http://dh2015.org/abstracts/data_records.php?alias="+ urllib.parse.quote("Abstracts By Title")+"&filter=Titles&searchText="
        #获取每篇文章url
        paper_url = url_base + urllib.parse.quote(paper_title).replace("%3A",":")
        print(paper_url)
        sleeptime = random.uniform(1,3)
        time.sleep(round(sleeptime,2))
        #print(urllib.parse.quote(paper_url))
        #paper_page_data = getData(paper_url,code = 'utf8')
        
        driver.get(paper_url)
        #print(driver.page_source)
        papger_page_soup = BeautifulSoup(driver.page_source,'html.parser')

        if papger_page_soup.find('a',{'target':'_dh2015XML'}) is None:
            print("这篇文章没有资料")
            continue
        else:            
            #print(papger_page_soup)
            paper_xml_url = papger_page_soup.find('a',{'target':'_dh2015XML'})['href']
            #print(paper_xml_url)
            full_xml_url = "http://dh2015.org/abstracts"+paper_xml_url[1:len(paper_xml_url)]
            sleeptime = random.uniform(1,3)
            time.sleep(round(sleeptime,2))
            #print(full_xml_url)
            paper_xml_page = getData(full_xml_url, code = 'utf-8')
            #打开每篇文章的xml
            paper_xml = BeautifulSoup(paper_xml_page,'xml')
            title,institutions,locations,keywords,topics,fulltext = readXML(paper_xml)
            #print(title + " " + institutions + " " + keywords +" " + topics)
            savetoSQL(title,institutions,locations,keywords,topics,fulltext,2015)
            #time.sleep(round(sleeptime,2))



    # for paper in papers:
    #     #获取每篇文章url
    #     paper_url = "http://dh2016.adho.org" + paper.find('a')['href']
    #     sleeptime = random.uniform(1,3)
    #     time.sleep(round(sleeptime,2))
    #     paper_data = getData(paper_url, code = 'utf-8')
    #     paper_soup = BeautifulSoup(paper_data,'html.parser')
    #     #获取每篇文章xml的url
    #     paper_xml_url = "http://dh2016.adho.org" + paper_soup.find('div',{'class':'col-xs-12'}).find('a',{'class':'btn'})['href']
    #     paper_soup.clear()
    #     paper_xml_page = getData(paper_xml_url, code = 'utf-8')
    #     #打开每篇文章的xml
    #     paper_xml = BeautifulSoup(paper_xml_page,'xml')
        
    #     title,institutions,locations,keywords,topics,fulltext = readXML(paper_xml)



    #     savetoSQL(title,institutions,locations,keywords,topics,fulltext,2015)


            


            

def main():
    Loop()

if __name__=="__main__":
    main()
