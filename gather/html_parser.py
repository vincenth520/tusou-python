#!/usr/bin/env python
#!_*_coding:utf-8_*_
# @Date    : 2016-04-05 19:02:14
# @Author  : Vincent H (1091986039@qq.com)
# @Link    : http://luvial.cn
# @Version : $Id$
from bs4 import BeautifulSoup
import time,uuid
import re,os
#import html_downloader
if __name__ == '__main__':
	import html_downloader
else:
    from . import html_downloader

class HtmlParser(object):
	
	def __init__(self,s):
		self.search = s

	def _get_new_urls(self,page_url,soup):
		new_urls = set()
		img = soup.find_all('div',class_='e')
		links = soup.find_all('a',href=re.compile(r'http://www.topit.me/items/search\?query=[\%\=\&\w]+'))
		for i in img:
			imglist = i.find('a',href=re.compile(r'http://www.topit.me/item/\d+'))
			new_urls.add(imglist['href'])
		for link in links:
			new_urls.add(link['href'])
		return new_urls


	def set_path(self):
		return ('%s/static/tmp/%s' %(os.getcwd(),self.search))

	def _get_new_data(self,page_url,soup):
		#img admin_collection ui-draggable
		try:
			new_data_path = set()
			img = soup.find('img',class_='admin_collection')
			id = '%s/%015d%s000.jpg' %(self.set_path(),int(time.time() * 1000),uuid.uuid4().hex)
			# id = id.encode()
			# id = id.decode()
			downloader = html_downloader.HtmlDownloader()
			#print(id)
			pic = downloader.download(img['src'])
			#print(pic)
			f = open(id,'wb')
			f.write(pic)
			f.close()
			id = id.replace(os.getcwd(),'')
			print(id)
			new_data_path.add(id)
			return new_data_path
		except Exception as ex: 
			print (Exception,"[html_parser.py]:",ex )
			

	def parse(self,page_url,html_cont):
		if page_url is None or html_cont is None:
			return

		new_data = set('')
		new_urls = set('')
		soup = BeautifulSoup(html_cont,'html.parser',from_encoding='utf-8')
		t=re.search(r'http://www.topit.me/items/search\?query=[\%\=\&\w]+',page_url)
		if t:
			#print(page_url,'1')
			new_urls = self._get_new_urls(page_url,soup)
		else:
			#print(page_url,'2')
			new_data = self._get_new_data(page_url,soup)
		return new_urls,new_data
		
